# Roadmap on troubleshooting missing wifi in qubes

This is the roadmap on how to wifi troubleshoot. At the steps with [N] i have some additional information that is **really** worth reading before starting down below.

**You right now:**

So you are in the position, that suddently your qubesOS is not connected to your wifi for some reason. It worked once and you did not change anything you can think. No worries, we can fix this.

You first have to determine:

0. **Can you see networks/your network?**

If yes: It "forgot" the network. Add it/reconnect. This may happen again, but will get rarer until it does work 100% of times.

If no:

1. **Does *sys-net* see the the wifi card and recognizes it as such?** (`iwconfig` in *sys-net* should display wifi device[1])

If yes: Restart network manager. (`sudo systemctl restart NetworkManager` in *sys-net* or restart whole qube[3])

If no: 

2. **Is the wificard present as a PCI device in *sys-net*?** (`sudo lspci -v` in *sys-net* should show wifi device[2])

If Yes: Driver issue, what to do is dependend on what `sudo lspci -v` says the card is.

If no:

3. **Can dom0 see the PCI wifi card?** (`sudo lspci -v` [2] in *dom0*).

If yes: Check settings for missing device assignment. Assign card to *sys-net*. Exact commands/device is dependend on output of lspci

If no:

4. **Check bios if card is activated.**

If no: Activate card in bios
If yes:

5. **Try your wifi card with another OS or in another device to determine if it is physically functional**

**Other things one can try and useful stuff:**

* [1]: `iwconfig`: You are looking for some big block of text like this:

```
lo        no wireless extensions.

ens6f0    no wireless extensions.

wls7      IEEE 802.11  ESSID: $ESSID 
          Mode:Managed  Frequency:5.24 GHz  Access Point: FF:FF:FF:FF:FF:FF  
          Bit Rate=866.7 Mb/s   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
          Link Quality=70/70  Signal level=-26 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:18   Missed beacon:0

vif3.0    no wireless extensions.
```

This means, that your system has detected the wifi card and can communicate with it.

If you only have "no wireless extentions." lines, your *sys-net* does not know how to talk to the card (or does not even see it).

* [2]: `sudo lspci -v` may spit out many things. You can grep for your wifi with `sudo lspci -v | grep --before-context 20 --after-context 10 wifi`. This will print the 20 lines before all lines containing "wifi" and the following 10. Usually this is enough to get the device name and address. Here is an example output of what we are looking for.

```
00:06.0 0280: 8086:2723 (rev 1a)
	Subsystem: 8086:0084
	Physical Slot: 6
	Flags: fast devsel, IRQ 40
	Memory at f2024000 (64-bit, non-prefetchable) [size=16K]
	Capabilities: <access denied>
	Kernel modules: iwlwifi
```

It may speed up finding it, but not finding it with that does not necessarily mean it is missing! As you can see, the wifi device can be quite hidden (usually it is not tho). In the worst case you have to go through all devices and determine with your favorite search engine what all the devices are.

* [3] When restarting *sys-net*, the gui will not allow you unless all qubes with networking are shut down. You can use the *dom0* command line and do things anyway like a pro with the command: `qvm-shutdown --wait --force sys-net && qvm-start sys-net` :slight_smile:.
* Using a USB wifi device attached to *sys-net* and see if that works to ensure that the whole setup is "able to wifi".
* **Remove MAC addresses!** Mac addresses are permanent hardware serial numbers that are transmitted and can be received by anybody in range. For that reason they usually are deleted before posting logs or terminal outputs. It is not detrimental if you accidentally posted it, but it is proper OPSEC/privacy to remove them. They look something like: `d4:a5:93:cd:00:b2`. Just change it to `FF:FF:FF:FF:FF:FF` for example, as i did in the iwconfig output.


This would be the whole roadmap through "Wifi not working" as far as i can see to at least narrow down where the problem is.

I wrote this and determined, it might be a good roadmap to post as a standalone guide. Please add your error if this would not be determined by this procedure or help improve this.