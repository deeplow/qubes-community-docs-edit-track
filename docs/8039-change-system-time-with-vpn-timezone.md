Hi there,

Using VPN,  testing https://whoer.net, getting message:

Your disguise: 90% Minor remarks regarding your anonymity and security

-10% System time different
The time set in your system differs from your IP addresses time zone. You are possibly trying to hide your current location by anonymity means.

Is there an automated way to change the time in every AppVM? For example:
sys-net <-> sys-firewall0 <-> sys-VPN0 <-> ... <-> sys-VPNx <-> sys-firewall1 <-> AppVM

How do I have every AppVM check the time of the VPN-exit-node and change it's system time accordingly?
Secondly: how do I make AppVM check the time every minute or so and change it's system time whenever I change VPN-exit-node?

Thanks,
Cheers