I messed up something on some config file in dom0, and so QubesOS would crash on boot.  

So I had to find a way to start it in rescue mode/maintenance mode/init 1/single user mode, and from what I saw on the QubesOS website and this forum, nothing help me much.   

So here is what I did if someone found it useful (or for me later if I messed up again) and can confirm it works well with Qubesos :   

>  From the GRUB boot prompt, press the E button to edit the first boot option.  
> 
> Find the kernel line starting with linux and change ro to rw init=/sysroot/bin/sh.