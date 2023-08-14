This guide uses unman's `qubes-sync` to sync directories from multiple qubes to a single qube while using chroots to prevent client qubes from accessing other qubes' files.

The goal of this is to allow for easier backup from a single qube, or to use software like syncthing to keep multiple devices in sync without requiring network access in client qubes.

## Qube creation

Create an appvm to be the **server** qube. In the instructions replace **$SERVERNAME** with the name of this qube.

Create an appvm to be the **client** qube. In the instructions replace **$CLIENTNAME** with the name of this qube.

## Template setup

These instructions should be done in the **template** qube (i.e. debian-11).

Install dependencies:
```sh
sudo apt install openssh-server sshfs
```

Create `/lib/systemd/system/qubes-ssh-forwarder.socket` (note that `ConditionPathExists` is in unman's source, but is removed here):
```
[Unit]
Description=Forward connection to ssh over Qubes RPC

[Socket]
ListenStream=127.0.0.1:840
BindToDevice=lo
Accept=true

[Install]
WantedBy=multi-user.target
```

Create `/lib/systemd/system/qubes-ssh-forwarder@.service`:
```
[Unit]
Description=Forward connection to ssh over Qubes RPC

[Service]
ExecStart=/usr/bin/qrexec-client-vm '' qubes.ssh
StandardInput=socket
StandardOutput=inherit
```

Create `/etc/qubes-rpc/qubes.ssh`:
```
#!/bin/sh
exec socat STDIO TCP:localhost:22
```

Then mark it as executable:
```
sudo chmod +x /etc/qubes-rpc/qubes.ssh
```

Shut down the **template** and (re)start the server and client qubes.

## Set up directories

Run this on **$SERVERNAME**: 
```sh
sudo mkdir -p /rw/syncdir/authorized_keys
```

To make sure that client qubes aren't able to access files outside of their directories, it's important to configure `chroot`:

Create a new file `/rw/syncdir/sshd_config-addition` on **$SERVERNAME**:
```
AuthorizedKeysFile /rw/syncdir/authorized_keys/%u

Match Group sftponly
    ChrootDirectory %h
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PasswordAuthentication no
```

Append this to `/rw/config/rc.local` on **$SERVERNAME**:
```sh
groupadd sftponly
cat /rw/syncdir/sshd_config-addition | sudo tee -a /etc/ssh/sshd_config
```

Restart **$SERVERNAME**

## Add clients

Run this in **$CLIENTNAME**
```sh
# Run this command, accept defaults for no password
ssh-keygen
# Copy the generated key to the server qube
qvm-copy /home/user/.ssh/id_rsa.pub
```

Run this in **$SERVERNAME**:
```sh
# Create user for qube
sudo useradd -g sftponly -s /usr/sbin/nologin -d /rw/syncdir/$CLIENTNAME sync-$CLIENTNAME
# Set up directory for user to chroot to
sudo mkdir /rw/syncdir/$CLIENTNAME
# Set up writable directory for user
sudo mkdir /rw/syncdir/$CLIENTNAME/writable
sudo chown sync-$CLIENTNAME /rw/syncdir/$CLIENTNAME/writable
# Set up ssh keys for user
sudo mv /home/user/QubesIncoming/$CLIENTNAME/id_rsa.pub /rw/syncdir/authorized_keys/sync-$CLIENTNAME
sudo chown root:root /rw/syncdir/authorized_keys/sync-$CLIENTNAME
sudo chmod 644 /rw/syncdir/authorized_keys/sync-$CLIENTNAME
systemctl restart sshd
```

Append this to `/rw/config/rc.local` in **$SERVERNAME**:
```sh
useradd -g sftponly -s /usr/sbin/nologin -d /rw/syncdir/$CLIENTNAME sync-$CLIENTNAME
```

Append this to `/etc/qubes/policy.d/30-user.policy` in **dom0**:
```
qubes.ssh    *    $CLIENTNAME    @default    allow    target=$SERVERNAME
```

Run this in **$CLIENTNAME**
```sh
mkdir /home/user/sync
```

## Connect client to server

Run in **$SERVERNAME**:
```sh
systemctl start sshd
```

Run in **$CLIENTNAME**
```sh
systemctl start qubes-ssh-forwarder.socket
sshfs -p 840 sync-$CLIENTNAME@localhost:/writable /home/user/sync
```

## Start qubes-sync automatically

Append this to `/rw/config/rc.local` on **$SERVERNAME**. **This must come after all `useradd` commands**:
```sh
bash -c "sleep 10 && systemctl restart sshd"
```

Append this to `/rw/config/rc.local` on **$CLIENTNAME**:
```sh
systemctl start qubes-ssh-forwarder.socket
sudo -H -u user -i sshfs -p 840 sync-$CLIENTNAME@localhost:/writable /home/user/sync
```

## Notes
- To let multiple qubes access the same files, append the `id_rsa.pub` for each new qube to `/rw/syncdir/authorized_keys/sync-$CLIENTNAME`. When connecting, use `sshfs` as the user that has access to the directory (use `ls -l` to check ownership of the directory).
- Bind-dirs is not used for `sshd_config`. You may want to set this up instead of appending controls using `rc.local`
- The `sftponly` group and all users are created when the server qube is started. Changing the order that users are created in `rc.local` or adding a new user in the template may change gid or uid for users and break permissions. 
    - If this happens you can either assign uid and gid manually, or `chown` using the new ones.
    - Or instead of creating groups/users/configs on boot, you can modify `sshd_config` and create the group and users in the template (and remove all lines from `rc.local` in **$SERVERNAME**)


Sources:
- <https://github.com/unman/qubes-sync>
- <https://wiki.archlinux.org/title/SFTP_chroot>

---

Is there anything that's unclear or should be changed? Feedback is welcome!