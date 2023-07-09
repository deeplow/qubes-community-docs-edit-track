I'll be quick on this, since I'm away. Hopefully it'll help someone. I'll edit it properly in the weeks ahead.

So, I needed to connect to internet via USB tethering. Here's how I do it.

0. I didn't choose during Qubes OS install `sys-usb` and `sys-net` to be handled together, but separately.
1. I have more than one USB controllers (NOT ports!). 
2. For each controller, I created separate `sys-usb`, preferably based on `minimals`, thus reducing attacking surface.
3. Each `sys-usb` is a-must disposable for security reasons.
4. One of the controllers is strictly dedicated to USB mouse and/or USB keyboard, nothing else can be attached to it.
5. For the noobs, for the other USB controller, in its sys-usb `Settings->Advanced tab "Provides network"` is checked. Let's call that qube - `sys-usb-teth`.
6. Detach any external devices you had on `sys-usb-teth` and restart the qube to bring it to clean state for security reasons.
7. Connect your phone to the qube.
8. When recognized, on the phone enter `"Portable hotspot"` setting, don't turn it on, but only "USB tethering" option.
9. In `sys-usb-teth` terminal now run
>$ sudo NetworkManager

Yes, with privileges.

9. Now check if it's working by running there for example
>$ ping 8.8.8.8

10. If everything is OK, proceed to

11. I have created `sys-firewall-teth` based also on disposable minimal template. Start it and set its NetVm `sys-usb-teth`.
12. I have created `sys-whonix-teth`, and set its netvm` sys-firewall-teth`.
13. Start your browsing `dispVM` and set for its netVM either `sys-whonix-teth`, or `sys-firewall-teth` (tor or clearnet)
14. Everything should work flawlessly.

15. After you finish, disconnect phone and don't forget to restart `sys-usb-teth` before attaching again external devices to it, in order to bring it to clean state for the devices.