After using OpenBSD as the main OS for 2-3 years I wanted to give Qubes OS another shot, but I still wanted to have Qube with full desktop experience of OpenBSD.
So here is my configuration how I set up my OpenBSD qube with full 1080p resolution, and with audio and usb support. This config allows me (and possibly you) to use OpenBSD qube in full screen (desktop like experience) using gop, which is not available in OpenBSD Qube using SeaBIOS.

0. Create OpenBSD installation USB with image that includes sets. Qube VM won't boot from .img file directly.
1. Create a new Standalone VM named openbsd-vm.
2. Enable audio and usb support (stubdomain).
```
	qvm-features openbsd-vm audio-model ac97
	qvm-features openbsd-vm stubdom-qrexec 1
```
3. Enable UEFI in OpenBSD qube
```
	qvm-features openbsd-vm uefi 1
```

4. We need to modify libvirt configuration for this qube, as xbf driver causes kernel panic on OpenBSD when booting under UEFI. This will make disks to show as SATA disks instead of IDE disks when xbf driver is not loaded.

	4.1. Copy default config file.
	
	```
	sudo cp /usr/share/qubes/templates/libvirt/xen.xml /etc/qubes/templates/libvirt/xen/by-name/openbsd-vm.xml
	```

	4.2. Modify below config segment in openbsd-vm.xml:

```
		from this:
		
                <disk type="block" device="{{ device.devtype }}">
                    <driver name="phy" />
                    <source dev="{{ device.path }}" />
                    {% if device.name == 'root' %}
                        <target dev="xvda" />
                    {% elif device.name == 'private' %}
                        <target dev="xvdb" />
                    {% elif device.name == 'volatile' %}
                        <target dev="xvdc" />
                    {% elif device.name == 'kernel' %}
                        <target dev="xvdd" />
                    {% else %}
                        <target dev="xvd{{dd[counter.i]}}" />
                        {% if counter.update({'i': counter.i + 1}) %}{% endif %}
                    {% endif %}

                    {% if not device.rw %}
                        <readonly />
                    {% endif %}

                    {% if device.domain %}
                        <backenddomain name="{{ device.domain }}" />
                    {% endif %}
                </disk>

		to this:
		<disk type="block" device="{{ device.devtype }}">
                    <driver name="phy" />
                    <source dev="{{ device.path }}" />
                    {% if device.name == 'root' %}
                        <target dev="sda" bus="virtio" />
                    {% elif device.name == 'private' %}
                        <target dev="sdb" bus="virtio" />
                    {% elif device.name == 'volatile' %}
                        <target dev="sdc" bus="virtio" />
                    {% elif device.name == 'kernel' %}
                        <target dev="sdd" bus="virtio" />
                    {% else %}
                        <target dev="sd{{dd[counter.i]}}" bus="virtio" />
                        {% if counter.update({'i': counter.i + 1}) %}{% endif %}
                    {% endif %}

                    {% if not device.rw %}
                        <readonly />
                    {% endif %}

                    {% if device.domain %}
                        <backenddomain name="{{ device.domain }}" />
                    {% endif %}
                </disk>
                
```

5. Start qube and enter OVMF menu. Attach install USB to VM, and boot from it. 
6. When in bootloader, type:
```
	machine gop 22 -> sets output of gop to 1920x1080. Change this to number that
		represents resolution you want. see `machine gop` for all modes
	boot -c	-> Enter boot_config 
```
7. When in boot_config (mode after entering 'boot -c'), disable xbf driver with `'disable xbf'` then `'quit'`.
8. Continue with the installation as normal (i wont explain that here.)
9. On first boot, repeat 6. and 7 as changes we did were not permanent (yet).
10. Next we need to make kernel modifications permanent. this can be done with entering ```config -e -o /bsd.new /bsd``` command as root
	10.1. Type ```disable xbf``` and then ```quit```. This will generate new modified kernel with disabled xbf driver.
11. After that we need to tell bootloader that we want to use a modified kernel with the automatic setting of gop. To do that, put the following in `/etc/boot.conf`:
	```
		machine gop 22
		boot bsd.new
	``` 
12. Thats it. You should now have Fully working OpenBSD Qube with working USB passthrough, audio and correct resolution for full screen usage.

* Known problems:
	* Was unable to use microphone. 
	* There is unhandled scsi interrupt that happens when installing OpenBSD and when shutting down a Qube. It does not cause any problems and it is not shown under normal use.