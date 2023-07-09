Good news, with fedora-38 the network manager supports Wireguard out of the box!
The only thing required are extra firewall rules in the VPN qube, as explained in [the community documentation about VPN](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/vpn.md).

## What you'll need
This guide assumes you are using a VPN service that has wireguard support. For example, ProtonVPN and Mullvad VPN do support it. But you can also follow this guide to add any other (even your own).

## Create a new qube providing network
> :information_source:  Make sure `fedora-38` template is installed ([instructions](https://www.qubes-os.org/doc/templates/fedora/#installing))

Menu » Qubes Tools » Create Qubes VM:
- **name**: sys-vpn (you pick yours)  
- **template:** `fedora-38`  
- **type:** `app qube` (or AppVM)  
-  ☑️ Launch settings after creation
- <kbd>advanced</kbd> (tab) » Provides network access to other qubes

And then <kbd>OK</kbd>. Then the qube settings window should show up (procced to the next step).
### Enable service “network-manager” in sys-vpn
![add|690x64, 75%](upload://2r8q1bkftaD2vQhv6yWrswwhllL.png)

In the settings windown that popped up, go to the <kbd>Services</kbd>, select `network-manager` from the drop-down list and click <kbd>:heavy_plus_sign: add</kbd>. Then save the settings by clicking <kbd>OK</kbd>.

## Get your wireguard VPN configuration file
Go your VPN provider and either get a download a configuration file **for wireguard** (e.g.: `vpn.conf`)
On your VPN provider download the **wireguard** configuration for the server you want to connect to.

Here are the download pages for some popular VPN services: [Mullvad](https://mullvad.net/en/account/wireguard-config), [ProtonVPN](account.proton.me/u/0/vpn/WireGuard)

## Use the Qube GUI to set the firewall to the VPN endpoint (this avoids leaks)

> :information_source: This is essentially a **killswitch**. It is a fail-safe that ensures that if your VPN connection fails, it does let anything through.

Open the configuration file in a text editor and take note of the IP address in right next to `Endpoint`. If the line looks like the following, then you take note of the IP address as `1.2.3.4`. 
>   ```
>   Endpoint = 1.2.3.4:5555
>   ```

Open the qube settings for `sys-vpn` and navigate to the <kbd>Firewall rules</kbd> tab and set <kbd>:radio_button: Limit outgoing connections to</kbd>.

![firewall|690x133](upload://aOddjpqb61Fu1tF3A65GTywvrAk.png)

Then click on  <kbd> :heavy_plus_sign:</kbd> to add a new firewall and add your saved IP address(es)

![ip|375x172, 75%](upload://rrxJUKcOlwO37Psto41J4KQ1t1C.png)


Hit <kbd>OK</KBD> to apply and click <kbd>OK</KBD> again to apply the settings

## Configure your VPN in the Network Manager
On the qube on which you downloaded your wireguard configuration (e.g.: `vpn.conf`), open the file explorer where the file was saved. Then right-click a file and <kbd>Copy to another AppVM</kbd> and choose to `sys-vpn` as the target.

Open your file manager in `sys-vpn` and find the `<NAME>.conf` file you just copied. It should in the directory `QubesIncoming`. Move it to your home directory.

Open the `Terminal` application on your `sys-vpn` qube and run the following command (replacing `<NAME>.conf` with the correct name of the file):

```text
nmcli connection import type wireguard file vpn.conf
```

If successful, you should see a notification about successful connection. If that doesn't happen, something may be wrong with your config file:

![oppp|412x210](upload://fQlyyzTGsMXgW1VuY0On9IWm5Ne.png)


> :information_source: You should also see an icon with a padlock ![oppp(1)|22x22](upload://kRH6Pr00qtxThM8rkJIosNbq3EL.png)  in the top-right corner of your screen (system tray). This indicates that your VPN connection is active. Without a padlock, means that it failed to connect.

## Assign a VM to the new Qube network to use the VPN

Now that the VPN is configured, for each qube that you want to connect to the VPN, open its settings and set `networking` to `sys-vpn`.  If you want this to be the default net qube, then you can set it in the Qubes Global Settings.

After that you're done :partying_face:


## Hardening (optional)

> :information_source: TODO explain why this is needed

Add the rules below in `/rw/config/qubes-firewall-user-script` in `sys-vpn`:

```
# Prevent the qube to forward traffic outside of the VPN
iptables -I FORWARD -o eth0 -j DROP
iptables -I FORWARD -i eth0 -j DROP
ip6tables -I FORWARD -o eth0 -j DROP
ip6tables -I FORWARD -i eth0 -j DROP

# Redirect all the DNS traffic to the preferred DNS server
DNS=9.9.9.9
iptables -t nat -A PR-QBS -i vif+ -p udp --dport 53 -j DNAT --to "$DNS"
iptables -t nat -A PR-QBS -i vif+ -p tcp --dport 53 -j DNAT --to "$DNS"
```

<div data-theme-toc="true"> </div>