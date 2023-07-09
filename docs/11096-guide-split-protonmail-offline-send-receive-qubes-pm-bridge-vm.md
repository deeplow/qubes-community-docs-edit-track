## INTRODUCTION
Hello all.

The goal of this guide is to provide you with a split-protonmail setup made of a minimal mail template and three AppVMs: `protonmail-bridge`, `mail-receive`, and `mail-send`.

This will allow you to effectively separate incoming and outgoing mail (into non-networked qubes), and your protonmail credentials (security by compartmentalization).

This guide was inspired by a [Reddit post](https://web.archive.org/web/20210630065228/https://www.reddit.com/r/Qubes/comments/oarnuj/qubes_os_protonmail_bridge_paranoid_isolation_my/) to which I made some modifications, since the configuration proposed in the original post didn't quite work for me.

I hope this guide can help some of you.

Note 1: I'm not an expert, so I'm sharing what worked for me. If you have suggestions or modification proposals, feel free to post them.
Also, feel free to let me know if I've made any mistake so I can update this post accordingly.

Note 2: Protonmail Bridge is currently only available to Protonmail paid accounts.

## 1. Mail template
Note 1: if you don't want to create a dedicated template, just make sure that the required software is installed in your template of choice. Personally, I prefer to create a template for each purpose.

Note 2: you can take this a step further by creating a template for Protonmail bridge, and another one for Thunderbird. For simplicity, in this example, I use only one template for both purposes.

Note 3: I'm using a `debian-11-minimal` template, I haven't tested this setup with Fedora.

1. Install the official minimal template as instructed in the Qubes Documentation: https://www.qubes-os.org/doc/templates/minimal/
2. Clone the minimal template:
```
[user@dom0]$ qvm-clone debian-11-minimal debian-11-protonmail
```
3. Update the new clone:
Note 1: those of you who set up a `apt-cacher-ng` qube might need to update the urls of the repositories. Expand the section below for the commands

[details="Howto: Update repo urls to work with `apt-cacher-ng`"]
```
[root@debian-11-protonmail]# sed -i 's#https://#http://HTTPS///#g' /etc/apt/sources.list
[root@debian-11-protonmail]# sed -i 's#https://#http://HTTPS///#g' /etc/apt/sources.list.d/*.list
```
[/details]
```
[root@debian-11-protonmail]# apt update && apt full-upgrade -y
```
4. Create a `packages.txt` file, type them or use whatever method you prefer to install the following packages:

[details="packages.txt"]
```
fonts-dejavu
gnome-keyring
libblockdev-crypto2
libgpgme11
libpulse-mainloop-glib0
libqt5core5a
libqt5gui5
libqt5network5
libqt5qml5
libqt5svg5
libqt5widgets5
qubes-core-agent-networking
qubes-thunderbird
thunderbird
wget
```
[/details]

```
[root@debian-11-protonmail]# apt install -y --no-install-recommends $(cat packages.txt)
```
5. Download and install Protonmail Bridge, then shutdown the qube:
Note 1: those of you who set up a `apt-cacher-ng` qube might need to change the protonmail url from `https://protonmail.com` to `http://HTTPS///protonmail.com`
Note 2: if you're using Fedora, you will need to check the [Protonmail website](https://protonmail.com/support/knowledge-base/protonmail-bridge-install/) for the appropriate package.
```
[root@debian-11-protonmail]# https_proxy=http://127.0.0.1:8082/ http_proxy=http://127.0.0.1:8082/ wget https://protonmail.com/download/bridge/protonmail-bridge_2.1.1-1_amd64.deb
[root@debian-11-protonmail]# dpkg -i protonmail-bridge_*_amd64.deb && shutdown
```

## 2. AppVM: protonmail-bridge
This qube will only run protonmail bridge and will be the only one with a netvm assigned. This example uses sys-whonix, feel free to pick your netvm of choice.

Note 1: Keep in mind that if you pick a different name than `protonmail-bridge` you will have to adjust some parameters in the following steps.

Note 2: I included a maxmem value that works for me. You can always adjust as needed.
1. Create the qube:
```
[user@dom0]$ qvm-create --class=AppVM --template=debian-11-protonmail --label=blue protonmail-bridge
[user@dom0]$ qvm-prefs protonmail-bridge maxmem 900
[user@dom0]$ qvm-prefs protonmail-bridge netvm sys-whonix
```
2. Optional: set firewall to **Limit outgoing connections to**:
    - `protonmail.ch`
    - `protonmail.com`
3. Create the policies:
```
[root@protonmail-bridge]# mkdir -p /rw/usrlocal/etc/qubes-rpc
[root@protonmail-bridge]# echo 'socat STDIO TCP:localhost:1143' > /rw/usrlocal/etc/qubes-rpc/user.protonmail-imap
[root@protonmail-bridge]# echo 'socat STDIO TCP:localhost:1025' > /rw/usrlocal/etc/qubes-rpc/user.protonmail-smtp
```
4. Optional: add Protonmail Bridge to appmenu
```
[user@dom0]$ qvm-features protonmail-bridge menu-items protonmail-bridge.desktop
[user@dom0]$ qvm-sync-appmenus protonmail-bridge
```
5. Shutdown the VM:
```
[user@dom0]$ qvm-shutdown protonmail-bridge
```

## 3. AppVM: mail-receive
This qube will only be able to receive mail and will not be connected to a netvm.
1. Create the qube:
```
[user@dom0]$ qvm-create --class=AppVM --template=debian-11-protonmail --label=green mail-receive
[user@dom0]$ qvm-prefs protonmail-receive maxmem 900
[user@dom0]$ qvm-prefs protonmail-receive netvm ''
```
2. Add the startup command:
```
[root@mail-receive]# echo 'qvm-connect-tcp ::1143' >> /rw/config/rc.local
```
3. Optional: add Thunderbird to appmenu
```
[user@dom0]$ qvm-features mail-receive menu-items thunderbird.desktop
[user@dom0]$ qvm-sync-appmenus mail-receive
```
4. Shutdown the VM:
```
[user@dom0]$ qvm-shutdown mail-receive
```

## 4. AppVM: mail-send
This qube will only be able to send mail and will not be connected to a netvm.
1. Create the qube:
```
[user@dom0]$ qvm-create --class=AppVM --template=debian-11-protonmail --label=red mail-send
[user@dom0]$ qvm-prefs protonmail-send maxmem 900
[user@dom0]$ qvm-prefs protonmail-send netvm ''
```
2. Add the startup command:
```
[root@mail-send]# echo 'qvm-connect-tcp ::1025' >> /rw/config/rc.local
```
3. Optional: add Thunderbird to appmenu
```
[user@dom0]$ qvm-features mail-send menu-items thunderbird.desktop
[user@dom0]$ qvm-sync-appmenus mail-send
```
4. Shutdown the VM:
```
[user@dom0]$ qvm-shutdown mail-send
```

## 5. dom0 policies
These policies allow communications between the relevant qubes: specifically, the `mail-receive` qube will be able to fetch email automatically, while the `mail-send` qube will require an extra user prompt. This set up may or may not be desirable for you, so feel free to experiment.
```
[root@dom0]# echo "mail-receive protonmail-bridge allow,target=protonmail-bridge" >> /etc/qubes-rpc/policy/user.protonmail-imap
[root@dom0]# echo "mail-send protonmail-bridge ask,default_target=protonmail-bridge" >> /etc/qubes-rpc/policy/user.protonmail-smtp
[root@dom0]# echo "mail-receive @default allow,target=protonmail-bridge" >> /etc/qubes-rpc/policy/qubes.ConnectTCP
[root@dom0]# echo "mail-send @default ask,default_target=protonmail-bridge" >> /etc/qubes-rpc/policy/qubes.ConnectTCP
```

## 6. Final configurations
1. Start `protonmail-bridge`, login with your Protonmail credentials and make sure that the bridge is set to run on startup (there's an option in the app settings).
2. Start `mail-receive`, add an account on Thunderbird with the credentials provided by Protonmail bridge (**NOT your actual Protonmail credentials!**). For IMAP use server `127.0.0.1`, port `1143`. For SMTP use `0.0.0.0`. Connection security: `STARTTLS`, `Normal Password`. Then click on `Advanced settings` to save, and fetch mail.
3. Start `mail-send`, add an account on Thunderbird with the credentials provided by Protonmail bridge (**NOT your actual Protonmail credentials!**). For IMAP use server `0.0.0.0`. For SMTP use server `127.0.0.1`, port `1025`. Connection security: `STARTTLS`, `Normal Password`. Then click `Advanced settings` to save.
4. `mail-send` requires that you approve the Protonmail certificate: you'll receive a prompt the first time you attempt to send an email.