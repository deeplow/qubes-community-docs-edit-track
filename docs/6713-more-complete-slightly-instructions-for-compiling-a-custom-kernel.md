The kernel instructions to compile your own kernel at https://www.qubes-os.org/doc/managing-vm-kernels/#installing-different-vm-kernel-based-on-dom0-kernel seem incomplete, so I'm making a slightly more complete version here:

1.  do:
   ```
   sudo qubes-dom0-update qubes-kernel-vm-support kernel-devel
   ```
2. Find a valid version (which will eventually be used as a parameter for qubes-prepare-vm-kernel) by doing:
   ```
   ls /usr/src/kernels/
   ```
   each subdirectory name should be a valid version, and will be a valid parameter for qubes-prepare-vm-kernel.
3. Pick a subdirectory / version and enter that subdirectory.  Example:
   ```
   cd 5.10.61-1.fc32.qubes.x86_64
   ```
4. Configure the kernel by editing the .config file in that directory
    (note, you cannot use "make menuconfig" or "make config", unless you install the special dependencies for those)
    (Also note, there are a lot of options, so it may take a while)
5. build it with qubes-prepare-vm-kernel {name of exact subdirectory you chose}. Example:
   ```
   sudo qubes-prepare-vm-kernel 5.10.61-1.fc32.qubes.x86_64
   ```
This should succeed in placing a new copy of the kernel in /var/lib/qubes/vm-kernels/{version of what you just configured}

**However**, the compilation process runs ***way*** too fast, so it is obviously not compiling the kernel.  Possibly just managing modules?

**Confirmed:**  typing ```make all``` or  ```make zImage``` returns "flex: command not found", so it is not capable of recompiling it as it would require packages to do the actual build that are not on your system

**Conjectured procedure:**
So, i suspect you are supposed to create a development qube.  And I'll conjecture that it's supposed to be a fedora qube (to match dom0).  I'm not familiar with the fedoa build dependancies, but I'm guessing it should be something like:
```
qvm-create --template fedora32 --label red kernel-compile
cd /
tar -cvzf ~/kernel-to-transfer.tgz /usr/src/kernels/{kernel version}/
qvm-copy-to-vm kernel-compile ~/kernel-to-transfer.tgz
qvm-run kernel-compile 'sudo dnf install kernel-devel'   ### to install the fedora build dependancies
qvm-run kernel-compile 'tar -xvzf /home/user/QubesIncoming/dom0/kernel-to-transfer.tgz'   ## (this would need to be done from /)
##then log into kernel-compile
cd /usr/src/kernels/{version you just copied over ending in .qubes.x86_64}  
make menuconfig
make all
tar -cvzf /home/user/back-to-dom0.tgz /usr/src/kernels/{version you just copied over ending in .qubes.x86_64}
###go back to dom0
qvm-run --pass-io kernel-compile 'cat /home/user/back-to-dom0.tgz' > /home/user/back-to-dom0.tgz
cd /
tar -xvzf /home/usr/back-to-dom0.tgz
```

Then use the ```sudo qubes-prepare-vm-kernel 5.10.61-1.fc32.qubes.x86_64``` (or whatever your version name was) command to install it