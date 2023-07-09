# Troubleshooting

## How can I disable Xen Meltdown mitigations?

Set `xpti=false` option in Xen command line (xen.gz option in grub, or options= line in xen.cfg for UEFI).

## How can I upgrade to testing?

dom0: `sudo qubes-dom0-update --enablerepo=qubes-dom0-current-testing --clean` (or --check-only instead for dom0).

fedora: `sudo dnf update --enablerepo=qubes-vm-*-current-testing --refresh`

debian/whonix: `sudo apt-get update -t *-testing && sudo apt-get dist-upgrade -t *-testing`

This way, you don't need to edit any files for debian/whonix to get the testing. If you also want to increase reliability further, you can make a dependency/cache check with "sudo apt-get check", which is normally very quick. For that, under debian/whonix do: `sudo apt-get check && sudo apt-get update -t *-testing && sudo apt-get dist-upgrade -t *-testing`.

## How can I upgrade dom0, templates, and standalones?

Make a dom0 script with the following:

```
#!/bin/sh

for domain in $(qvm-ls --fields NAME,CLASS | \
    awk '($2 == "TemplateVM" || $2 == "StandaloneVM") {print $1}'); do
    qvm-run --service $domain qubes.InstallUpdatesGUI
done

sudo qubes-dom0-update
```

From <https://gist.github.com/JimmyAx/818bcf11a14e85531516ef999c8c5765>. See also the scripts listed under [`OS-administration`](https://github.com/Qubes-Community/Contents/tree/master/code).

## VM fail to start after hard power off

I realized that some VMs refuse to start after a hard power-off (hold power button for 10s). When running `qvm-start test` I get `vm-test-private missing`. But this thin volume is actually there. Also the volume `vm-test-private-snap` is still present.

Try this in dom0:

```
sudo pvscan --cache --activate ay
sudo systemctl restart qubesd
qvm-start test
```

## Slow VM startup

Use tools like 'systemd-analyze blame' as your guide.

Another service that shows up with significant time is wpa_supplicant. You can have it start only for network VMs by creating `/lib/systemd/system/wpa_supplicant.service.d/20_netvms` with the following:

```
[Unit]
ConditionPathExists=/var/run/qubes/this-is-netvm
```

## Xen passthrough compatible video cards

- <https://en.wikipedia.org/wiki/List_of_IOMMU-supporting_hardware#AMD>
- <http://www.overclock.net/t/1307834/xen-vga-passthrough-compatible-graphics-adapters>
- <https://wiki.xenproject.org/wiki/Xen_VGA_Passthrough_Tested_Adapters#ATI.2FAMD_display_adapters>

## Discrete nVidia GPU support

This will definitely vary by system, but some have managed to use onboard Intel graphics for Qubes and still permit function of their separate nVidia card by editing their xen.cfg with:

- Removed nouveau.modeset=0
- Added kernel param: acpi_osi=!
- Changed iommu support from iommu=no-igfx to iommu=on

## Where are VM log files kept?

In the `/var/log/libvirst/libxl/`, `/var/log/qubes/` and `/var/log/xen/console/` directories.

# Development

## What is the process flow when opening a link/file in another VM ?

1.  in an AppVM ('srcVM') a link - or file - is set to be opened with the graphical "open in VM" or "open in dispVM" extensions (or respectively with the `/usr/bin/qvm-open-in-vm` or `/usr/bin/qvm-open-in-dvm` command line tools)
2.  in src VM, the destination VM is hardcoded to '$dispvm' if dispVMs are used (`/usr/bin/qvm-open-in-dvm` is a simple wrapper to `/usr/bin/qvm-open-in-vm`)
3.  in srcVM, `/usr/lib/qubes/qrexec-client-vm` is called, which in turn executes the `qubes.OpenURL` [RPC service](https://www.qubes-os.org/doc/qrexec3/#qubes-rpc-services) to send the url to dstVM
4.  in dstVM, `/etc/qubes-rpc/qubes.OpenURL` is called upon reception of the `qubes.OpenURL` RPC event above, which validates the url and executes `/usr/bin/qubes-open`
5.  in dstVM, `/usr/bin/qubes-open` executes `xdg-open`, which then opens the url/file with the program registered to handle the associated mime type (for additional info see the [freedesktop specifications](https://www.freedesktop.org/wiki/)).

## What are some undocumented QWT registry keys?

MaxFPS, UseDirtyBits.

# Tweaks

## Disable auto-maximize when dragging window to top of screen in XFCE

Uncheck System Tools \> Window Manager Tweaks \> Accessibility \> Automatically tile windows when moving toward the screen edge.

## How can I set environment variables for a VM?

Either add to `/etc/environment` or create `~/.envsrc` and set a variable there, then create `.xsessionrc` and source `~/.envsrc`. See [this thread](https://www.mail-archive.com/qubes-users@googlegroups.com/msg20360.html).

## How would I enable sudo authentication in a Template?

There are two ways to do this now:

1.  Follow this [Qubes doc](https://www.qubes-os.org/doc/vm-sudo/#replacing-password-less-root-access-with-dom0-user-prompt) to get the yes/no auth prompts for sudo.

2.  Remove the 'qubes-core-agent-passwordless-root' package.

This second way means that sudo no longer works for a normal user. Instead, any root access in the VM must be done from dom0 with a command like `qvm-run -u root vmname command`.

## How can I provision a VM with a larger/non-standard swap and /tmp?

Fedora's /tmp uses tmpfs ; it's mounted by systemd at boot time. See `systemctl status tmp.mount` and `/usr/lib/systemd/system/tmp.mount.d/30_qubes.conf` to increase its size. Alternatively you can increase the size afterwards with `mount -o remount,size=5G /tmp/`.

If you need to have a disk based tmp you'll have to mask the systemd unit (`systemctl mask tmp.mount`) and put a fstab entry for /tmp.

Alternatively you can add swap with a file inside the vm but it's a bit ugly:

```
dd if=/dev/zero of=swapfile bs=1M count=1000
mkswap swapfile
swapon swapfile
```

## How do I attach an `.img` file to a Qube?

```
    # a file cannot be attached if it is in directory /var/lib/qubes/appvms, so create a link first
    ln /var/lib/qubes/appvms/$1/private.img /home/user/private.img
    LOOPDEV=`sudo losetup -f`
    sudo losetup $LOOPDEV /home/user/private.img
    qvm-block attach -o frontend-dev=xvds -o read-only=true backupvm dom0:$(basename "$LOOPDEV")

[backup happens here]

    qvm-block detach backupvm dom0:$(basename "$LOOPDEV")
    sudo losetup -d $LOOPDEV
    rm /home/user/private.img
```

See <https://groups.google.com/d/msg/qubes-users/LLSo_3oWXJI/0clWN0BUBgAJ> for more details.

## How can I "sparsify" an existing volume?

Use the `fallocate` command. It has a way to deallocate zero blocks in-place so you probably won't need to use issue lvm commands directly:

`sudo fallocate --dig-holes /dev/mapper/qubes_dom0-vm--untrusted--private`

This method can also be used on .img files (for Qubes installations that use them).

## How do I change display resolution on a Linux HVM?

You only get one resolution at a time. In the HVM's `/etc/X11/xorg.conf`, in Subsection "Display" for Depth 24, make a single mode like this:

```
...
    Subsection "Display"
        Viewport 0 0
        Depth 24
        Modes "1200x800"
    EndSubSection
EndSection
```

Only some modes will work. check wikipedia. if your host display is 1080p(1920x1080), then an hvm at 1440x900 works well. if its more than that, might as well do 1080p in the hvm.

## How can I get Bluetooth audio working?

Either use a 3.5mm jack to BT adapter, or see [this](https://m7i.org/tips/qubes-VM-bluetooth-audio/).

Hint: [this guide](../configuration/bluetooth.md) might come in handy too.

## Manually install Whonix templates

See the [official Whonix documentation](https://www.whonix.org/wiki/Qubes/Install) for supported installation methods.

*Thanks to all mailing list contributors, from where most of these came.*

# Qubes 3.2

## In Qubes 3.2, how do I remove old entries from "Move/copy to other AppVM"?

The rogue entries are stored in \~/.config/qvm-mru-filecopy in the qube you are trying to copy from. You can just edit that file to remove them from the list.

## How can I permanently attach a block device to an HVM?

In 3.2 you can just edit the conf file under /var/lib/qubes.

# Qubes 4.0

## How can I contribute to developing Qubes Windows Tools for R4.0?

See [this post](https://www.mail-archive.com/qubes-devel@googlegroups.com/msg02808.html) and thread.

## How can I switch R4.0 stubdomains back to qemu-traditional?

```
qvm-features VMNAME linux-stubdom ''
```

## How can I build an ISO from existing packages without having to compile them all?

```
gpg --fetch-keys https://keys.qubes-os.org/keys/qubes-developers-keys.asc
git clone https://github.com/QubesOS/qubes-builder.git
cd qubes-builder
git verify-commit HEAD || echo DANGER DANGER HIGH VOLTAGE
cp example-configs/qubes-os-r4.0.conf builder.conf
variables='DISTS_VM= USE_QUBES_REPO_VERSION=4.0 USE_QUBES_REPO_TESTING=1 INSTALLER_KICKSTART=/tmp/qubes-installer/conf/travis-iso-full.ks'
make $variables COMPONENTS='installer-qubes-os builder-rpm' get-sources
make $variables COMPONENTS=intel-microcode get-sources qubes clean-rpms
[Customize as desired here]
sudo chroot chroot-fc25 dnf -y install dnf-yum
make $variables COMPONENTS= iso
```

If any step fails due to a download error, just rerun it. If you wish to customize the kernel or another package, include it (e.g. `linux-kernel`) in `COMPONENTS` to actually include that package on the image. You may also need to either adjust `qubes-src/installer-qubes-os/conf/comps-qubes.xml` (kernel -> kernel-latest), or build the package as "kernel" not "kernel-latest" (edit `suffix` file in the linux-kernel sources). Make sure `audit=0` is not present in kernelopts / `/proc/cmdline`.

## How can I permanently attach a block device to an HVM?

Have a look at <https://dev.qubes-os.org/projects/core-admin/en/latest/libvirt.html>

You want to add a new device: use normal Xen configuration. <https://libvirt.org/formatdomain.html#elementsDisks> will help. Use the phy driver, and specify the source as /dev/sdX, and target dev on your qube.

The libvirt page explains how to create a custom specification for a qube, and where to put the files. The basic specification is created from a template file - on my system it's at /usr/share/qubes/templates/libvirt/xen.xml. (The documentation is a little out of step here.) If you look at that file you can see how the configuration for your qubes is constructed.

What we want to do is to modify the settings for qube foo so that /dev/sdb on dom0 will appear at /dev/xvde in foo.

Create a new file in dom0 at:

```
/etc/qubes/templates/libvirt/by-name/foo.xml
```

The contents are:

```
{% extends 'libvirt/xen.xml' %}
{% block devices %}
    {{ super() }}
        <disk type='block' device='disk' >
            <driver name='phy' />
            <source dev='/dev/sdb' />
            <target dev='xvde' />
        </disk>
{% endblock %}
```

The "extends" statement tells the system that it will be modifying the definition in libvirt/xen.xml. The "super()" imports the specification for block devices from that file. Then we define a new disk device - the syntax here is quite obvious and follows the reference in libvirt.org.

Now when you boot foo, Qubes will pick up this file, and attach /dev/sdb to the foo qube, where it will appear as /dev/xvde. You can put an entry in to /etc/fstab so that the /dev/xvde device will be automatically mounted where you will.

## What is the process flow when starting an AppVM under Qubes R4.x?

1.  qvm-start sends a request to qubesd, using Admin API
2.  qubesd starts required netvm (recursively), if needed
3.  qubesd request qmemman to allocate needed memory for new VM (according to VM's 'memory' property)
4.  qubesd calls into appropriate storage pool driver to prepare for VM startup (create copy-on-write layers etc)
5.  qubesd gathers needed VM properties etc and builds libvirt VM configuration (XML format, can be seen using `virsh dumpxml`)
6.  qubesd calls into libvirt to start the VM (but in paused mode)
7.  libvirt setup the VM using libxl, this include starting stubdomain if needed
8.  qubesd start auxiliary processes, including:
    - qrexec-daemon
    - qubesdb-daemon (and fill its content)
9.  libvirt unpause the VM
10. qvm-start-gui process (running separately from qubesd, as part of dom0 user GUI session) starts gui daemon

See "source" link [here](https://dev.qubes-os.org/projects/core-admin/en/latest/qubes-vm/qubesvm.html#qubes.vm.qubesvm.QubesVM.start).

# Qubes 4.1

## How can I permanently attach a block device to an HVM?

Assuming that block device is labeled as `sdb`, run the following command:

```
qvm-block attach --persistent <HVM> sys-net:sdb
```

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/misc/iaq.md)
- First commit: 30 Apr 2018. Last commit: 14 Oct 2018.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 3.2, 4.0
- Original author(s) (GitHub usernames): awokd, taradiddles, null
- Original author(s) (forum usernames): @taradiddles
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>