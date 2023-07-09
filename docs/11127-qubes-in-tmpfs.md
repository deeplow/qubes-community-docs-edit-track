You can use your QubesOS 𝚜𝚝𝚊𝚝𝚎𝚕𝚎𝚜𝚜 just like TailsOS, with **persistent storage** for VMs. That is pretty simple! It takes 6Gb of extra 𝚁𝙰𝙼 (for store root filesystem files).

## The steeps:

1. Install QubesOS, boot to it and make base configuration: screen resolution, keyboard layout, etc.

2. Edit kernel parameters variables at grub settings file `/etc/default/grub`:

```
GRUB_CMDLINE_LINUX="... 𝚛𝚍.𝚋𝚛𝚎𝚊𝚔"
GRUB_CMDLINE_XEN_DEFAULT="... dom0_mem=max:10240M ..."
```
*The 𝚛𝚍𝚋𝚛𝚎𝚊𝚔 option - drop to a shell at the end (see `𝚖𝚊𝚗 𝚍𝚛𝚊𝚌𝚞𝚝`).*

3. Generate grub2 config and reboot PC:

```
sudo grub2-mkconfig | sudo tee /boot/efi/EFI/grub.cfg
reboot
```

4. "𝙿𝚛𝚎𝚜𝚜 𝙴𝚗𝚝𝚎𝚛 𝚏𝚘𝚛 𝚖𝚊𝚒𝚗𝚝𝚒𝚗𝚊𝚗𝚌𝚎", then copy files from SSD to 𝚁𝙰𝙼:

```
umount /sysroot
mkdir /mnt
mount /dev/mapper/qubes_dom0-root /mnt
mount -t 𝚝𝚖𝚙𝚏𝚜 -o size=100% none /sysroot
cp -a /mnt/* /sysroot
```

- Press Ctrl-D to continue QubesOS boot-up.

   **Hooya! Your 𝚀𝚞𝚋𝚎𝚜𝙾𝚂 𝚠𝚘𝚛𝚔𝚒𝚗𝚐 𝚒𝚗 𝚁𝙰𝙼.**

*You can create a 𝚍𝚛𝚊𝚌𝚞𝚝 module to automate the steep four, if that makes sense.*

## Then the volume

1. Mount a special 𝚑𝚒𝚍𝚍𝚎𝚗 partition to /opt

2. Create qubes VMs files at varlibqubes pool

```
qvm-create -P varlibqubes --class TemplateVM --label black debian-10-pool
qvm-create -P varlibqubes --template debian-10-pool --label blue darknet-i2p
```

3. Change the path via symlinks to access the VMs:

```
sudo rm -Rf /var/lib/qubes/vm-templates/ ; ln -s /opt/vm-templates/ /var/lib/qubes/
sudo rm -Rf /var/lib/qubes/appvms/ ; ln -s /opt/appvms /var/lib/qubes/
```
* In the /opt directory should be a VM files created earlier, with identical to current VMs names.

## You should like to configure the system

1. Add bash aliases

```
echo '
alias qvm-clone="qvm-clone -P varlibqubes"
alias qvm-create="qvm-create -P varlibqubes"
' >> $HOME/.bashrc
```

2. Configure AppVMs


```
lspci
qvm-pci attach --persistent --verbose vmname dom0:06_00.0

qvm-prefs --set vmname ip 10.137.0.81
qvm-prefs --set vmname netvm none
qvm-prefs --set vmname provides_network true
qvm-prefs --set vmname memory 800
qvm-prefs --set vmname maxmem 8000
```

Good luck!

*NOTE: Install QubesOS updates from normal persistent mode (not from 𝚁𝙰𝙼 mode).*

## References
1. Linux - Load your root partition to 𝚁𝙰𝙼 and boot it - Tutorials - reboot.pro:
_https://reboot.pro/topic/14547-linux-load-your-root-partition-to-ram-and-boot-it/ 
_https://web.archive.org/web/20220224235759/https://reboot.pro/topic/14547-linux-load-your-root-partition-to-ram-and-boot-it/
2. 𝙳𝚛𝚊𝚌𝚞𝚝 Wiki: _https://dracut.wiki.kernel.org/index.php/Main_Page
3. Deniable encryption · Issue #2402 · QubesOS/qubes-issues · GitHub: _https://github.com/QubesOS/qubes-issues/issues/2402
4. AMD Memory Encryption — The Linux Kernel documentation: _https://www.kernel.org/doc/html/v5.8/x86/amd-memory-encryption.html