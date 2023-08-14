## Introduction
This guide describes setting up a `sys-proxy` qube, which will transparently route the traffic of qubes using it as their networking qube through a SOCKS5, HTTP(S) or [other supported](https://dreamacro.github.io/clash/configuration/outbound.html#proxies) proxy.

## Requirements
1. Qubes OS R4.1 or R4.2
2. A proxy server (SOCKS5, HTTP(S), Shadowsocks)

## Setup

### Setting up the template
We'll be using a minimal Fedora template. To install it, run in **`dom0`**:
`sudo qubes-dom0-update qubes-template-fedora-38-minimal`

After it has finished installing, open the Qubes update tool in `dom0`, enable `Enable updates for qubes without known available updates`, check `fedora-38-minimal` and hit next, wait for it to finish updateing.

Open Qube Manager, find `fedora-38-minimal`, right-click it, choose `Clone qube`, name it `fedora-38-minimal-proxy` and hit OK.

Open a terminal window in **`dom0`**, open up a root terminal in the cloned template:
`qvm-run -u root fedora-38-minimal-proxy xterm`

Install the necessary software **in the template** by running in the opened terminal window of the template:
```sh
dnf install qubes-core-agent-networking iproute clash dnscrypt-proxy
systemctl disable dnscrypt-proxy
poweroff
```

### Creating `sys-proxy` qube

Open the Qube creation tool and configure the qube as follows:
 * Name: sys-proxy
* Type: AppVM
* Template: `fedora-38-minimal-proxy`
* Networking: this is for you to decide, perhaps you want to use a VPN qube, default is `sys-firewall`

Tick `Launch settings after creation` and hit OK
Select tab Advanced, tick `Provides network`
click Apply and then OK

Launch a terminal in **`dom0`** and run:
```sh
qvm-firewall sys-proxy del --rule-no 0
qvm-firewall sys-proxy add drop
qvm-firewall sys-proxy add --before 0 drop proto=icmp
qvm-firewall sys-proxy add --before 0 drop specialtarget=dns
qvm-firewall sys-proxy add --before 0 accept PROXY_IP
qvm-firewall sys-proxy
```
replace `PROXY_IP` with your proxy’s IP
last command should show accept → drop DNS → drop ICMP → drop

### Configuring `sys-proxy` qube

Open `sys-proxy`'s terminal by running in **`dom0`**:
`qvm-run -u root sys-proxy xterm`

In **`sys-proxy`**'s terminal run: `mkdir -p /rw/proxy/dns /rw/proxy/clash`

Edit `/rw/proxy/dns/dnscrypt-proxy.toml` in `sys-proxy` and add:
```
listen_addresses = ['127.0.0.1:5353']
max_clients = 250
proxy = 'socks5://127.0.0.1:7891'
timeout = 5000
keepalive = 30
ignore_system_dns = true
netprobe_timeout = 0
cache = true
[static]
  [static.quad9_doh]
    stamp = 'sdns://AgMAAAAAAAAABzkuOS45LjkgKhX11qy258CQGt5Ou8dDsszUiQMrRuFkLwaTaDABJYoSZG5zOS5xdWFkOS5uZXQ6NDQzCi9kbnMtcXVlcnk'
  [static.mullvad_doh]
    stamp = 'sdns://AgcAAAAAAAAAAAAPZG9oLm11bGx2YWQubmV0Ci9kbnMtcXVlcnk'
```

Edit `/rw/proxy/clash/config.yaml` in `sys-proxy` and add:
```
socks-port: 7891
redir-port: 7892

mode: rule

allow-lan: true
bind-address: '*'

dns:
  enable: false

proxies:
  - name: "socks_proxy"
    type: socks5
    server: PROXY_IP
    port: 1080
    # username: username
    # password: password
  # - name: "http_proxy"
  #   type: http
  #   server: PROXY_IP
  #   port: 80
  #   # username: username
  #   # password: password
  #   # tls: true # https
  #   # skip-cert-verify: true

rules:
  - MATCH,socks_proxy # or http_proxy
```
Replace `PROXY_IP` and with your proxy’s IP, modify proxy settings as needed

#### For Qubes R4.1
Edit `/rw/config/rc.local` in `sys-proxy` and add:
```sh
sysctl -w net.ipv4.conf.all.route_localnet=1
iptables -I FORWARD -o eth0 -j DROP
iptables -I FORWARD -i eth0 -j DROP
ip6tables -I FORWARD -o eth0 -j DROP
ip6tables -I FORWARD -i eth0 -j DROP
iptables -P OUTPUT DROP
iptables -A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -d PROXY_IP -j ACCEPT
iptables -t nat -F PR-QBS
iptables -t nat -A PR-QBS -d 10.139.1.1 -p udp --dport 53 -j DNAT --to 127.0.0.1:5353
iptables -t nat -A PR-QBS -d 10.139.1.1 -p tcp --dport 53 -j DNAT --to 127.0.0.1:5353
iptables -t nat -A PR-QBS -d 10.139.1.2 -p udp --dport 53 -j DNAT --to 127.0.0.1:5353
iptables -t nat -A PR-QBS -d 10.139.1.2 -p tcp --dport 53 -j DNAT --to 127.0.0.1:5353
iptables -t nat -A PREROUTING -i vif+ -p udp -j REDIRECT --to-ports 7892
iptables -t nat -A PREROUTING -i vif+ -p tcp -j REDIRECT --to-ports 7892
iptables -I INPUT -i vif+ -p tcp --dport 7892 -j ACCEPT
iptables -I INPUT -i vif+ -p udp --dport 7892 -j ACCEPT
iptables -I INPUT -i vif+ -p tcp --dport 5353 -j ACCEPT
iptables -I INPUT -i vif+ -p udp --dport 5353 -j ACCEPT
clash -d /rw/proxy/clash >/dev/null 2>&1 &
sleep 0.5
dnscrypt-proxy -config /rw/proxy/dns/dnscrypt-proxy.toml >/dev/null 2>&1 &
```
Replace `PROXY_IP` and with your proxy’s IP

#### For Qubes R4.2
Edit `/rw/config/rc.local` in `sys-proxy` and add:
```sh
sysctl -w net.ipv4.conf.all.route_localnet=1
nft 'add rule ip qubes custom-forward oifname "eth0" drop'
nft 'add rule ip6 qubes custom-forward oifname "eth0" drop'
nft 'add rule ip qubes custom-forward iifname "eth0" drop'
nft 'add rule ip6 qubes custom-forward iifname "eth0" drop'
nft flush chain ip qubes dnat-dns
nft 'add rule ip qubes dnat-dns ip daddr 10.139.1.1 udp dport 53 dnat to 127.0.0.1:5353'
nft 'add rule ip qubes dnat-dns ip daddr 10.139.1.1 tcp dport 53 dnat to 127.0.0.1:5353'
nft 'add rule ip qubes dnat-dns ip daddr 10.139.1.2 udp dport 53 dnat to 127.0.0.1:5353'
nft 'add rule ip qubes dnat-dns ip daddr 10.139.1.2 tcp dport 53 dnat to 127.0.0.1:5353'
nft 'add rule ip qubes custom-input iifname "vif*" tcp dport 7892 accept'
nft 'add rule ip qubes custom-input iifname "vif*" udp dport 7892 accept'
nft 'add rule ip qubes custom-input iifname "vif*" tcp dport 5353 accept'
nft 'add rule ip qubes custom-input iifname "vif*" udp dport 5353 accept'
nft 'add chain ip qubes redir { type nat hook prerouting priority -99 ; policy accept; }'
nft 'add rule ip qubes redir iifname "vif*" ip protocol udp redirect to :7892'
nft 'add rule ip qubes redir iifname "vif*" ip protocol tcp redirect to :7892'
nft 'add chain ip qubes output { type filter hook output priority filter ; policy drop; }'
nft 'add rule ip qubes output ct state related,established accept'
nft 'add rule ip qubes output oifname "lo" accept'
nft 'add rule ip qubes output ip daddr PROXY_IP accept'
clash -d /rw/proxy/clash >/dev/null 2>&1 &
sleep 0.5
dnscrypt-proxy -config /rw/proxy/dns/dnscrypt-proxy.toml >/dev/null 2>&1 &
```
Replace `PROXY_IP` and with your proxy’s IP
#### End of Qubes version specific instructions

Download `Country.mmdb` from [here ](https://cdn.jsdelivr.net/gh/Dreamacro/maxmind-geoip@release/Country.mmdb) in another qube, move it to `sys-proxy`’s `/rw/proxy/clash` directory.
It doesn't actually get used, but the proxy client refuses to start without it, meaning it doesn't have to be kept up-to-date.

Last but not least, **restart** `sys-proxy`!

### Using `sys-proxy`
After having restarted `sys-proxy`, you can create a new qube that uses `sys-proxy` as its networking qube.
To test if it's indeed working, in the new qube `curl https://ip.me` should show the proxy's IP address.

## Notes
* `clash`, the proxy client used, also supports other proxy protocols such as Shadowsocks in addition to SOCKS5 and HTTP(S), see [their documentation](https://dreamacro.github.io/clash/configuration/outbound.html#proxies) for more details.
* `dnscrypt-proxy`, the DNS client used, is being used with a minimal configuration that has two preconfigured DNS servers: Quad9's and Mullvad's DoH servers. You can also configure sources for lists of DNS servers, but make sure to preserve the custom configuration in our `dnscrypt-proxy.toml` file (before `[static]`). See their [documentation](https://github.com/DNSCrypt/dnscrypt-proxy/wiki) and [example config file](https://github.com/DNSCrypt/dnscrypt-proxy/blob/master/dnscrypt-proxy/example-dnscrypt-proxy.toml) for details.
* It should be leak-proof, since `qvm-firewall` is used to block all traffic of all kinds from `sys-proxy` to any non-proxy IPs.