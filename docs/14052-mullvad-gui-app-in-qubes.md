This is my first post and also first guide. Welcoming critiques from those more experienced!

I read that some people were having trouble getting wireguard to work with the Mullvad GUI App, so I took a stab at it, and it was just a matter of following an existent [Mullvad guide for qubes](https://mullvad.net/en/help/wireguard-on-qubes-os/) to forward DNS requests properly for wireguard.

Here is a detailed guide, command by command:


In a debian-11-minimal template (with qubes-core-agent-passwordless-root already installed):

`sudo apt install --no-install-recommends wget qubes-core-agent-networking libnss3 libasound2 iproute2 qubes-core-agent-network-manager wireguard openresolv`
`export https_proxy=http://127.0.0.1:8082 && export http_proxy=http://127.0.0.1:8082`
`wget https://mullvad.net/media/mullvad-code-signing.asc`
`gpg --import mullvad-code-signing.asc`
`gpg --edit-key A1198702FC3E0A09A9AE5B75D5A1D4F266DE8DDF`

in gpg:
`trust`
`5` ## _sets to ultimate trust!_
`y`
`q`

now verify & install mullvad:
`wget --trust-server-names https://mullvad.net/download/app/deb/latest`
`wget --trust-server-names https://mullvad.net/download/app/deb/latest/signature`
`gpg --verify MullvadVPN-20xx.x_amd64.deb.asc` ## _make sure you get a good signature_
`sudo apt install -y ./MullvadVPN-20xx.x_amd64.deb`

create a networking app-hvm based on this template & add network-manager service.
boot it and add these rules to /rw/config/qubes-firewall-user-script:

`virtualif=10.137.0.xx` ## _replace 10.137.0.xx with the IP address of your vif interface (IP of qube in qube-manager)_
`vpndns1=10.64.0.1`
`iptables -F OUTPUT`
`iptables -I FORWARD -o eth0 -j DROP`
`iptables -I FORWARD -i eth0 -j DROP`
`iptables -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS  --clamp-mss-to-pmtu`
`iptables -F PR-QBS -t nat`
`iptables -A PR-QBS -t nat -d $virtualif -p udp --dport 53 -j DNAT --to $vpndns1`
`iptables -A PR-QBS -t nat -d $virtualif -p tcp --dport 53 -j DNAT --to $vpndns1`

reboot. should work now. test an app-vm networked to it.
you also probably want to add the mullvad root directory to bind-dirs config to make it persistent, save your login/settings:

`sudo mkdir -p /rw/config/qubes-bind-dirs.d`
add `binds+=( '/etc/mullvad-vpn' )` to /rw/config/qubes-bind-dirs.d/50\_user.conf

reboot and it will be persistent.

NOTE: as many have commented including mullvad-- the app has had bugs and will have bugs... so it is decidedly safer to use a .conf file and another method such as qtunnel. my recommendation is to run the mullvad app behind a qtunnel qube, just in case it does leak, and this will give you an extra wg hop, too.