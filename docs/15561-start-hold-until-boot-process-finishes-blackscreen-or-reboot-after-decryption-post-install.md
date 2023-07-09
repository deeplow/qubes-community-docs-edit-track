After couple of days of troubleshooting and trying everything that the Qubes Forum and documentation had to offer, I finally found the kinda trivial solution (at least in my case) that fixes the following problem which some users face when installing qubes:

After installing Qubes and completing the initial setup, the machine gets a blackscreen / graphical weird looking screen and shuts down / reboots following the LUKS decryption.

The process stops at "start hold until boot process finishes..." (LightDM)

The GUI troubleshooting section in the documentation suggests to add 'efi=no-rs' to the xen.cfg file, but this (in my case) didn't work.

In my case, just a PCI attached device (done automatically with the initial setup?) to sys-net was the problem.

This steps fixed it for me:
1. Install Qubes normally on your preferred machine, but on an external drive
2. If you face the issue, boot Qubes (installed on the external drive) on another machine
3. Deactivate "start automatically on boot" for sys-net
4. Remove any PCI devices from sys-net
5. Shutdown and boot again on your preferred machine

Now this particular Qubes installation should work on your machine.

In my case, the cause of the problem was the Wifi card, so you may want to use another one than your current one for Qubes Wifi access.

(I don't know if this has been mentioned so far anywhere or not, but I just thought it may be helpful for future users who face the issue and maybe find this post via Google, as I couldn't find any anwser that worked for me, so maybe as an addition to all the other things you could try in case of this issue)

For keywords:
qubes post installation reboot loop
qubes post installation black screen
qubes post installation decryption not loading
qubes start hold until boot process finishes
qubes lightdm hold until boot process finishes