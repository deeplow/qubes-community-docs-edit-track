Continuing the discussion from [Automate debian-minimal based template creation](https://forum.qubes-os.org/t/automate-debian-minimal-based-template-creation/11421/60):

# Betterbird
[details="Qubes OS - minimal installation"]

**Official installation instructions:** : [Betterbird Downloads](https://www.betterbird.eu/downloads/index.php)
**Installation type**: Linux Archive (*.tar.bz2)
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **ibxtst6** : unknown
* **llibpci3**: unknown
* **libbotan-2-17** : unknown
* **libdbus-glib-1-2** : unknown
* **libevent-2.1-7** : unknown
* **libtspi1** : TPM hardware, key and hash management [Package description](https://packages.debian.org/buster/libtspi1)
* **libgpgme11** : for GPG integration
* **bzip2** : unpacking download file

**Comments** : bzip2 can be removed afterwards since it is only required to unpack the installation bzip tar.

The archive have to be unpack into */opt*.

A desktop shortcut can be added in */usr/share/applications*

Optionally, you may want to use [split GPG](https://www.qubes-os.org/doc/split-gpg/) for Betterbird.

Betterbird is a fine-tuned version of *Mozilla Thunderbird*. Here is an [feature overview](https://www.betterbird.eu/index.html#featuretable). 

source: [Qubes Community post by Sven](https://forum.qubes-os.org/t/betterbird/13899?u=whoami).

[/details]



# KeePassXC (with Yubikey)

[details="Qubes OS - minimal installation"]

**Official installation instructions:** : apt install keepassxc
**Installation type**: included in debian standard
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **policykit-1** : required for YubiKey Challenger Response
* **xserver-xorg-input-libinput** : required for YubiKey static password
* **qubes-usb-proxy** : to connect the USB qube (sys-usb, usb-hub etc.) to this AppVM

UI settings (not mandatory) to make KeePassXC looks like the system theme
* **qt5-style-plugins**
* **gtk2-engines-murrine**
* **QT_QPA_PLATFORMTHEME=gtk2**

**Comments** : It is not mandatory but highly recommended to install KeePassXC on a **network off** AppVM (vault, secrets etc.). This AppVM is also mostly used for [split-GPG](https://www.qubes-os.org/doc/split-gpg/) and [split-SSH](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/split-ssh.md). This setup has been tested with Yubikey, it should also work with other hardware token keys (Challenger Response / hmac-sha1 method).

See also https://keepassxc.org/docs/#faq-yubikey-2fa

[/details]



# LibreOffice
[details="Qubes OS - minimal installation"]

**Official installation instructions:** : 
**Installation type**: 
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **xxx** : yyy
* **xxx** : yyy

**Comments** : …

[/details]


# Signal, Session, Element ...

[details="Qubes OS - minimal installation"]
**Official installation instructions:** :

 [Signal - Download for Linux](https://signal.org/en/download/)

[Session - Download for Linux](https://deb.oxen.io/)

[Element - Download for Linux](https://element.io/download#linux)

**Installation type**: apt repository (requires gpg key)
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **curl** : *required to download the gpg key for the apt repository*

  [details="Remark"]
  There are many ways to download the apt key.
  * You can either use *wget* or *curl*. Both do the download but have a different syntax. It is recommended to use the tool which is used in the official installation instruction.
  * If you are concerned about your security or if you want to keep the installation as small as possible you can i. e. remove curl right after the gpg download or skip the curl installation and do the gpg download in a different AppVM and afterwards move the gpg key to the template VM.
  [/details]

* **qubes-core-agent-networking** : *to allow internet access*
* **qubes-core-agent-nautilus** : graphical folder and file view and file operations
* **nautilus** : graphical folder and file view and file operations
* **zenity** : graphical user dialogs
* **gnome-keyring** : gpg key management
* **fonts-noto-color-emoji** : optionally, to ensure emojis are properly displayed
* **dunst** : for desktop notifications
* **xfce4-notifyd** : for desktop notifications
* **pulseaudio-qubes**: Do be able to make audio and video calls

  [details="Remark"]
  If you just want to do texting you can skip the pulseaudio-qubes package.
  [/details]

**Comments** : …
[/details]



# Thunderbird
[details="Qubes OS - minimal installation"]

**Official installation instructions:** : 
**Installation type**: 
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **xxx** : yyy
* **xxx** : yyy

**Comments** : …

[/details]



# Yubikey U2F
[details="Qubes OS - minimal installation"]

**Official installation instructions:** : 
**Installation type**: 
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **xxx** : yyy
* **xxx** : yyy

**Comments** : …



[/details]
# Yubikey Manager
[details="Qubes OS - minimal installation"]

**Official installation instructions:** : 
**Installation type**: 
**Qubes OS release** : 4.1
**Debian release** : 11
**Required packages** :

* **xxx** : yyy
* **xxx** : yyy

**Comments** : …

[/details]