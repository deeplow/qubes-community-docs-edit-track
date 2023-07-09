Hi everyone,

It took me a while to figure this procedure out properly, so I thought it might be useful also for others.

Big thanks to @unman who [pointed me in this direction](https://forum.qubes-os.org/t/storage-and-backup-of-large-amounts-of-data/4474) and who wrote [very helpful instructions](https://github.com/unman/qubes-sync) which are the basis of this procedure.

As I'm still new to QubesOS, I'm also curious about feedback/comments from the qubes community on this guide.

**Context**
Let's assume the following qube structure:

* *data1* and *data2*: Offline storage qubes with large amount of data that changes often and needs to be backed up regularly (there could be many more like those)
* *backupsync*: An offline storage qube which is only in charge of collecting the backups and writing them to an external harddrive

The below mechanism lets you efficiently sync the data changes of the data qubes to the backup qube using rsync and qrexec.

Of course, this mechanism is [not as secure as the official QubesOS backup mechanism](https://forum.qubes-os.org/t/how-do-you-organize-your-backups/3986/10?u=qpost135) but probably secure enough in specific cases (depending on the actual threat model, of course).

The guide is using the Fedora templates. On Debian, several commands and package names might be different.


**Step 1: Build the data templates**

* Make a copy of the Fedora 33 Minimal Template and name it "fedora-33-mini-data"
* In Dom0: `qvm-run -u root fedora-33-mini-data xterm`
  * `dnf upgrade`
  * `dnf install rsync-daemon`
  * Write the file `/etc/rsyncd.conf`
```
port = 873

[syncdata]
path = /home/user/
uid=1000
gid=1000
comment = Read-only data to be synced
read only = yes
```
Note: uid/gid are needed to ensure that rsyncd has the same permissions as the default user "user" (who has the id 1000)

  * Write the file `/etc/qubes-rpc-qubes.Rsync`
```
#!/bin/sh
exec socat STDIO TCP:localhost:873
```
  * `systemctl enable rsyncd`
* Shutdown this template VM

**Step 2: Build the appvm "data1"**
* Create a new VM:
  * Name: data1
  * Type: Qube based on template (AppVM)
  * Template: fedora-33-mini-data
  * Networking: None
* In Dom0 run: `qvm-run data1 xterm`
  * `touch /home/user/testdata1.txt`
  * Ensure that the rsync service is running: `systemctl status rsyncd`

**Step 3: Build the appvm "data2"**
* Create a new VM:
  * Name: data2
  * Type: Qube based on template (AppVM)
  * Template: fedora-33-mini-data
  * Networking: None
* In Dom0 run: `qvm-run data2 xterm`
  * `touch /home/user/testdata2.txt`
  * Ensure that the rsync service is running: `systemctl status rsyncd`


**Step 4: Build the "backupsync" template**

* Make a copy of the Fedora 33 Minimal Template and name it "fedora-33-mini-backupsync"
* In Dom0: `qvm-run -u root fedora-33-mini-data xterm`
  * `dnf upgrade`
  * `dnf install rsync`
    * Note: `qubes-core-agent-nautilus`, `cryptsetup` and `lvm2` are useful for mounting an external harddrive with encryption based on luks.
  * Now we create the service and socket files and enable the service for `data1`:
      * Write the file `/lib/systemd/system/qubes-rsync-forwarder1@.service`
```
[Unit]
Description=Forward connection to rsync daemon on data1 over qrexec to port 1837

[Service]
ExecStart=/usr/bin/qrexec-client-vm data1 qubes.Rsync
StandardInput=socket
StandardOutput=inherit
```

   * Write the file `/lib/systemd/system/qubes-rsync-forwarder1.socket`

```
[Unit]
Description=Forward connection to rsync daemon on test-server1 over qrexec to port 1837

[Socket]
ListenStream=127.0.0.1:1837
BindToDevice=lo
Accept=true

[Install]
WantedBy=multi-user.target
```
    * `systemctl enable qubes-rsync-forwarder1.socket`
  * Now we create the service and socket files and enable the service for `data2`:
    * Write the file `/lib/systemd/system/qubes-rsync-forwarder2@.service`
```
[Unit]
Description=Forward connection to rsync daemon on data2 over qrexec to port 2837

[Service]
ExecStart=/usr/bin/qrexec-client-vm data2 qubes.Rsync
StandardInput=socket
StandardOutput=inherit
```

  * Write the file `/lib/systemd/system/qubes-rsync-forwarder2.socket`

```
[Unit]
Description=Forward connection to rsync daemon on test-server2 over qrexec to port 2837

[Socket]
ListenStream=127.0.0.1:2837
BindToDevice=lo
Accept=true

[Install]
WantedBy=multi-user.target
```
    * `systemctl enable qubes-rsync-forwarder2.socket`
* Shutdown this template VM

**Step 5: Set the RPC policy in Dom0**
* Allow the RPC-based communication between those VMS by creating this file: `/etc/qubes-rpc/policy/qubes.Rsync`

```
backupsync data1 allow
backupsync data2 allow
```

**Step 6: Build the appvm "backupsync"**
* Create a new VM:
  * Name: backupsync
  * Type: Qube based on template (AppVM)
  * Template: fedora-33-mini-backupsync
  * Networking: None

**Step 7: Trigger the backup**
* In Dom0 run: `qvm-run backupsync xterm`
  * Ensure that the data1 rsync service is running: `systemctl status qubes-rsync-forwarder1.socket`
  * Ensure that the data2 rsync service is running: `systemctl status qubes-rsync-forwarder2.socket`
  * Mount a luks encrypted external harddrive in this vm
  * Navigate to the directory where this harddrive is mounted and execute rsync to synchronize the data (of course, you can synchronize the data into two different directories):
    * `rsync -a --delete --stats --port=1837 localhost:syncdata`
    * `rsync -a --delete --stats --port=2837 localhost:syncdata`

**Step 8**
Enjoy the feeling of having a fast and reasonably secure backup mechanism for your large data :slightly_smiling_face: