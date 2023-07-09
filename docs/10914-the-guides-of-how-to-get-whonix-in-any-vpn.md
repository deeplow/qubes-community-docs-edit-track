As many people using qubes as their daily driver, including Tor usage, all of these information that I may advice you about the following warnings:
1. All your TOR traffic will redirect to other providers (Servers) may blocked by them
2. Make sure all of your TOR traffic went to your well-trusted and well-secured VPN provider/facility by your own trust
3. Make sure your VPN providers don't IP log (This is a top of the line and state of the art advice of how I browse the darknet)

Here comes the real part of the guide:
### Installation
1. In your template qube, install your VPN provider ( let's use RiseupVPN)
> $ sudo snap install --classic riseup-vpn

If you don't have snap, please use the following
Fedora:
> $ sudo dnf install snapd

Debian based:
> $ sudo apt install snapd

2. After you installed that, the following things made you possible with ease:
  a. create a qube that is part of your installation template
  b. in the qubes settings, goes to the APPLICATIONS tab, find your VPN. Notes: you may refresh the application menu by the following command in DOM0 terminal:
> $ qvm-sync-appmenus [your template VM name]

  c. select your VPN client from the available side to the selected side via clicking the single arrow symbol pointing to the right.
  d. EXTRA (This step is optional) turn down your max memory down to 1000M
  e. in the advanced tab, find the section called Other, select Provides network. This is to let other qubes to connect this newly created qube.
  f. select OK, this is the similar version of APPLY button but saves faster

3. After the above steps, the followings are the qube networks for the TOR
  a. select back to the newly created qube settings
  b. in advanced tab, find Memory/CPU section, turn your vCPUs from the default of 2 into 4
  c. (advanced, but not annoyance) in the Basic tab, click Start qube automatically on boot
  d. click OK

4. in your newly created qube, consider the following steps:
  a. in your qubes app menu, find your newly created qube and select your VPN client and wait
  b. once been popped up, start using it

Conclusion:
It was a somewhat difficult tasks to do in order to have the vpn working with you at all time. As an advice, the best way to segregate your traffic is to clone your existed firewall qube to avoid any qube crashes, if has it, that may totally reset your TOR traffic. As a result, you don't have any annoyance from that alone.