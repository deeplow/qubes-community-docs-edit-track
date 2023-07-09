I used to run `dnscrypt-proxy` inside of `sys-net` to encrypt and secure dns-requests. Meanwhile I moved the service to a separate `sys-dns` and would like to share the setup with the community. Prerequisite is a `fedora-36-minimal` and `fedora-36-minimal-dvm` with `dnscrypt-proxy` installed and disabled.
```
[user@dom0 ~]$ qvm-clone fedora-36-minimal-dvm fedora-36-minimal-dns
[user@dom0 ~]$ qvm-create -C DispVM --template fedora-36-minimal-dns --label orange sys-dns
[user@dom0 ~]$ qvm-prefs sys-dns netvm sys-net
[user@dom0 ~]$ qvm-prefs sys-dns autostart true
[user@dom0 ~]$ qvm-prefs sys-dns provides_network true
[user@dom0 ~]$ qvm-run -u root fedora-36-minimal-dns xterm
```
Change `/rw/config/rc.local` in `fedora-36-minimal-dns` as follows:
```
[user@fedora-36-minimal-dns]~% cat /rw/config/rc.local
#!/bin/sh

# This script will be executed at every VM startup, you can place your own
# custom commands here. This includes overriding some configuration in /etc,
# starting services etc.

# Example for overriding the whole CUPS configuration:
#  rm -rf /etc/cups
#  ln -s /rw/config/cups /etc/cups
#  systemctl --no-block restart cups

# allow redirects to localhost
/usr/sbin/sysctl -w net.ipv4.conf.all.route_localnet=1
/usr/sbin/iptables -I INPUT -i vif+ -p tcp --dport 53 -d 127.0.0.1 -j ACCEPT
/usr/sbin/iptables -I INPUT -i vif+ -p udp --dport 53 -d 127.0.0.1 -j ACCEPT

# redirect dns-requests to localhost
/usr/sbin/iptables -t nat -F PR-QBS
/usr/sbin/iptables -t nat -A PR-QBS -d 10.139.1.1/32 -p udp -m udp --dport 53 -j DNAT --to-destination 127.0.0.1
/usr/sbin/iptables -t nat -A PR-QBS -d 10.139.1.1/32 -p tcp -m tcp --dport 53 -j DNAT --to-destination 127.0.0.1
/usr/sbin/iptables -t nat -A PR-QBS -d 10.139.1.2/32 -p udp -m udp --dport 53 -j DNAT --to-destination 127.0.0.1
/usr/sbin/iptables -t nat -A PR-QBS -d 10.139.1.2/32 -p tcp -m tcp --dport 53 -j DNAT --to-destination 127.0.0.1

# set /etc/resolv.conf and start dnscrypt-proxy
echo "nameserver 127.0.0.1" > /etc/resolv.conf
/usr/bin/systemctl start dnscrypt-proxy.service
```
If you want to configure `dnscrypt-proxy` the easiest way to achieve persitance is doing that in the template:
```
[user@dom0 ~]$ qvm-run -u root fedora-36-minimal xterm
```
From my point of view the most interesting settings are located in the following files:
```
[user@fedora-36-minimal]~% nano /etc/dnscrypt-proxy/dnscrypt-proxy.toml 
[user@fedora-36-minimal]~% nano /etc/dnscrypt-proxy/captive-portals.txt 
[user@fedora-36-minimal]~% nano /etc/dnscrypt-proxy/cloaking-rules.txt
```
I.e. you need to have
```
listen_addresses = ['127.0.0.1:53']
```
set in `/etc/dnscrypt-proxy/dnscrypt-proxy.toml`. I disabled `systemd-resolved` in the template, it might be possible to deinstall it. Actually I like systemd but sometimes systemd (and others like NetworkManager) do stuff in the background which I do not fully understand. 

After setting everything up to your needs `fedora-36-minimal-dns` and `fedora-36-minimal` have to be shutdown. Then start `sys-dns` and point `sys-firewall` to `sys-dns`:
```
[user@dom0 ~]$ qvm-shutdown fedora-36-minimal
[user@dom0 ~]$ qvm-shutdown fedora-36-minimal-dns
[user@dom0 ~]$ qvm-start sys-dns
[user@dom0 ~]$ qvm-prefs sys-firewall netvm sys-dns
```