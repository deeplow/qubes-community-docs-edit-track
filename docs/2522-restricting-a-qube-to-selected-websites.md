A common requirement seems to be the ability to restrict a qube's access to a certain subset of websites; something that is difficult to achieve using the firewall rules due to multi-hosted websites/CDN's etc.

The following is a description of *one* way to setup a qube with restricted website access using only software that is already installed in Qubes OS.

Create a qube based on template:fedora-32 or fedora-33, lets call it **my-proxy**. Set its networking to **sys-firewall**.

![Screenshot_2021-03-12_16-46-28|624x328](upload://a9BobSbJ88PCmRBlRBOmg5opcci.png) 

Open **Qube Settings** for **my-proxy** and in the **Services** tab, add an entry for `tinyproxy` (enter tinyproxy in the text field and click the plus button).

![Screenshot_2021-03-12_16-47-19|605x500](upload://laY34n6USSz1QWYP2V3qM9ckAwv.png) 

Create a qube based on template:fedora-32 or fedora-33, lets call it **my-qube**. Set its networking to **none**.

![Screenshot_2021-03-12_16-47-55|624x328](upload://68UAyK6bxXRdAkTWlC7EvFW3L7l.png) 

First we need to make sure changes to the tinyproxy configuration files are preserved between reboots of **my-proxy**.

Start a terminal in **my-proxy** and run the following command:

```
sudo mkdir -p /rw/config/qubes-bind-dirs.d
```

Create the file **/rw/config/qubes-bind-dirs.d/50_user.conf** with the following contents:

```
binds+=( '/etc/tinyproxy' )
``` 

Restart the **my-proxy** qube so the changes take effect.

Edit **/etc/tinyproxy/tinyproxy.conf** and uncomment the following lines:

```
Filter "/etc/tinyproxy/filter"
FilterDefaultDeny Yes
```

Create the file **/etc/tinyproxy/filter** and add all host names that should be allowed (note that these are regular expressions).

For example, to only allow access to all websites in the example.net domain (eg. example.net, www.example.net, etc), add the following lines:

```
^example\.net$
\.example\.net$
```

Edit the file **/rw/config/rc.local** and add the following line at the end of the file to start tinyproxy when the **my-proxy** qube is started:

```
systemctl start tinyproxy
```

In **dom0**, create the file **/etc/qubes-rpc/policy/qubes.ConnectTCP+8888** with the following contents (this will allow **my-qube** to connect to port 8888 of **my-proxy**):

```
my-qube @default allow,target=my-proxy
```

In **my-qube**, edit **/rw/config/rc.local** to add the following line which will create a link between port 8888 in **my-qube** and port 8888 in **my-proxy** (port 8888 being the default port used by tinyproxy):

```
qvm-connect-tcp ::8888
```

Start **my-qubes**'s Firefox and set HTTP Proxy to **localhost** port **8888** and select **Also use this proxy for FTP and HTTPS**.

You should now be unable to browse to any website which is not in list of allowed domains.

Bonus Feature - when you start **my-qube**, **my-proxy** will be automatically started by Qubes OS!

**Notes**

1. Many websites will try to load CSS, javscript libraries, images, etc from other domains. Blocking these could lead to websites not working correctly, so you may need to track down and add those other domains.
2. Attemping to access a blocked **https** site will result in "The proxy server is refusing connections" error - this is the expected hehaviour.`

**Troubleshooting**

1. In **my-proxy**, check that tinyproxy is running:
`sudo systemctl status tinyproxy`
If tinyproxy is not running, check that **/var/run/qubes-service/tinyproxy** exists. Also check the tinyproxy log file at **/var/log/tinyproxy/tinyproxy.log** for any error messages.
2. In **my-qube**, run the following:
`qvm-connect-tcp ::8888`
You should get an "Address is already in use" error.
3. In **my-qube**, check that the HTTP/HTTPS proxy has been set in Firefox.