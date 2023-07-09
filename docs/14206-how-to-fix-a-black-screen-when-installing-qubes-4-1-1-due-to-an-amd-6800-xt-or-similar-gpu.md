I was getting a black screen during install. The GRUB menu loaded fine, but after selecting an install option I got a black screen (with a cursor in upper right) and never reached the installer.

I spent hours trying the following:

- Official troubleshooting pages were out of date and didn't apply to 4.1.1.
- I tried all the UEFI + legacy mode configs in BIOS 
- Bought a new USB

It turns out none of that was needed though! All you need is to add an option while in the GRUB menu.

**How to fix:**

Add `nomodeset=0` to the grub entry after booting, and it works. After install, you'll also need to do this permanently, or else each time you boot.

1. Boot from USB
2. When GRUB menu opens, navigate to the boot option you want and hit `e`
3. Find the line with `vmlinuz` in it, and add `nomodeset=0` at the end
4. Hit `CTRL + X` which will run your edited command, and you should make it to the installer!

P.S. After editing the grub config, the line containing `vmlinuz` should look something like this:

```
    module2 /images/pxeboot/vmlinuz inst.stage2=hd:LABEL=QUBES-R4-1-1-X86-64 plymouth.ignore-serial-consoles quiet nomodeset=0
```

**After install:**

You'll need to permanently edit the GRUB config with this option after install, but you can also follow the steps above each time you boot too. I haven't edited the GRUB config yet, but I've seen some discussions here about how to do so.

Without the `nomodeset=0` option after installing, you'll get to the disk encryption screen, but get a black screen after entering the password. I tried updating the kernel using `sudo qubes-dom0-update kernel-latest` in case that fixed it, but I still needed `nomodeset=0` to boot.

**What is `nomodeset`?**

Not sure, but it appears to be a common flag for fixing GPU issues.

I found the following definition here https://ubuntuforums.org/showthread.php?t=1613132:

```
**nomodeset**

The newest kernels have moved the video mode setting into the kernel. So 
all the programming of the hardware specific clock rates and registers on 
the video card happen in the kernel rather than in the X driver when the X 
server starts.. This makes it possible to have high resolution nice 
looking splash (boot) screens and flicker free transitions from boot 
splash to login screen. Unfortunately, on some cards this doesnt work 
properly and you end up with a black screen. Adding the nomodeset parameter
instructs the kernel to not load video drivers and use BIOS modes instead 
until X is loaded.
```

**Credits:**

This topic mentioned the `nomodeset` option in relation to fixing 6800 XT issues. However, being new, it still took me many hours to figure out where to put it and that I needed to set it to `nomodeset=0` :slight_smile: 

https://forum.qubes-os.org/t/anaconda-hangs-after-successfully-loading-the-live-system-cant-switch-to-a-tty/12352

Hope this helps someone!