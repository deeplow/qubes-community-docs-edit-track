
## Part 2 of [Playing with qubes]
Is a rewrite of my old notes, [Qubes OS Installation - Detached encrypted boot and header]

Thank you @kaizer and @dum0 for donating to qubes so that I could rewrite this guide.

I'd recommend that you try in VM first, before doing it on your machine, so that you can also learn and understand too.
 
This is _**UEFI**_ based only.

* Prerequisite :
  * QubesOS Installation Medium.
  * 2 Drives for separated Root and Boot/EFI Partition, and we would call them with :
     * Root = /dev/nvme0n1
     * Boot = /dev/sda

* After booting into installation in language section, press ctrl + alt + f2 to enter tty2

* Format drive we would use for the installation.
  * > dd if=/dev/urandom of=/dev/nvme0n1 bs=1M status=progress
  * > dd if=/dev/urandom of=/dev/sda bs=1M status=progress

* Create Boot, EFI, Root Header, Swap Header Partition.

  Boot Partition
  * > sgdisk -n 0:0:+200MiB -t 0:ef02 /dev/sda 
  
  EFI Partition
  * > sgdisk -n 0:0:+200MiB -t 0:ef00 /dev/sda
  
  Root Header Partition
  * > sgdisk -n 0:0:+16MiB -t 0:8309 /dev/sda

  If you want to use BTRFS also add swap header, another FS is not needed.
  
  Swap Header Partition
  * > sgdisk -n 0:0:+16MiB -t 0:8309 /dev/sda

### XFS / EXT4
* Create custom Luks configuration.
  * > cryptsetup -c aes-xts-plain64 -h sha512 -s 512 -y -i 10000 luksFormat /dev/nvme0n1
  
  You may want to use -i 1 (iterations 1ms) to speed up decrypting process for practice.

  Of course you can choose another -c (chiper) -h (hash size) -s (key size)
  * > cryptsetup luksOpen /dev/nvme0n1 luks-root
  * > pvcreate /dev/mapper/luks-root
  * > vgcreate qubes_dom0 /dev/mapper/luks-root
  * > lvcreate -L 8G -n swap qubes_dom0 
  
  You might want to read [8.2. Recommended system swap space] if you're not sure about swap space
  * > lvcreate -T -L 40G qubes_dom0/root-pool
  * > lvcreate -T -l +90%FREE qubes_dom0/vm-pool
  
  SSD would perform badly if all of the space is used, so we leave 10% of the total to maintain the best performance.
  * > lvcreate -V30G -T qubes_dom0/root-pool -n root-pool
  
  You should leave at least 10% in total of Thin Pool space so it could tell you if your drive will out of space.
  * > lvs
  
  To see how much space you have in the VM pool, and use it to create VM lv.
  * > lvcreate -V800G -T qubes_dom0/vm-pool -n vm
  
  _XFS_
  * > mkfs.xfs /dev/qubes_dom0/vm
  * > mkswap /dev/qubes_dom0/swap
  
  _EXT4_
  * > mkfs.ext4 /dev/qubes_dom0/vm
  * > mkswap /dev/qubes_dom0/swap
  
### BTRFS
* Create Root and Swap Partition.

  Swap Partition
  * > sgdisk -n 0:0:+8GiB -t 0:8200 /dev/nvme0n1

  Root Partition
  * > sgdisk -n 0:0:0 -t 0:8304 /dev/nvme0n1
  
* Create custom Luks configuration.
  * > cryptsetup -c serpent-xts-plain64 -h sha512 -s 512 -y -i 10000 luksFormat /dev/nvme0n1p1
  * > cryptsetup -c aes-xts-plain64 -h sha512 -s 512 -y -i 10000 luksFormat /dev/nvme0n1p2
  * > cryptsetup luksOpen /dev/nvme0n1p1 luks-root
  * > cryptsetup luksOpen /dev/nvme0n1p2 luks-swap
  * > mkfs.btrfs --csum blake2b -L qubes_dom0 -d single /dev/mapper/luks-root

  You can use another -csum (checksum) and may want to read this if you want to learn another [Checksum Algorithms]
  * > mkswap /dev/mapper/swap

### Proceed GUI Installation

* This is also a full video of this guide. 

[![qubes](upload://lYG6BYXuYMWf546gJuacm09aPDU.jpeg)](https://ileg.al/videos/qubes-custom.webm "qubes-custom")

_**Begin installation.**_

* After installation go back to tty2

  * > cp -r /usr/lib/grub/x86_64-efi /mnt/sysroot/boot/efi/EFI/qubes/
  * > chroot /mnt/sysroot/
  * > mount -oremount,ro /boot
  * > install -m0600 /dev/null /tmp/boot.tar
  * > tar -C /boot --acls --xattrs --one-file-system -cf /tmp/boot.tar .
  * > umount /boot/efi
  * > umount /boot

* Reformat Boot Partition
  * > cryptsetup -c twofish-xts-plain64 -h sha512 -s 512 -y -i 1 --use-random --type luks1 luksFormat /dev/sda1

* Create Alias
  
  uuidB = /boot partition

  uuidR = /root partition
  
  uuidS = swap partition

  * > uuidB="$(blkid -o value -s UUID /dev/sda1)"
  
  _XFS / EXT4_
  * > uuidR="$(blkid -o value -s UUID /dev/nvme0n1)"

  _BTRFS_
  * > uuidS="$(blkid -o value -s UUID /dev/nvme0n1p1)
  * > uuidR="$(blkid -o value -s UUID /dev/nvme0n1p2)"

* Reopen luks boot partition

  * > cryptsetup luksOpen /dev/sda1 luks-$uuidB

  _XFS_
  * > mkfs.xfs /dev/mapper/luks-$uuidB
  * > xfs_admin -U $uuidB /dev/mapper/luks-$uuidB
  
  _EXT4 / BTRFS_
  * > mkfs.ext2 -m0 -U $uuidB /dev/mapper/luks-$uuidB

* Configure fstab
  * > sed -i 's?UUID=QUBE[^ ]*?/dev/mapper/luks-'$uuidB'?g' /etc/fstab
  
  Replace QUBE with the First 4 UUID Numbers of /dev/sda1
  
  _XFS / EXT4_
  * > sed -i 's?/dev/qubes-dom0-root?/dev/mapper/luks-'$uuidR'?g' /etc/fstab

  _BTRFS_
  * > sed -i 's?UUID=QUBE[^ ]*?/dev/mapper/luks-'$uuidR'?g' /etc/fstab
  * > echo -e "/dev/mapper/luks-$uuidS none swap defaults 0 0" >> /etc/fstab

  Remount Boot and EFI partition
  * > mount -v /boot
  * > tar -C /boot --acls --xattrs -xf /tmp/boot.tar
  * > mount /dev/sda1 /boot/efi

* Configure keys
  * > mkdir -m0700 /etc/keys
  * > ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/root.key conv=excl,fsync )
  * > ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/boot.key conv=excl,fsync )

  _BTRFS also create swap key_
  * > ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/swap.key conv=excl,fsync )

* Configure LUKS for XFS / EXT4
  * > cryptsetup luksAddKey /dev/nvme0n1 /etc/keys/root.key
  * > cryptsetup luksAddKey /dev/sda1 /etc/keys/boot.key
  * > cryptsetup luksHeaderBackup /dev/nvme0n1 --header-backup-file header
  * > dd if=/header of=/dev/sda3 bs=16M count=1 status=progress

* Configure LUKS for BTRFS
  * > cryptsetup luksAddKey /dev/nvme0n1p2 /etc/keys/root.key
  * > cryptsetup luksAddKey /dev/nvme0n1p1 /etc/keys/swap.key
  * > cryptsetup luksAddKey /dev/sda1 /etc/keys/boot.key
  * > cryptsetup luksHeaderBackup /dev/nvme0n1p2 --header-backup-file root-header
  * > cryptsetup luksHeaderBackup /dev/nvme0n1p1 --header-backup-file swap-header
  * > dd if=/root-header of=/dev/sda3 bs=16M count=1 status=progress
  * > dd if=/swap-header of=/dev/sda4 bs=16M count=1 status=progress

* Remove unnecessary files
  * > shred -uvz /header
  * > shred -uvz /tmp/boot.tar

* Configure Crypttab

  _XFS / EXT4_
  * > echo -e “luks-$uuidR /dev/nvme0n1 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sda3\nluks-$uuidB UUID=$uuidB /etc/keys/boot.key luks,key-slot=1” > /etc/crypttab

  BTRFS
  * > echo -e “luks-$uuidR /dev/nvme0n1p2 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sda3\nluks-$uuidS /dev/nvme0n1p1 /etc/keys/swap.key luks,key-slot=1,header=/dev/sda4\nluks-$uuidB UUID=$uuidB /etc/keys/boot.key luks,key-slot=1” > /etc/crypttab

* Configure GRUB
  * > echo “GRUB_ENABLE_CRYPTODISK=y” >> /etc/default/grub
  * > grub2-mkconfig -o /boot/efi/EFI/qubes.cfg

* Rewrite uuid map and crypttab

  _XFS / EXT4_
  * > sed -i 's?block_uuid.map"?block_uuid.map"\necho “/dev/nvme0n1 '$uuidR'\n/dev/disk/by-uuid/'$uuidB' '$uuidB'" > “${initdir}/etc/block_uuid.map”?g' /usr/lib/dracut/modules.d/90crypt/module-setup.sh
  * > sed -i 's?$initdir/etc/crypttab?$initdir/etc/crypttab\necho “luks-'$uuidR' /dev/nvme0n1 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sda3\nluks-'$uuidB' UUID='$uuidB' /etc/keys/boot.key luks,key-slot=1” > $initdir/etc/crypttab?g' /usr/lib/dracut/modules.d/90crypt/module-setup.sh
  
  _BTRFS_
  * > sed -i 's?block_uuid.map"?block_uuid.map"\necho “/dev/nvme0n1p2 '$uuidR'\n/dev/nvme0n1p1 '$uuidS'\n/dev/disk/by-uuid/'$uuidB' '$uuidB'" > “${initdir}/etc/block_uuid.map”?g' /usr/lib/dracut/modules.d/90crypt/module-setup.sh
  * > sed -i 's?$initdir/etc/crypttab?$initdir/etc/crypttab\necho “luks-'$uuidR' /dev/nvme0n1p2 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sda3\nluks-'$uuidS' /dev/nvme0n1p1 /etc/keys/swap.key luks,discard,key-slot=1,header=/dev/sda4\nluks-'$uuidB' UUID='$uuidB' /etc/keys/boot.key luks,key-slot=1” > $initdir/etc/crypttab?g' /usr/lib/dracut/modules.d/90crypt/module-setup.sh

* Configure Dracut
  * > echo -e 'add_dracutmodules+=" crypt "\ninstall_items+=" /etc/keys/root.key /etc/keys/boot.key ”' > /etc/dracut.conf.d/qubes.conf
  * > dracut -vf /boot/initramfs-*
  * > exit
  * > umount /mnt/sysroot/boot/efi
  * > umount /mnt/sysroot/boot
  * > umount -l /mnt/sysroot
  * > umount -l /mnt/sysimage

  _XFS / EXT4_
  * > swapoff /dev/qubes_dom0/swap
  * > vgchange -a n qubes_dom0
  * > cryptsetup luksClose /dev/mapper/luks-root
  * > cryptsetup luksClose /dev/mapper/luks-*
  * > wipefs -a /dev/nvme0n1
  * > reboot

  _BTRFS_
  * > swapoff /dev/mapper/luks-swap
  * > cryptsetup luksClose /dev/mapper/luks-root
  * > cryptsetup luksClose /dev/mapper/luks-swap
  * > cryptsetup luksClose /dev/mapper/luks-*
  * > wipefs -a /dev/nvme0n1p1
  * > wipefs -a /dev/nvme0n1p2
  * > reboot

**Please remember that we do Detached Boot, so if you plan to use sys-usb (well you should), don't forget to edit the kernel parameter in the grub menu if you want to update kernel, and add `qubes_skip.autostart` to prevent sys-usb starting and detaching our /boot partition.**

[Playing with qubes]: https://forum.qubes-os.org/t/playing-with-qubes/11603

[Qubes OS Installation - Detached encrypted boot and header]: https://forum.qubes-os.org/t/qubes-os-installation-detached-encrypted-boot-and-header/6205

[8.2. Recommended system swap space]: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_storage_devices/getting-started-with-swap_managing-storage-devices

[Checksum Algorithms]: https://wiki.tnonline.net/w/Btrfs/Checksum_Algorithms