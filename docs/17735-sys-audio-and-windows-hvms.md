So, after a while of having no audio in HVMs if using sys-audio, I decided to have a look into the issue. Using https://forum.qubes-os.org/t/using-sys-audio-for-windows-audio/10416/9 as a starting point, I created a patch file that can be applied to init in `/usr/libexec/xen/boot/qemu-stubdom-linux-full-rootfs`.
```
--- init	2023-03-30 17:15:27.389013186 +0100
+++ init	2023-03-30 17:17:35.048015003 +0100
@@ -29,6 +29,7 @@
 
 # add audiodev conf to cmdline and run pulseaudio 
 audio_model=$(echo "$dm_args" | sed -n '/^-soundhw/ {n;p}')
+audioid=$(xenstore-read "/global/qvm-hvm-audio-id" || echo "0")
 if [ -n "$audio_model" ] ; then
     model_args=
     if [ "$audio_model" == "ich6" ] ; then
@@ -38,7 +39,7 @@
     pa_args=$'-audiodev\npa,id=qemupa,server=unix:/tmp/pa.sock'$model_args;
     pulseaudio --use-pid-file=no --daemonize=no --exit-idle-time=-1 --disable-shm=yes -n \
 	-L "module-native-protocol-unix auth-anonymous=1 socket=/tmp/pa.sock" \
-	-L "module-vchan-sink domid=0" &
+	-L "module-vchan-sink domid=$audioid" &
 fi
 
 # Extract network parameters and remove them from dm_args
```

Following @disp584's instructions, ensuring that commands are run as root...

1. If patch is not already installed... `qubes-dom0-update patch`
2. Make a working directory for the stubdom: `mkdir /tmp/stubroot`
3. Copy the stubdom into the directory: `cp /usr/libexec/xen/boot/qemu-stubdom-linux-full-rootfs /tmp/stubroot/stubdom.gz`
4. cd into the directory: `cd /tmp/stubroot`
5. Decompress: `gzip -d stubdom.gz`
6. Extract: `cpio -i -d -H newc --no-absolute-filenames < stubdom ; rm stubdom`
7. Patch init: `patch < /path/to/downloaded/audioid.patch`
8. Rebuild stubdom: `find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../new-stubdom`
9. (Optional) Make a backup of the original stubdom: `cp /usr/libexec/xen/boot/qemu-stubdom-linux-full-rootfs /usr/libexec/xen/boot/qemu-stubdom-linux-full-rootfs.BAK`
10. Copy the new stubdom over the old one: `mv ../new-stubdom /usr/libexec/xen/boot/qemu-stubdom-linux-full-rootfs`
11. Save the following below to a script and execute said script to update the requisite xen variable:
```
#!/bin/bash
audiodomain=$(qubes-prefs default_audiovm)
echo "Audio domain is $audiodomain"
ADxid=$(qvm-prefs "$audiodomain" xid)
echo "xid of audio domain is $ADxid"
if [ "$ADxid" -gt -1 ]; then
  xenstore-write /global/qvm-hvm-audio-id "$ADxid"
  xenstore-chmod /global/qvm-hvm-audio-id "r*w0"
else
  echo "Not updating, AudioVM not running!"
fi

echo "Wrote $ADxid to /global/qvm-hvm-audio-id and reset perms to r*w0"
```

This should now allow audio to work correctly within HVMs. Unfortunately, attempts to make the script above execute automatically as a libvirt hook only caused the system to hang upon reboot or upon starting up any HVM. Even executing the script above in background results in the system hanging. I suspect this is due to QubesDB or whatever qubes-prefs/qvm-prefs uses hanging while a VM starts up. Also, this script assumes that "default_audiovm" is set to something other than dom0 via `qubes-prefs default_audiovm`. 

So, any additions to this solution is welcome!