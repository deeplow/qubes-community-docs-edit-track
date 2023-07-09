I have long bothered by the issue [https://github.com/QubesOS/qubes-issues/issues/7340] .
marmarek recently mentioned that I can debug xen using a USB 3.0 debug cable. I have a hard time trying to make it work, but now I have succeeded.
I have finally reach the point where I can debug the xen on another machine - using USB 3.0 console. Now I record the successful setup here.
Debugee is Thinkpad L15 Gen 2, debug host is Thinkpad T440p. 
Here is the difficulties and notes that the earlier post of marmarek [https://github.com/QubesOS/qubes-issues/issues/6834#issuecomment-1296221396] may not mention:
1. A USB 3.0 debug cable (for example the cable for WinDBG) is required and DIY will mostly fail as most USB A-A cable is 123456789 <-> 123456789 whereas a USB debug cable should be 123456789 <-> zzz489756.
2. In order to make debug environment controllable and stable, one can use LiveCD Ubuntu 22.04 as debug host. By default the LiveCD `/etc/apt/sources.list` does have only main repos and no universe repos, you need to add them if you want to use picocom in ubuntu 22.04 LiveCD.
3. (ignore this) <del>Append `usbcore.autosuspend=-1` to the debug host kernel command line (I am not sure whether this is needed)</del> Using the bind/unbind, the debug host does not need to worry about suspension - as long as the connection is closed (for example peer is sleeping) and the device is unbind (maybe you can unplug the debug cable now), host can suspend.

4. Make sure that your debug host has at least one USB3.0 plug.
5. If USB 3.0 debug does not work, it is a good idea to debug on a LiveCD Ubuntu 22.04 as it has every software and kernel module to let it work definitely. Make sure your machine has at least 2 USB 3.0 port, connect your debug cable on one end, "look for /sys/bus/pci/devices/*/dbc file" (you should go to the correct device and change the asterisk to that device number, for example 00:14.0), and then write "enable" to the `dbc` file (`echo enable > dbc`). Then you plug the other end onto a different USB 3.0 port. The debug info should appear in `dmesg` and `/dev/ttyUSB0` `/dev/ttyDBC0` should appear at your `/dev` directory. If this does not work, most likely your hardware has some problem.
6. In ubuntu 22.04, load `usb_debug` module and install picocom
```
sudo modprobe usb_debug
sudo apt update
sudo apt install picocom
```
7. The `usb_debug` seems not to work when host plugs first and debugee pauses later - When debugee pauses, plug the usb debug cable to host. `sudo dmesg -w` can be useful in both debug host side and debug guest side. If you manages to plug a debugee to debug host, on debug host side, the debugee shows up as a USB device:
```
[12107.070400] usb 4-2: new SuperSpeed USB device number 2 using xhci_hcd
[12107.090923] usb 4-2: LPM exit latency is zeroed, disabling LPM.
[12107.091160] usb 4-2: New USB device found, idVendor=1d6b, idProduct=0010, bcdDevice= 0.00
[12107.091162] usb 4-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[12107.091164] usb 4-2: Product: Debug console
[12107.091166] usb 4-2: Manufacturer: Xen
[12107.091167] usb 4-2: SerialNumber: 0
```
so whenever the debug host side has any problem about usb, you can catch it immediately.
8. xen boot command: remove `console=none` and add `dbgp=xhci@pci00:14.0,share=yes console=vga,xhci loglvl=all guest_loglvl=all` (if your debugee USB 3.0 is at 00:14.0). You can edit the command at grub2 boot menu.
UPDATE: `dbgp=xhci@pci00:14.0,share=yes console=vga,xhci loglvl=all guest_loglvl=all watchdog watchdog_timeout=20` (as suggested by andyhhp)
9. When you edited the command and attempt booting, xen will _pause_ until debug host is ready.
This command is recommended in debug host, so that tthe console will pop out when the debugee is ready:
```
while true; do if [ -e /dev/ttyUSB0 ]; then sudo picocom -b 115200 /dev/ttyUSB0; fi; sleep 1;done
```
Connect the two computers with the USB 3.0 debug cable. You can see that (1) a `Debug console` device appears in `sudo dmesg -w`; (2) xen debug info appears in `picocom`; (3) debugee boots up.
10. You should be very careful when xen is accepting the console input - type 'h' to see why (it is help). If you typed 'r' accidentally, the computer will hard reset and your hard disk will hurt.
11. When Qubes OS fully boots, dom0 log in prompt will appear in the console. You can log in and run `sudo dmesg -w`. It will write dom0 log persistently to the console.
12. Triple `ctrl-a` will switch _input_ between xen and dom0. When you are using `picocom` it is typing `ctrl-a` 6 times since `ctrl-a` is also escape command for `picocom` by default. `picocom -e b` can change the escape combination into `ctrl-b` which can save your fingers from pressing `ctrl-a` 6 times.
13. When you are doing suspend-resume experiments, the USB 3.0 debug device will frequently power off and power on. When you resume, the device may not work. Unplug and plug each time will work. If that works, here is another trick that also works and does not hurt your USB 3.0 plug:
```
root@ubuntu:/sys/bus/pci/drivers/xhci_hcd# echo 0000:00:14.0 > unbind
root@ubuntu:/sys/bus/pci/drivers/xhci_hcd# echo 0000:00:14.0 > bind
root@ubuntu:/sys/bus/pci/drivers/xhci_hcd# 
```
14. In summary of many debug host tricks, here is a script that can save a lot of labor:
```
#!/bin/sh
ADDR=0000:00:14.0
SYSFS_PATH=/sys/bus/pci/drivers/xhci_hcd
WAIT=6
while true
do
	echo "Count $WAIT secs:"
	for i in `seq ${WAIT} -1 1`
	do
		echo -n "$i, "
		sleep 1
	done
	echo "One trial"
	sudo sh -c "echo ${ADDR} > ${SYSFS_PATH}/bind"
	sleep 0.5
	if [ -e /dev/ttyUSB0 ]
	then
		# escape is ctrl-b
		# write to file
		sudo picocom -e b -b 115200 /dev/ttyUSB0 -g log.txt
	fi
	sleep 0.5
	sudo sh -c "echo ${ADDR} > ${SYSFS_PATH}/unbind"
done
```

Also there are many notes that may not apply to the topic.
<details><summary>personal notes</summary>

1. (xen 4.14) xen console command '`*`' will expand to:
`d 0 H I M Q V a c e g i m n q r s t u v z`

2. picocom sometimes echo back data to the debugee (usually the first 128 bytes of the data from debugee) - it is possibly because that serial port connection is not stable. I do not know a good solution on this behavior. This may cause xen to behave crazy and reset the machine when xen is accepting input rather than dom0.

3. code in `<details>` must have at least one additional new line between a html line and a "```" line, otherwise it will not be parsed as code. See:

https://github.com/gettalong/kramdown/issues/155#issuecomment-339779671

</details>