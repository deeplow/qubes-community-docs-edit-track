Trezor's instructions didn't work for me on 4.1. The main problem was that the qubes rpc script needs to be executable. The documentation here https://wiki.trezor.io/Qubes_OS is also using the pre-4.1 policy format, and I ran into some weird stuff getting the bridge software itself, so I made this guide, which I hope makes it to the trezor wiki somehow.

# First you need the bridge software. 
## if you want to use their rpm
You can go to suite.trezor.io/web for the prompt to download the latest bridge, or you can `wget https://wallet.trezor.io/data/bridge/2.0.27/trezor-bridge-2.0.27-1.x86_64.rpm` This is not the latest version of trezord, it is a few years old and signed with Pavol's key that I managed to track down (shame on you satoshilabs!), but it looks like not much has changed in trezord since, and the old bridge does work with the current suite. Get Pavol's key `wget rusnak.io/public/pgp.txt` and verify the rpm
```
sudo rpm --import pgp.txt
rpm --checksig trezor-bridge-2.0.27-1.x86_64.rpm
> trezor-bridge-2.0.27-1.x86_64.rpm: digests signatures OK
```
I didn't want to install the rpm in a template, rather just in sys-usb. I made this persistent by replicating what the installation does in rc.local
```
# in a trusted vm you use to get and verify the rpm
sudo dnf install trezor-bridge-2.0.27-1.x86_64.rpm
rpm -qlp trezor-bridge-2.0.27-1.x86_64.rpm
> /lib/udev/rules.d/50-trezor.rules
> /usr/bin/trezord
> /usr/lib/systemd/system/trezord.service
qvm-copy /lib/udev/rules.d/50-trezor.rules /usr/bin/trezord /usr/lib/systemd/system/trezord.service #to sys-usb
# now in sys-usb
sudo mkdir /rw/config/trezor
sudo mv QubesIncoming/trusted/* /rw/config/trezor
```
Then add the following to /rw/config/rc.local to run on startup
```
# /rw/config/rc.local on sys-usb
ln -s /rw/config/trezor/trezord /usr/bin/trezord
ln -s /rw/config/trezor/50-trezor.rules /lib/udev/rules.d/50-trezor.rules
ln -s /rw/config/trezor/trezord.service /usr/lib/systemd/system/trezord.service
ln -s /rw/config/trezor/qubes.Trezor /etc/qubes-rpc/qubes.Trezor
# add user that systemctl service is configured to use
useradd trezord
systemctl start trezord
```
and finally create the executable for the qubes rpc calls by writing the following into `/rw/config/trezor/qubes.Trezor`
```
#!/bin/sh
socat - TCP:localhost:21325
```
and make it executable `sudo chmod +x /rw/config/trezor/qubes.Trezor`
## if you want to build a recent version of trezord
either to have the latest version, to have built the binary from source, or both, then do the following in a fresh vm with network
```
# install go from the link here https://go.dev/doc/install currently:
wget https://go.dev/dl/go1.18.1.linux-amd64.tar.gz
tar -xzf go1.18.1.linux-amd64.tar.gz
mv go ~/.local
echo 'export PATH="$PATH:/home/user/.local/go"' >> ~/.bashrc
source ~/.bashrc
mkdir buildtrezord
cd buildtrezord
# follow instructions here https://github.com/trezor/trezord-go
GO111MODULE=auto go get github.com/trezor/trezord-go
GO111MODULE=auto go build github.com/trezor/trezord-go
qvm-copy trezord-go
```
Easy, copy that binary to sys-usb. You still need the udev rules and the systemd service, which you can get from the rpm and verify that they look like this
```
# 50-trezor.rules
# Trezor: The Original Hardware Wallet
# https://trezor.io/
# Put this file into /usr/lib/udev/rules.d

# note - hidraw* lines are not necessary for trezord-go, as we don't use hidraw
# however, it is still necessary for Chrome support of u2f

# Trezor
SUBSYSTEM=="usb", ATTR{idVendor}=="534c", ATTR{idProduct}=="0001", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
KERNEL=="hidraw*", ATTRS{idVendor}=="534c", ATTRS{idProduct}=="0001",  MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"

# Trezor v2
SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="53c0", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="53c1", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
KERNEL=="hidraw*", ATTRS{idVendor}=="1209", ATTRS{idProduct}=="53c1",  MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
```
```
# trezord.service
[Unit]
Description=Trezor Bridge
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/trezord
User=trezord

[Install]
WantedBy=multi-user.target
```
Then just like in the instructions based on the rpm, you need to add the lines to rw/config/rc.local, put `50-trezor.rules` `trezord.service` and the binary you compiled (`trezord-go` which you should rename to `trezord`) in /rw/config/trezor, and create `qubes.Trezor`.

# Make the qubes rpc policy
in dom0, add the following line to /etc/qubes/policy.d/30-user.policy (create the file if it doesn't exist yet)
```
qubes.Trezor * CLIENTVM sys-usb allow
```
where `CLIENTVM` is the vm that you want to have access to the bridge (like to use the trezor suite). You can check the policy documentation if you want to allow more vms or have other rules.

# Make a socket in the client vm
This part is just like in trezor's documentation. Add the following line to /rw/config/rc.local in the client vm to create a socket that listens on the trezord port and forwards standard input/output to the qubes rpc call
```
# /rw/config/rc.local
socat TCP-LISTEN:21325,fork EXEC:"qrexec-client-vm sys-usb qubes.Trezor" &
```

And that's it! At least this works on my machine. When either the trezor suite or the cli tool `trezorctl` makes a request to localhost:21325, it goes through the qrexec to sys-usb, where qubes.Trezor forwards it again with socat. 

You can also do this with a disposable sys-usb in case you connect other devices at some point. In that case, you'll want to install the bridge software in the disposable template, and then point the client vm's rpc calls (and the rpc policy) to the disposable vm, which I found intuitive enough but feel free to ask if it's not.