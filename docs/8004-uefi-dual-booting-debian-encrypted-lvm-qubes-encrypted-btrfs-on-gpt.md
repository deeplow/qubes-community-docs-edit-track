I got a new laptop with nothing on it. Debian has been my go to OS so far, but want to transition to Qubes(4.1 w/KDE) and while i test/learn/setup Qubes so i can continue working on my Debian and can have it as backup if i have issues with Qubes.

I have been doing a lot of research on this, but nothing i find is concrete or is conflicting or [requires Legacy/UEFI mix setup](https://micahflee.com/2014/04/dual-booting-qubes-and-ubuntu-with-encrypted-disks/).

My understanding of the setup process so far as per [Community/contents/docs/configuration/multiboot](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/multiboot.md) and https://micahflee.com/2014/04/dual-booting-qubes-and-ubuntu-with-encrypted-disks/ :

1. Install Debian first with `/boot` & `encrypted LVM`. But, `/boot` here has to be EFI since i'm installing on a brand new SSD on a UEFI system. 
2. Then install Qubes on the remaining free space. But then where does the `/boot` for Qubes go other thant the same `/boot` that was created for Debian? And it is advised against to have them both on the same `/boot` partition.

Laptop specs:
- Intel Iris Xe Graphics G7
- Intel Core i7-1165G7
- 32 GB DDR4-3200 Samsung
- 2TB 510 Seagate Firecuda

I am confused and would greatly appreciate if anyone can help lay out a clear path to achieve this.

Thank you