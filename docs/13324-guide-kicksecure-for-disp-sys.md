**Introduction:**

I will explain how I created a disposable sys-usb, sys-net, sys-firewall off a debian-11 minimal template with Kicksecure and other hardening features from the Kicksecure checklist.   

**Assumptions:**

* Qubes R4.1.1
* Comfortable with bash
* This guide wasn't meant to be introduction to kicksecure and the features installed. It is expected you have read up on kicksecure and understand, LKRG, tirdad, malloc hardening and appamor. There are various settings you have for all of these. This is the setup I'm happy with and works for me. You may need to change it to suit your setup.
* Using the latest debian bullseye-backports kernel for the LKRG and tirdad. You could use the standard kernel and headers in bullseye but its rather old and I haven't tested it. It's  older than the standard Qubes kernels used in Dom0 and VMs so I opted for a newer one.

**Recommended reading:**

* https://forum.qubes-os.org/t/automate-debian-minimal-based-template-creation
* https://forum.qubes-os.org/t/debian-10-minimal-configuration/2603/12
* https://www.qubes-os.org/doc/managing-vm-kernels/#installing-kernel-in-debian-vm
* https://www.kicksecure.com/wiki/System_Hardening_Checklist
* https://madaidans-insecurities.github.io/guides/linux-hardening.html#mac
* https://www.kicksecure.com/wiki/Linux_Kernel_Runtime_Guard_LKRG/Qubes
* https://www.kicksecure.com/wiki/Hardened_Malloc
* https://github.com/Kicksecure/tirdad
* https://www.kicksecure.com/wiki/AppArmor
* https://www.qubes-os.org/doc/disposable-customization/#create-custom-sys-net-sys-firewall-and-sys-usb-disposables
* https://www.qubes-os.org/doc/usb-qubes/

**Requirements:**

* Using Dom0 for generating templates
* Using @Sven method for creating templates ( thanks Sven)
* Using a USB qube for deb-11-sysusb

**Note:**

You are adding another repository with a number of software packages to be installed. You need to consider the risks associated with this, and consider how well you trust the sources of the software. Like always if you have the ability and time it is recommended to review the code before using it.

Kicksecure is new and I haven't done extensive testing, so I can't guarantee this won't break anything.  That being said i've had no problems since I've set it up.

****Creating Debian minimal templates****

This is nothing more than @sven method. Look [here](https://forum.qubes-os.org/t/automate-debian-minimal-based-template-creation/11421) for more details.

**Note:** I strongly suggest reading through that guide and understanding it. I've attached my deb-11-min template. As you can see it has parts commented out. These sections won't work unless you have followed the guide for dark themes. 

**Steps:**

1. Create the deb-11-min template in a folder on your dom0. I have mine in ~/scripts/

````bash
#!/bin/bash

SOURCE_TEMPLATE=debian-11-minimal
TARGET_TEMPLATE=deb-11-min

# download, clone 
# I commented out remove as it will be used many times.
# Up to you if you want to remove it after each template is generated.
qvm-template install $SOURCE_TEMPLATE 
qvm-clone $SOURCE_TEMPLATE $TARGET_TEMPLATE
#qvm-remove -f $SOURCE_TEMPLATE

qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /home/user/QubesIncoming"

# copy themes ( I'm using dark themes, i use both Yaru-dark and Arc-Dark
# you will need to have them installed in dom0 if you want to use.
#Commented out for that reason. If you want dark themes 

#qvm-copy-to-vm $TARGET_TEMPLATE /usr/share/themes/Yaru*
#qvm-copy-to-vm $TARGET_TEMPLATE /usr/share/themes/Arc*

#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /usr/share/themes/Yaru*"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "mv /home/user/QubesIncoming/dom0/Yaru* /usr/share/themes/"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "mv /home/user/QubesIncoming/dom0/Arc* /usr/share/themes/"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /home/user/QubesIncoming"

# copy icons (i'm using themes, if you want to use dark themes look at the qubes post and 
# uncomment

#qvm-copy-to-vm $TARGET_TEMPLATE /usr/share/icons/Yaru

#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /usr/share/icons/Yaru*"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "mv /home/user/QubesIncoming/dom0/Yaru /usr/share/icons/"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /home/user/QubesIncoming"

# copy fonts

#qvm-copy-to-vm $TARGET_TEMPLATE /usr/share/fonts/ubuntu

#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /usr/share/fonts/truetype/ubuntu"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "mv /home/user/QubesIncoming/dom0/ubuntu /usr/share/fonts/truetype/"
#qvm-run --pass-io -u root $TARGET_TEMPLATE "rm -Rf /home/user/QubesIncoming"

# setup /etc/X11/Xresources/x11-common

qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "Xft.dpi: 96" >> /etc/X11/Xresources/x11-common'
qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "XTerm*faceName: Ubuntu Mono" >> /etc/X11/Xresources/x11-common'
qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "XTerm*faceSize: 12" >> /etc/X11/Xresources/x11-common'
qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "XTerm*background: #300a24" >> /etc/X11/Xresources/x11-common'
qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "XTerm*foreground: linen" >> /etc/X11/Xresources/x11-common'
qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "XTerm*selectToClipboard: true" >> /etc/X11/Xresources/x11-common'

# install basic packages

qvm-run --pass-io -u root $TARGET_TEMPLATE "apt update && apt full-upgrade -y"
qvm-run --pass-io -u root $TARGET_TEMPLATE "apt install qubes-core-agent-passwordless-root qubes-app-shutdown-idle -y"

# set Xterm as default

qvm-run --pass-io -u root $TARGET_TEMPLATE "update-alternatives --set x-terminal-emulator /usr/bin/xterm"

# copy GTK configs and desktop shortcuts into /etc/skel
# you need to have these file in your Dom0. I'm using them for
# to have consistency between my themes. I've commeted out. If you want to do this look 
# at dark themes guide on the qubes forum.

#qvm-copy-to-vm $TARGET_TEMPLATE ~/scripts/.gtkrc-2.0
#qvm-copy-to-vm $TARGET_TEMPLATE ~/scripts/settings.ini
#qvm-copy-to-vm $TARGET_TEMPLATE ~/scripts/qvm-open-in-vm-desktop.desktop

#qvm-run --pass-io $TARGET_TEMPLATE "sudo mkdir -p /etc/skel/.config/gtk-3.0"
#qvm-run --pass-io $TARGET_TEMPLATE "sudo mkdir -p /etc/skel/.local/share/applications"

#qvm-run --pass-io $TARGET_TEMPLATE "sudo mv ~/QubesIncoming/dom0/.gtkrc-2.0 /etc/skel"
#qvm-run --pass-io $TARGET_TEMPLATE "sudo mv ~/QubesIncoming/dom0/settings.ini /etc/skel/.config/gtk-3.0"
#qvm-run --pass-io $TARGET_TEMPLATE "sudo mv ~/QubesIncoming/dom0/qvm-open-in-vm-desktop.desktop /etc/skel/.local/share/applications"
#qvm-run --pass-io $TARGET_TEMPLATE "rm -Rf ~/QubesIncoming"

#qvm-run --pass-io -u root $TARGET_TEMPLATE 'echo "xdg-settings set default-web-browser #qvm-open-in-vm-desktop.desktop" >> /etc/skel/.bashrc'

# shutdown
qvm-shutdown --wait $TARGET_TEMPLATE

qvm-prefs $TARGET_TEMPLATE memory 400
qvm-prefs $TARGET_TEMPLATE maxmem 0
````


2. Create add-feature-kicksecure
````bash
#!/bin/bash
# kicksecure.sh
# Distro morphing debian-11-minimal to Kicksecure
# URL: https://www.whonix.org/wiki/Kicksecure/Debian

qvm-run --pass-io --no-gui --user=root $1 'apt-get -y update && apt-get dist-upgrade'
# Some packages needed for kicksecure to install
qvm-run --pass-io --no-gui --user=root $1 'apt-get -y install zenity pulseaudio-qubes qubes-menus qubes-core-agent-networking qubes-mgmt-salt-vm-connector  grub2 qubes-kernel-vm-support'
# The next steps are straight from the kicksecure website but in a bash script
# This copies over their key and created the apt repo for kicksecure then installs kicksecure-cli
qvm-run --pass-io --no-gui --user=root $1 'apt-get -y install --no-install-recommends sudo adduser'
qvm-run --pass-io --no-gui --user=root $1 'addgroup -system console && adduser user console && adduser user sudo'
qvm-run --pass-io --no-gui --user=root $1 'apt-get -y install --no-install-recommends curl'
qvm-run --pass-io --no-gui --user=root $1 'curl --proxy http://127.0.0.1:8082/ --output derivative.asc https://www.kicksecure.com/derivative.asc'
qvm-run --pass-io --no-gui --user=root $1 'cp derivative.asc /usr/share/keyrings/derivative.asc'
qvm-run --pass-io --no-gui --user=root $1 'echo "deb [signed-by=/usr/share/keyrings/derivative.asc] https://deb.kicksecure.com bullseye main contrib non-free" | sudo tee /etc/apt/sources.list.d/derivative.list'
qvm-run --pass-io --no-gui --user=root $1 'apt-get update'
qvm-run --pass-io --no-gui --user=root $1 'apt-get dist-upgrade'
qvm-run --pass-io --no-gui --user=root $1 'apt-get -y install --no-install-recommends kicksecure-qubes-cli'
qvm-run --pass-io --no-gui --user=root $1 'mv /etc/apt/sources.list ~/'
qvm-run --pass-io --no-gui --user=root $1 'touch /etc/apt/sources.list'
# Installing latest kernel to be used by LKRG triad and other kernel hardening mods
qvm-run --pass-io --no-gui --user=root $1 'apt-get -t bullseye-backports -y --no-install-recommends install linux-image-amd64 linux-headers-amd64'
qvm-run --pass-io --no-gui --user=root $1 'grub-install /dev/xvda'
````
3. Create add-feature-sysfirewall
````bash
#!/bin/bash

# Adding sys-firewall  support

echo +++ installing sys-firewall packages into  $1
qvm-run --pass-io -u root $1 "apt install --no-install-recommends qubes-core-agent-networking qubes-core-agent-dom0-updates -y"
````
4. Creating the sys-firewall template
````bash
#!/bin/bash

 SOURCE_TEMPLATE=deb-11-min
 TARGET_TEMPLATE=deb-11-sysfirewall

 #clone
 qvm-clone $SOURCE_TEMPLATE $TARGET_TEMPLATE

 #add features

 $(pwd)/add-feature-sysfirewall          $TARGET_TEMPLATE
 $(pwd)/add-feature-kicksecure          $TARGET_TEMPLATE
 #shutdown
 qvm-shutdown --wait $TARGET_TEMPLATE
 qvm-prefs $TARGET_TEMPLATE memory 400
 qvm-prefs $TARGET_TEMPLATE maxmem 4000

````
5. After you have created those three files.  You need to make them executable `sudo chmod +x file`
6. run `./deb-11-sysfirewall` this will create a deb-11-sysfirewall template that installs the features in the add-feature-sysfirewall and add-feature-kicksecure. 

 **Install LKRG, tirdad, malloc and enabling apparmor** 

1. We are using the Linux VM kernel from bullseye-backports this requires installing pvgrub2-pvh in dom0 as the deb-11-sysfirewall is PVH virtualisation.  `sudo qubes-dom0-update grub2-xenpvh`
2. Go to Qubes Manager and find the deb-11-sysfirewall. Click on settings -> Advanced and change the kernel to pvgrub2-pvh, Then start the deb-11-sysfirewall. This will now boot with the latest kernel
3.  Open a xterm on deb-11-sysfirewall then check you are on the latest kernel `uname -a`
4. Install Linux Kernel runtime guard (LKRG) `sudo apt install --no-install-recommends lkrg-dkms`
5. Install tirdad `sudo apt-get install tirdad`
5. restart deb-11-sysfirewall 
6. Check LKRG  and tirdad is installed by `sudo dkms status`
7. Install hardened Malloc `echo "/usr/lib/libhardened_malloc.so/libhardened_malloc.so" | sudo tee /etc/ld.so.preload`
8.  Enabling apparmor in Dom0. `qvm-prefs -s deb-11-sysfirewall kernelopts "apparmor=1 security=apparmor"`

These steps are the same for sysnet and sys-usb. However, sys-net and sys-usb should be set to HVM due to attachments of devices (ethernet and usb controller). Therefore you will have to make a slight change to step 2. Instead of pvgrub2-pvh you will need to put (none).

**add-feature-sys-net**
````bash
#!/bin/bash

# Adding sys-net support

echo +++ installing sys-net packages into  $1
# Note I have a Intel iwl wifi adapter if you don't you can remove this.
qvm-run --pass-io -u root $1 "apt install --no-install-recommends qubes-core-agent-networking qubes-core-agent-network-manager gnome-keyring firmware-iwlwifi -y"

````
**add-feature-sys-usb**
````bash
#!/bin/bash

# Adding sys-usb support

echo +++ installing sys-usb packages into  $1
qvm-run --pass-io -u root $1 "apt install --no-install-recommends qubes-usb-proxy qubes-input-proxy-sender qubes-core-agent-nautilus nautilus zenity gnome-keyring policykit-1 libblockdev-crypto2 ntfs-3g -y"
````
**deb-11-sysusb**
````bash
#!/bin/bash

 SOURCE_TEMPLATE=deb-11-min
 TARGET_TEMPLATE=deb-11-sysusb

 #clone
 qvm-clone $SOURCE_TEMPLATE $TARGET_TEMPLATE

 #add features

 $(pwd)/add-feature-sysusb          $TARGET_TEMPLATE

 #shutdown
 qvm-shutdown --wait $TARGET_TEMPLATE
 qvm-prefs $TARGET_TEMPLATE memory 400
 qvm-prefs $TARGET_TEMPLATE maxmem 600
````
**deb-11-sysnet**
````bash
#!/bin/bash

 SOURCE_TEMPLATE=deb-11-min
 TARGET_TEMPLATE=deb-11-sysnet

 #clone
 qvm-clone $SOURCE_TEMPLATE $TARGET_TEMPLATE

 #add features

 $(pwd)/add-feature-sysnet          $TARGET_TEMPLATE

 #shutdown
 qvm-shutdown --wait $TARGET_TEMPLATE
 qvm-prefs $TARGET_TEMPLATE memory 400
 qvm-prefs $TARGET_TEMPLATE maxmem 600

````

**Creating DISP-Sys*** 

1. the template are currently just that. Templates with kicksecure installed and setup. You still need to create disposable templates from them. I will expand on section later but the details for doing this in already at https://www.qubes-os.org/doc/disposable-customization/#create-custom-sys-net-sys-firewall-and-sys-usb-disposables
You will need to follow that but use the deb-11-sysfirewall, deb-11-sysusb, deb-11-sysnet for these.

**Known Issues:**