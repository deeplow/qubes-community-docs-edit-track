Quick guide If you have a kernel module patch and want to try it out in Qubes OS kernel. I had a hard time doing this but I finally work it out.

0. It is better to make sure that the AppVM you building kernel module at (VM1), the TemplateVM you want to try out hot patch (VM2), and the AppVM user of VM2 (VM3) uses the exact same version of Qubes OS VM kernel.
1. Build your patched kernel module in VM1. Make sure that you have the environment suitable for linux kernel building (tutorial on how to build kernel is everywhere on the internet); download the correct linux kernel version; apply patch; refer to https://yoursunny.com/t/2018/one-kernel-module/ to make sure that your module building context is correct (`cd linux-5.xx.xx`; `zcat /proc/config.gz > .config`; `ln -s /lib/modules/5.xx.xx-x.fc32.qubes.x86_64/build/Module.symvers .`; `make scripts prepare modules_prepare`); build the specific module (`make -C . M=drivers/path/to/your/module/dir/`)
2. (Optional) inspect your `.ko` file in `objdump` or `ghidra` to make sure that you have applied your patch.
3. `qvm-copy` the kernel module file to VM2.

We need to put the module file in `/lib/modules/5.xx.xx-x.fc32.qubes.x86_64/kernel/drivers/path/to/your/module/dir/`, however yo got a permission denied even when you are root (mostly due to selinux). So we have a circumvention.

4. In VM2, `cd /tmp; mkdir sysroot; sudo mount /dev/xvda3 sysroot`;
Notice that you cannot copy the sole `.ko` to the `/tmp/sysroot/lib/modules/.../`; you need to copy the whole tree and patch the module. 
Thus `sudo cp -r /lib/modules/KERNEL_VERSION /tmp/sysroot/lib/modules/`, and then patch your kernel module by
`sudo cp ~/QubesIncoming/VM1/yourmodule.ko /tmp/sysroot/lib/modules/5.xx.xx-x.fc32.qubes.x86_64/kernel/drivers/path/to/your/module/dir/`.
Finally `cd /tmp; sudo umount sysroot`

5. Shutdown VM2; reboot VM2 to see whether it boots; if it boots then the config should be correct. Run VM3 and test out your patch.