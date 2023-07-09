Continuing the discussion from [Qubes OS Installation - Detached encrypted boot and header](https://forum.qubes-os.org/t/qubes-os-installation-detached-encrypted-boot-and-header/6205):

In above thread I use xfs with uefi + gpt.
In here I will using mbr + bios with btrfs blake2 checksum.

Keep in mind that below are disk i used in the tutorial, you can use 2 flashdrive (1 boot, 1 header) + 1 hdd or whatever you want.

and btw I don't detach swap partition, well i think you should. Do write out to /dev/sdb3 if you want

> Take this as additional challenge :) 

I use different chipper for each partition; root with aes-xts, swap with serpent-xts and boot with twofish-xts, you can go with aes-xts for better performance.

/dev/sda = system
/dev/sdb = flashdrive

Don't forget to change boot order, so flashdrive is booting first.

*Please watch out any space, slash, periode in command issue / files IT REALLY MATTER*

---

* After booting into installation in language section, press ctrl + alt + f2

—# WARNING CONFIRM YOUR DISK FIRST BEFORE EXECUTING COMMAND

[anaconda /] dd if=/dev/urandom of=/dev/sda bs=1M status=progress
[anaconda /] dd if=/dev/urandom of=/dev/sdb bs=1M status=progress

Using /dev/urandom will take longer than /dev/zero but more secure.


[anaconda /] fdisk /dev/sda
---# root partition
n
p
1
(enter)
+36GiB

---# swap partition
n
p
2
(enter)
(enter) #4GiB for swap

w

---

* Create 2 or 3 partition in usb drive.

[anaconda /] fdisk /dev/sdb
—# boot partition
n
p
1
(enter)
+1GiB

—# header partition
n
p
2
(enter)
+30MiB

---# you can create 3 partition for additional use (whatever it is) / just use 2 partition
n
p
3
(enter)
(enter)

w

---

My block device after partitioning : 

![testing bios-2021-10-26-01-42-57|666x500](upload://lkXt5DhcYsBltRggghm1HCJfrTL.png)

---

—# I use iter time 1 for speeding up decrypt process you should increase it in real installation, see [5.13 ](https://gitlab.com/cryptsetup/cryptsetup/-/wikis/FrequentlyAskedQuestions#5-security-aspects) for details.
[anaconda /] cryptsetup -c aes-xts-plain64 -h sha512 -s 512 -y -i 1 --use-random luksFormat /dev/sda1
[luks prompt /] YES
[luks prompt /] (enter password)
[luks prompt /] (verify password)
[anaconda /] cryptsetup -c serpent-xts-plain64 -h sha512 -s 512 -y -i 1 --use-random luksFormat /dev/sda2
[luks prompt /] YES
[luks prompt /] (enter password)
[luks prompt /] (verify password)
[anaconda /] cryptsetup luksOpen /dev/sda1 root
[luks prompt /] (enter password)
[anaconda /] cryptsetup luksOpen /dev/sda2 swap
[luks prompt /] (enter password)

[anaconda /] mkfs.btrfs --csum blake2b -L qubes_dom0 -d single /dev/mapper/luksroot
[anaconda /] mkswap /dev/mapper/swap

![testing bios-2021-10-26-01-46-52|666x500](upload://utHweFjR9kIf1V36TGjJiduRAd1.png)

---

- Back to gui with ctrl + alt + f6.
- Choose language, timezone, user, and lastly storage.
- Click refresh on bottom right and rescan disk.
- Select disk sda and sdb, storage configuration is Advanced Custom (Blivet-GUI) click done.

![testing bios-2021-10-26-01-31-12|666x500](upload://3NcbigdsTB9Zppc5C9XxmFdtrPg.png)

---# /dev/sda
- Right click qubes_dom0 > new > name = root, mountpoiont = /

---# /dev/sdb
- Right click on sdb1 > edit > format to ext2 / ext4 and mountpoint to /boot leave name to none.

---

- Click done, and this is the Summary of Changes

![testing bios-2021-10-26-01-50-10|666x500](upload://hVM84pxoM9DztipIQkkVOdCci00.png)

- Click done and begin installation.
- After completion, switch back to shell with ctrl + alt + f2

---

My block device after installing : 

![testing bios-2021-10-26-01-57-33|666x500](upload://tl470ewBfx9RajOjtkCgsTuVIb.png)

---

[anaconda /] chroot /mnt/sysroot/
[anaconda /] mount -oremount,ro /boot
[anaconda /] install -m0600 /dev/null /tmp/boot.tar
[anaconda /] tar -C /boot --acls --xattrs --one-file-system -cf /tmp/boot.tar .
[anaconda /] umount /boot
—# WARNING CONFIRM YOUR DISK FIRST BEFORE EXECUTING COMMAND
[anaconda /] dd if=/dev/urandom of=/dev/sdb1 bs=1M
[anaconda /] cryptsetup -c twofish-xts-plain64 -h sha512 -s 512 -y -i 1 --use-random --type luks1 luksFormat /dev/sdb1
[luks prompt /] YES
[luks prompt /] (enter password)
[luks prompt /] (verify password)
---# 
[anaconda /] uuidR="$(blkid -o value -s UUID /dev/sda1)" # root device
[anaconda /] uuidB="$(blkid -o value -s UUID /dev/sdb1)" # boot device
[anaconda /] uuidS="$(blkid -o value -s UUID /dev/sda2)" # swap device
[anaconda /] cryptsetup luksOpen /dev/sdb1 luks-$uuidB
[anaconda /] mkfs.ext2 -m0 -U $uuidB /dev/mapper/luks-$uuidB

---

—# Configure fstab
- Change UUID=…on boot and root line to /dev/mapper/luks-(your $uuidR and $uuidB) 
- Add swap and leave the rest to default value

![testing bios-2021-10-26-02-21-11|666x500](upload://zy7TkKZAsNJ1KMtq3vSPPXH77M7.png)

---

[anaconda /] mount -v /boot
[anaconda /] tar -C /boot --acls --xattrs -xf /tmp/boot.tar

---# Configure grub
[anaconda /] echo “GRUB_ENABLE_CRYPTODISK=y” >> /etc/default/grub

in GRUB_CMDLINE_LINUX delete all of rd.luks.................... then add cryptdevice=$uuidB:luks-$uuidB in my case this is my final grub_cmdline_linux line : 

```
GRUB_CMDLINE_LINUX="cryptdevice=aa7332a5-e4ac-442c-9328-cdbd4a0b42e8:luks-aa7332a5-e4ac-442c-9328-cdbd4a0b42e8 plymouth.ignore-serial-consoles i915.alpha_support=1 rd.driver.pre=btrfs rhgb quiet"
```

—# create luks keys so we dont have to enter any password after grub
[anaconda /] mkdir -m0700 /etc/keys
[anaconda /] ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/root.key conv=excl,fsync )
[anaconda /] ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/boot.key conv=excl,fsync )
[anaconda /] ( umask 0077 && dd if=/dev/urandom bs=1 count=64 of=/etc/keys/swap.key conv=excl,fsync )
[anaconda /] cryptsetup luksAddKey /dev/sda1 /etc/keys/root.key
[luks prompt /] (system password)
[anaconda /] cryptsetup luksAddKey /dev/sda2 /etc/keys/swap.key
[luks prompt /] (swap password)
[anaconda /] cryptsetup luksAddKey /dev/sdb1 /etc/keys/boot.key
[luks prompt /] (boot password)
[anaconda /] cryptsetup luksHeaderBackup /dev/sda1 --header-backup-file header
—# WARNING CONFIRM YOUR DISK FIRST BEFORE EXECUTING COMMAND
[anaconda /] dd if=/header of=/dev/sdb2 bs=16M count=1 status=progress
[anaconda /] shred -uvz /header
[anaconda /] shred -uvz /tmp/boot.tar

—# Configure crypttab
[anaconda /] echo -e “luks-$uuidR /dev/sda1 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sdb2 \nluks-$uuidS UUID=$uuidS /etc/keys/swap.key luks,key-slot=1 \nluks-$uuidB UUID=$uuidB /etc/keys/boot.key luks,key-slot=1” > /etc/crypttab

![testing bios-2021-10-26-02-57-00|666x500](upload://6DEDf4b50bEZhhTsJcQkLcxnwyg.png)

--- 

---# Configure dracut
[anaconda /] echo -e “add_dracutmodules+=\" crypt \" \ninstall_items+=\" /etc/keys/*.key \"" > /etc/dracut.conf.d/misc.conf

[anaconda /] vi /usr/lib/dracut/modules.d/90crypt/module-setup.sh

—# write a persistence device at /etc/block_uuid.map in generated initramfs
echo “/dev/sda1 $uuidR
/dev/disk/by-uuid/$uuidB $uuidB
/dev/disk/by-uuid/$uuidS $uuidS” > “${initdir}/etc/block_uuid.map”

![testing bios-2021-10-26-03-15-17|666x500](upload://eH0IyF7FuYMCuoQWfosRMkWUGYD.png)

—# write a persistence device at /etc/crypttab in generated initramfs (have try inject /etc/crypttab into initramfs but it doesn't match, so we'll rewrite again)

echo “luks-$uuidR /dev/sda1 /etc/keys/root.key luks,discard,key-slot=1,header=/dev/sdb2
luks-$uuidB UUID=$uuidB /etc/keys/boot.key luks,key-slot=1
luks-$uuidS UUID=$uuidS /etc/keys/swap.key luks,key-slot=1” > $initdir/etc/crypttab

![testing bios-2021-10-26-03-48-11|666x500](upload://6U52fj7aKj5gAZ4hBsUA0FWFU2r.png)

---

[anaconda /] grub2-install --recheck /dev/sdb
[anaconda /] grub2-mkconfig -o /boot/grub2/grub.cfg
[anaconda /] dracut -v -f /boot/initramfs-*
[anaconda /] exit
[anaconda /] umount /mnt/sysroot/boot
[anaconda /] umount -l /mnt/sysroot
[anaconda /] umount -l /mnt/sysimage
[anaconda /] swapoff /dev/mapper/luksswap
[anaconda /] cryptsetup luksClose /dev/mapper/luksroot
[anaconda /] cryptsetup luksClose /dev/mapper/luks-$uuidB
[anaconda /] cryptsetup luksClose /dev/mapper/luksswap
[anaconda /] cryptsetup luksErase /dev/sda1
[luks prompt /] YES
[anaconda /] wipefs -a /dev/sda1

---

My block device after configure everything : 

![testing bios-2021-10-26-03-54-35|666x500](upload://85fNI2NpcDZDJfPFnDsW70810dY.png)

[anaconda /] reboot

---

---# Screenshot

![testing bios-2021-10-27-02-12-02|690x383](upload://jTn2RQSbO98yeCdksuyRTPbeRj2.png)

![testing bios-2021-10-27-01-36-52|666x500](upload://4qHq2Oh2eJHQtDWlhqLXBdcRVK5.png)

![testing bios-2021-10-27-01-47-23|666x500](upload://sKZmmCWjDHESBWJUNRwmZkS3LZz.png)

![testing bios-2021-10-27-01-52-57|666x500](upload://9gMk2yvTx8ifwTQexJu1JhwUx1b.png)

After update, everything still works.

![testing bios-2021-10-27-02-14-29|666x500](upload://4zq7a8UJ2Z7ZJMaou5bsRhmyXcg.png)