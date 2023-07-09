Guide about how to update kernels in Qubes OS 4.1. If kernel you want is in `qubes-dom0-unstable repository`, follow https://www.qubes-os.org/doc/managing-vm-kernels/

Assume AppVM is `disp1` and you have `qvm-copy-to-dom0` script in dom0.

Select kernels you want from https://ftp.qubes-os.org/repo/yum/r4.1/current/dom0/fc32/rpm/ 
Make sure have three rpm because some kernels only have `kernel-latest-*.qubes.x86_64.rpm`.

`kernel-latest-*.qubes.x86_64.rpm`
`kernel-latest-devel-*.qubes.x86_64.rpm`
`kernel-latest-qubes-vm-*.qubes.x86_64.rpm`

Suppose we want to install `5.16.18`.

After downloading kernels to `Download` of `disp1`, compress them to a single file because `qvm-copy-to-dom0` can't copy directory.
In `disp1`, run:
```bash
cd ~/Downloads
tar cvzf 5.16.18.tgz *5.16.18*
```

In `dom0`, run
```bash
kernel_version=5.6.18

mkdir $kernel_version
cd $kernel_version

qvm-copy-to-dom0 disp1 ~/Downloads/$kernel_version.tgz $kernel_version.tgz 

tar -xvf $kernel_version.tgz

sudo dnf install -y kernel-latest-*.qubes.x86_64.rpm
sudo dnf install -y kernel-latest-qubes-vm-*.qubes.x86_64.rpm

# install dependencies of devel
# if you need other dependies, search how to install them in Fedora, and replace `dnf install` with `qubes-dom0-update`
sudo qubes-dom0-update -y elfutils-libelf-devel
sudo dnf install -y kernel-latest-devel-*.qubes.x86_64.rpm

rm -rf ../kernel_version
```
After reboot, Qubes OS will select latest kernel automatically. You can manually set kernel too.