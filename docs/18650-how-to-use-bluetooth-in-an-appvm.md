Kind of had a hard time getting bluetooth running despite there being quite a bunch of guides and problem-reports on the internetz. Or maybe because of that. As usual I found the [arch wiki](https://wiki.archlinux.org/title/Bluetooth) most helpful.

There is a guide for debian qubes [somewhere](https://to-be.completed.org) which was helpful, but I wanted to use [pipewire](https://wiki.archlinux.org/title/PipeWire) and debian being the old aunt... 

Anyway, I'd like to share my writeup, since that might be useful for others.

```bash 
### in dom0
# check and/or enable bluetooth controller
cat /sys/devices/platform/thinkpad_acpi/bluetooth_enable
echo 1 > /sys/devices/platform/thinkpad_acpi/bluetooth_enable

# you can try to persistently attach the bluetooth controller
# but the device ID (check which) might change after a reboot 
qvm-device usb attach --persistent podcasts sys-usb:1-7
````

```bash
### in templateVM
# archlinux, obviously
sudo pacman -S bluez bluez-tools bluez-utils blueman
sudo pacman -S pavucontrol pulseaudio-bluetooth linux-firmware
sudo pacman -S obs-studio

# enable experimental features for bluetooth
sudo nano /etc/bluetooth/main.conf
# put the following just under [General]
 FastConnectable = true
 Experimental = true
 KernelExperimental = true
```

```bash
### in appVM
# to be done once if you want to make bluetooth configs persistant
sudo cp /etc/bluetooth /rw/config/
sudo /bin/sh -c 'echo "mount --bind /rw/config/bluetooth /etc/bluetooth" >> /rw/config/rc.local'
sudo /bin/sh -c 'echo "mount --bind /rw/config/bluetooth /var/lib/bluetooth" >> /rw/config/rc.local'

# to be done after each reboot (after attaching the usb-bluetooth-controller)
rfkill list
sudo systemctl start bluetooth
pulseaudio -k ; pulseaudio -D

# play around with stuff
blueman-manager&
pavucontrol&
quake2&
```

I couldn't get pipewire to work, though. Which is unfortunate as modern bluetooth headsets rely on modern codecs. To use a recent kernel in your archlinux qubes [this is](https://www.qubes-os.org/doc/managing-vm-kernels/) how-to it.

I'm happy for anybody correcting mistakes in my writeup... and for relevant advice concerning pipewire of course. I assume the qubes devs are [working on it](https://github.com/QubesOS/qubes-issues/issues/6358).

PS: [this](https://github.com/QubesOS/qubes-gui-agent-linux/pull/157) looks promising.