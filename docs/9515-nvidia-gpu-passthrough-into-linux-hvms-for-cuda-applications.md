While it is well known that [gaming in Windows HVMs](https://github.com/Qubes-Community/Contents/blob/master/docs/customization/windows-gaming-hvm.md) is easy to do now, I haven't seen much talk about Linux HVMs. In my personal use case, I wanted to run CUDA applications in a "headless" manner. By this, I mean having being able to use Qubes seamless GUI with a CUDA device in an AppVM like:

![2022-02-16_13-38|513x500](upload://oW9iRtzBQTkSrsoMIGN5OacQVTa.png)

If you would like to do this, below are the steps I took to create this. Note that I am not sure if this will work on 4.0. This guide will use a Standalone Fedora VM, and install the RPMFusion NVIDIA drivers. This should work for other OS/driver packages. I am just keeping it simple to give you a working setup fast.

Firstly, Follow the [gaming in Windows HVMs](https://github.com/Qubes-Community/Contents/blob/master/docs/customization/windows-gaming-hvm.md) guide for steps 1-3, i.e. ensure IOMMU groups are good, edit your GRUB options to hide your GPU device, and patch the stubdom-linux-rootfs.gz file. 

Now we will create the VM. In this case, create a new StandaloneVM from a Fedora template.

![2022-02-16_13-55|622x370](upload://9ttzmdWPk1nFNOJejjZKF9Y2WuM.png)

and configure your VM settings as such:

![2022-02-16_13-59|685x500](upload://9jjZSMFfRodNdifNnwBjnRVw3Wz.png)

![2022-02-16_13-59_1|682x500](upload://3HXVSHHfpdqVOYsm5S1LIM4QI5F.png)

`VCPUs` doesn't need to be as high if you don't have that many cores. Just set it to an appropriate option. Now, in dom0, attach your GPU's PCI devices to the VM. Again, following from the Windows guide, whether or not you require permissive mode is dependent on your system. In this example, my GPU is 01:00.0 and my GPU's audio device is 01:00.1:
```
qvm-pci attach --persistent gpu-linux dom0:01_00.0 -o permissive=True -o no_strict_reset=True`
qvm-pci attach --persistent gpu-linux dom0:01_00.1 -o permissive=True -o no_strict_reset=True
```

Start your VM now. `lspci -k` should output something similar:
```
[user@gpu-linux ~]$ lspci -k
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
	Subsystem: Red Hat, Inc. Qemu virtual machine
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
	Subsystem: Red Hat, Inc. Qemu virtual machine
00:01.1 IDE interface: Intel Corporation 82371SB PIIX3 IDE [Natoma/Triton II]
	Subsystem: Red Hat, Inc. Qemu virtual machine
	Kernel driver in use: ata_piix
	Kernel modules: pata_acpi, ata_generic
00:01.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 03)
	Subsystem: Red Hat, Inc. Qemu virtual machine
	Kernel modules: i2c_piix4
00:02.0 Unassigned class [ff80]: XenSource, Inc. Xen Platform Device (rev 01)
	Subsystem: XenSource, Inc. Xen Platform Device
	Kernel driver in use: xen-platform-pci
00:04.0 VGA compatible controller: Device 1234:1111 (rev 02)
	Subsystem: Red Hat, Inc. Device 1100
	Kernel modules: bochs_drm
00:05.0 USB controller: Intel Corporation 82801DB/DBM (ICH4/ICH4-M) USB2 EHCI Controller (rev 10)
	Subsystem: Red Hat, Inc. QEMU Virtual Machine
	Kernel driver in use: ehci-pci
	Kernel modules: ehci_pci
00:07.0 VGA compatible controller: NVIDIA Corporation GA104 [GeForce RTX 3070] (rev a1)
	Subsystem: PNY Device 136f
	Kernel modules: nouveau
00:08.0 Audio device: NVIDIA Corporation GA104 High Definition Audio Controller (rev a1)
	Subsystem: PNY Device 136f
	Kernel driver in use: snd_hda_intel
	Kernel modules: snd_hda_intel
[user@gpu-linux ~]$ 
```
As we can see, 00:07.0 corresponds to the GPU, and 00:08.0 corresponds to the GPU's audio device. If you can get this far, the rest of the guide _should_ work. 

For now, as mentioned at the start of the post, we will keep it simple and use RPMFusion's drivers. in your VM, we must enable RPMFusion's repos:

```[user@gpu-linux ~]$ sudo dnf config-manager --enable rpmfusion-{free,nonfree}{,-updates}```

Now, following [RPMFusion's NVIDIA page](https://rpmfusion.org/Howto/NVIDIA#Current_GeForce.2FQuadro.2FTesla):
```
sudo dnf update -y # and reboot if you are not on the latest kernel
sudo dnf install akmod-nvidia # rhel/centos users can use kmod-nvidia instead
sudo dnf install xorg-x11-drv-nvidia-cuda #optional for cuda/nvdec/nvenc support
```

**DO NOT RESTART AT THIS POINT!!!** 
you must wait for akmod to finish building:

```
[user@gpu-linux ~]$ modinfo -F version nvidia
modinfo: ERROR: Module nvidia not found. // not finished yet
[user@gpu-linux ~]$ modinfo -F version nvidia
510.47.03 // completed!
```

**STILL, DO NOT RESTART AT THIS POINT!!!! if you restarted your VM already and it is not working, either create a new VM from step 1 or go to end for information on debugging a broken Xorg.**

RPMFusion's NVIDIA driver package creates a file which will **BREAK XORG**. If you are installing from another repo or for another OS, you might get extra unwanted files as well. In RPMFusion's case, look here:
```
[user@gpu-linux ~]$ ls /usr/share/X11/xorg.conf.d/
10-quirks.conf  40-libinput.conf  71-libinput-overrides-wacom.conf  nvidia.conf
[user@gpu-linux ~]$ cat /usr/share/X11/xorg.conf.d/nvidia.conf 
#This file is provided by xorg-x11-drv-nvidia
#Do not edit

Section "OutputClass"
	Identifier "nvidia"
	MatchDriver "nvidia-drm"
	Driver "nvidia"
	Option "AllowEmptyInitialConfiguration"
	Option "SLI" "Auto"
	Option "BaseMosaic" "on"
EndSection

Section "ServerLayout"
	Identifier "layout"
	Option "AllowNVIDIAGPUScreens"
EndSection
```
Xorg will not be happy about this. While the file reads `Do not edit`, we are gonna do exactly that and just delete it. (someone else better with Xorg please provide a nicer solution)
```
[user@gpu-linux ~]$ sudo rm /usr/share/X11/xorg.conf.d/nvidia.conf 
[user@gpu-linux ~]$ ls /usr/share/X11/xorg.conf.d/
10-quirks.conf  40-libinput.conf  71-libinput-overrides-wacom.conf
```
After you delete the file, you can restart the VM. Your `lspci -k` should confirm that the driver loaded!
```
[user@gpu-linux ~]$ lspci -k
00:00.0 Host bridge: Intel Corporation 440FX - 82441FX PMC [Natoma] (rev 02)
	Subsystem: Red Hat, Inc. Qemu virtual machine
00:01.0 ISA bridge: Intel Corporation 82371SB PIIX3 ISA [Natoma/Triton II]
	Subsystem: Red Hat, Inc. Qemu virtual machine
00:01.1 IDE interface: Intel Corporation 82371SB PIIX3 IDE [Natoma/Triton II]
	Subsystem: Red Hat, Inc. Qemu virtual machine
	Kernel driver in use: ata_piix
	Kernel modules: pata_acpi, ata_generic
00:01.3 Bridge: Intel Corporation 82371AB/EB/MB PIIX4 ACPI (rev 03)
	Subsystem: Red Hat, Inc. Qemu virtual machine
	Kernel modules: i2c_piix4
00:02.0 Unassigned class [ff80]: XenSource, Inc. Xen Platform Device (rev 01)
	Subsystem: XenSource, Inc. Xen Platform Device
	Kernel driver in use: xen-platform-pci
00:04.0 VGA compatible controller: Device 1234:1111 (rev 02)
	Subsystem: Red Hat, Inc. Device 1100
	Kernel modules: bochs_drm
00:05.0 USB controller: Intel Corporation 82801DB/DBM (ICH4/ICH4-M) USB2 EHCI Controller (rev 10)
	Subsystem: Red Hat, Inc. QEMU Virtual Machine
	Kernel driver in use: ehci-pci
	Kernel modules: ehci_pci
00:07.0 VGA compatible controller: NVIDIA Corporation GA104 [GeForce RTX 3070] (rev a1)
	Subsystem: PNY Device 136f
	Kernel driver in use: nvidia
	Kernel modules: nouveau, nvidia_drm, nvidia
00:08.0 Audio device: NVIDIA Corporation GA104 High Definition Audio Controller (rev a1)
	Subsystem: PNY Device 136f
	Kernel driver in use: snd_hda_intel
	Kernel modules: snd_hda_intel
[user@gpu-linux ~]$ 
```
`nvidia-smi` will also be able to tell you information:
```
[user@gpu-linux ~]$ nvidia-smi
Wed Feb 16 14:37:50 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.47.03    Driver Version: 510.47.03    CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:00:07.0 Off |                  N/A |
| 31%   38C    P0    N/A / 220W |      0MiB /  8192MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```
Your GPU should now be work for CUDA applications!

 **OPTIONAL: TEST WITH PYTORCH**

Here are the steps as of this date, note that this might change in the future. Before proceeding, **MAKE SURE YOU HAVE 10GB+ IN YOUR HOME FOLDER**. If not, open your VM's settings and make sure your private storage is above 10GB as shown in the guide earlier.

Install conda, which can be found [here](https://docs.conda.io/en/latest/miniconda.html#linux-installers). In this case, I will install the current latest version for python3.9:
```
[user@gpu-linux ~]$ wget -q https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh 
[user@gpu-linux ~]$ chmod +x Miniconda3-py39_4.11.0-Linux-x86_64.sh 
[user@gpu-linux ~]$ ./Miniconda3-py39_4.11.0-Linux-x86_64.sh 
```
Follow the installation like normal. Once it's done, open a new shell and you should have
`(base) [user@gpu-linux ~]$` prompt. 

Now we can install pytorch from [here](https://pytorch.org/get-started/locally/). In this case, I will install Stable 1.10.2, using Conda, with CUDA 11.3. Note that this will install pytorch and its required files into the `base` environment:
```
(base) [user@gpu-linux ~]$ conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```
Accept the installation, and wait. This will take a little bit. After pytorch is done installing, you can check it with python:
```
(base) [user@gpu-linux ~]$ python
Python 3.9.7 (default, Sep 16 2021, 13:09:58) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
True
>>> 
```
You should get the exact same output. Awesome!

**OPTIONAL: Enable Coolbits**

Coolbits allow for more control of your hardware, such as setting fan speeds and overclocking etc. It allows for apps like [GreenWithEnvy](https://gitlab.com/leinardi/gwe) to be used to easily control these settings.

Note: this procedure _may_ mess up your Xorg, which you will have to follow tips at the bottom to recover from. **DISCLAIMER: VERY HACKY STUFF ABOUT TO FOLLOW**. I hope to find a better way to get this done, and I will update when it is found.

As of the time of this writing, Coolbits requires you to manipulate your Xorg configuration. It is a mystery as to why Xorg has anything to do with overclocking and fan speeds. Let's start by installing gwe:
```
(base) [user@gpu-linux ~]$ sudo dnf install gwe
```
Starting gwe now, you will be greeted with this message:

![2022-02-16_15-17|622x234](upload://b9VjxtSQU4JEhHQSYDRO1KYcQt1.png)

To fix this, we essentially need to make a fake screen for the NVIDIA GPU :roll_eyes:. We will create a nvidia.conf file. Open up `/etc/X11/xorg.conf.d/nvidia.conf` in your favourite text editing program, and paste this in:

```
Section "ServerLayout"
  Identifier	"Default Layout"
  Screen 0      "Screen0" 0 0 
  Screen 1      "Screen1"
  InputDevice   "qubesdev"
EndSection

Section "Screen"
# virtual monitor
    Identifier     "Screen1"
# discrete GPU nvidia
    Device         "nvidia"
# virtual monitor
    Monitor        "Monitor1"
    DefaultDepth 24
    SubSection     "Display"
       Depth 24
    EndSubSection
EndSection

Section "Monitor"
    Identifier     "Monitor1"
    VendorName     "Unknown"
    Option         "DPMS"
EndSection


Section "Device"
# discrete GPU NVIDIA
   Identifier      "nvidia"
   Driver          "nvidia"
   Option          "Coolbits" "28"
   # BusID           "PCI:0:7:0"
EndSection
```

Under the section Device, uncomment the BusID line and put in your GPU's PCI ID. You can get the bus ID from `lspci`:
```
(base) [user@gpu-linux ~]$ lspci | grep -i NVIDIA
00:07.0 VGA compatible controller: NVIDIA Corporation GA104 [GeForce RTX 3070] (rev a1)
00:08.0 Audio device: NVIDIA Corporation GA104 High Definition Audio Controller (rev a1)
```
In my case, my GPU is `00:07.0`, which corresponds to `PCI:0:7:0` in the nvidia.conf file. Yours might be different. `x:y.z` is `PCI:x:y:z` in the nvidia.conf file.

**DO NOT RESTART XORG YET**

**For Coolbits to work, your Xorg must be running as root**. You can check this like
```
(base) [user@gpu-linux ~]$ ps aux | grep -i xorg
root       13403  0.0  0.3  11504  6124 tty7     S+   15:41   0:00 /usr/bin/qubes-gui-runuser user /bin/sh -l -c exec /usr/bin/xinit /etc/X11/xinit/xinitrc -- /usr/libexec/Xorg :0 -nolisten tcp vt07 -wr -config xorg-qubes.conf > ~/.xsession-errors 2>&1
user       13414  0.0  0.0   4148  1336 ?        Ss   15:41   0:00 /usr/bin/xinit /etc/X11/xinit/xinitrc -- /usr/libexec/Xorg :0 -nolisten tcp vt07 -wr -config xorg-qubes.conf
user       13449  1.0  4.1 258416 81260 ?        Sl   15:41   0:00 /usr/libexec/Xorg :0 -nolisten tcp vt07 -wr -config xorg-qubes.conf
```

Here we can see /usr/libexec/Xorg is running as user. This is the case on Fedora at least. If you are **NOT** running as root, you need to edit a script file. **DISCLAIMER: editing Qubes files is bad**. Hopefully we can get this fixed in the future.

Open up the file `/usr/bin/qubes-run-xorg`, and at the bottom you will see this:
```
if qsvc guivm-gui-agent; then
    DISPLAY_XORG=:1

    # Create Xorg. Xephyr will be started using qubes-start-xephyr later.
    exec runuser -u "$DEFAULT_USER" -- /bin/sh -l -c "exec $XORG $DISPLAY_XORG -nolisten tcp vt07 -wr ->
else
    # Use sh -l here to load all session startup scripts (/etc/profile, ~/.profile
    # etc) to populate environment. This is the environment that will be used for
    # all user applications and qrexec calls.
    exec /usr/bin/qubes-gui-runuser "$DEFAULT_USER" /bin/sh -l -c "exec /usr/bin/xinit $XSESSION -- $XO>
fi
```
simply add the line `DEFAULT_USER="root"` before this, as such:
```
DEFAULT_USER="root"
if qsvc guivm-gui-agent; then
    DISPLAY_XORG=:1

    # Create Xorg. Xephyr will be started using qubes-start-xephyr later.
    exec runuser -u "$DEFAULT_USER" -- /bin/sh -l -c "exec $XORG $DISPLAY_XORG -nolisten tcp vt07 -wr ->
else
    # Use sh -l here to load all session startup scripts (/etc/profile, ~/.profile
    # etc) to populate environment. This is the environment that will be used for
    # all user applications and qrexec calls.
    exec /usr/bin/qubes-gui-runuser "$DEFAULT_USER" /bin/sh -l -c "exec /usr/bin/xinit $XSESSION -- $XO>
fi
```
now you can restart your VM/Xorg. `nvidia-smi` will now show that Xorg is running on the GPU (in a headless state though)
```
(base) [user@gpu-linux ~]$ nvidia-smi
Wed Feb 16 15:53:51 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.47.03    Driver Version: 510.47.03    CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:00:07.0  On |                  N/A |
| 30%   34C    P8    10W / 220W |     23MiB /  8192MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A     13901      G   /usr/libexec/Xorg                  21MiB |
+-----------------------------------------------------------------------------+
```
and gwe will work:

![2022-02-16_15-54|651x500](upload://hGFgk7o549U6Egd9MPF7OWLB0uO.png)

Congratulations! you have everything setup.

**BROKEN XORG TIPS, GUI NOT WORKING FIXES ETC**

When applications won't start, you can access a terminal inside of the vm from dom0:
`qvm-console-dispvm gpu-linux`. This will launch a terminal:

![2022-02-16_16-04|522x359](upload://wVVVMvoY27oMcO967LGPyNDFWGm.png)

It is likely there'll be a bunch of text. Don't worry about it. Just type in `user` and press enter. It will login and you now have a terminal to fix Xorg.

Some tips for fixing Xorg problems:

1. `qubes-gui-agent` controls Xorg, and it uses the config at `/etc/X11/xorg-qubes.conf` to do so. While editing your Xorg files, you can restart qubes-gui-agent by `sudo systemctl restart qubes-gui-agent` and it will restart Xorg for you, instead of needing to restart the VM.

2. Xorg will check directories `/usr/share/X11/xorg.conf.d`, and `/etc/X11/xorg.conf.d` after reading the `xorg-qubes.conf` file. You must make sure that there are no other files that might be conflicting with Qubes.

3. The Xorg log files can be found at `/home/user/.xsession_errors`, and `/home/user/.local/share/xorg/Xorg.0.log`. If your Xorg.0.log contains "Operation not permitted" etc, you most likely have to run Xorg as root, see the Coolbits section.

4. While fiddling with my setup to get this working, I had to restart my computer a few times because the GPU gets put into a unrecoverable situation occassionally. If you are scratching your head as to why something isn't working, try restarting your computer.