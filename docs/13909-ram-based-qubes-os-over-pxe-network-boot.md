This is a sub-topic fork of @alzer89's [Automated Qubes OS Installation using Kickstart and/or PXE Network Boot](https://forum.qubes-os.org/t/automated-qubes-os-installation-using-kickstart-and-or-pxe-network-boot/12963), focused on creating a repeatable guide to PXE Network Boot a RAM-based Qubes OS.

Basic concept: Your Qubes OS installation sits on another computer with the PXE server software. You can then have as many client computers as you want PXE network boot from this RAM-based Qubes OS using only their network connection and no drives needed to boot from. Your client computers reboot to a 100% clean Qubes OS state each time. Scales to many client computers at once.

RAM-based Qubes OS over PXE Network Boot is very useful for:

- Running further stateless endpoint computers without storage drives in them.

- Anti-forensics. Nothing stored on endpoint computers, except firmware of the hardware parts. No drives necessary at all.

- Disposable Qubes OS. Just easily reboot to instantly make and boot a new clean install of Qubes OS many times per day.

- Quick centralized management & deployment of Qubes OS configurations/updates to multiple endpoint computers.

Interesting initial conversations and a general Qubes OS PXE installer implementation in the general topic thread mentioned above.

Note: If you'd alternatively just like to run a RAM-based Qubes OS from a normal boot drive, then this is already available using @xuy's [Qubes in tmpfs](https://forum.qubes-os.org/t/qubes-in-tmpfs/11127).