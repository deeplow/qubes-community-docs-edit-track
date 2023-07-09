> Testing Qubes OS is not an easy task. It's not like you can run Qubes on the browser... or can you?!
>
> *That's what we're about to find out...*

![record8|690x460](upload://tuPNhdPsXeQX4lZNgsQYVMu6P5P.gif)


## What you'll need
- a random test laptop running Qubes 4.1
- internet connection

> #### :warning: A word of caution
> This setup involves completely invalidating the security properties of your Qubes installation. Do this only on a device used exclusively for testing.
>
> Additionally, participants will have access to the device as though they were next to you. If you connect the device to you home's WiFi, you should consider the risk of them being able to see its password or even find your home's physical address by your home network's name or the ones around.

## Overview

We have two devices: the participant's, which just needs to run Tor Browser and the UX Person's, which is running Qubes.

![qubes-remote-testing.drawio|690x225](upload://cyfFpgIZxW0bbEZj53AvNRIH4jV.png)


> :see_no_evil: **Limitations**
>
> * **2-20 seconds input delay** - can be improved if you use DNS instead of onion services. It really depends on your Tor circuit. I have been able to use with 2-4 seconds.

### 1. Create qube: remote-admin 

Create a new qube called `remote-admin` with the following settings:
|   |  |
|----|----|
| **Type** |  StandaloneVM |
| **Template** | debian-11 (:warning: debian 10 won't work) |

> :information_source: **Advanced**: for simplicity of software installation and persistence we create a standalone qube. Advanced users can probably figure out how to do the same with templates and app qubes.
###  2. Install remote screen sharing software in dom0:
> :information_source: instructions borrow from [here](https://github.com/QubesOS-contrib/qubes-remote-desktop) (in case they break check there).

Run the following in a dom0 terminal:
```bash
# install the qubes contributor's repository
sudo qubes-dom0-update qubes-repo-contrib

# install the remote-desktop software
sudo qubes-dom0-update qubes-remote-desktop

# set "VNCPASS" as the password
vncpasswd

#enable the qubes-x0vncserver (for some reason)
qvm-service --enable dom0 qubes-x0vncserver
```

:arrows_counterclockwise: and then start the dom0 VNC service
```
systemctl start qubes-x0vncserver@$(whoami)
```

### 2. Configure policy dom0 <-> remote-admin
In dom0's terminal type the following:
```bash
echo "qubes.ConnectTCP +5900 remote-admin @default allow target=dom0" | sudo tee /etc/qubes/policy.d/30-remote-admin.policy
```

### 3. (optional) Check that you have dom0 access from remote-admin

In `remote-admin`:

1. :arrows_counterclockwise: open a terminal and run `qvm-connect-tcp 5900:@default:5900` 

> :information_source: **Good point to test**
> At this stage you can check if you are correctly getting. You can install a VNC viewer like `remmina` and connect to `127.0.0.1:5900`. Then it will ask the password `VNCPASS` (you set it earlier).
>
> ![vnc_remmina2|551x500, 75%](upload://sNwYnO6LBIOvNdxZHpenDrJEiTy.png)
>
> ***
> :hammer_and_wrench: **Troubleshooting**
> * **vnc connection failure: too many security failures**
>  Just restart the vnc server in dom0 `systemctl restart qubes-x0vncserver@$(whoami)`
> 
> *** 

### 4. Install the guacamole server (vnc to web)
> :information_source: Guacamole essentially allows users to connect via their web browser to a VNC server. 

Still in the `remote-admin` qube

1. You install it like this:
```
sudo apt install -y guacd libguac-client-vnc0
sudo apt install -y tomcat9 tomcat9-admin tomcat9-common tomcat9-user
```
2. Download the latest guacamole `.war` from https://guacamole.apache.org/releases/

4. Verify the file integrity with the `sha256` hashes on the website
 *(can save you some troubleshooting time in case your download breaks)*

5. Copy the downloaded file onto `/var/lib/tomcat9/webapps/guacamole.war` (may need sudo)

6. restart tomcat for the newly installed `.war`
   `sudo systemctl restart tomcat9` 

7. Edit the file `/etc/guacamole/user-mapping.xml` (you may need to create `/etc/guacamole/`)
```xml
<user-mapping>
    <authorize username="user" password="pass">
        <protocol>vnc</protocol>
        <param name="hostname">127.0.0.1</param>
        <param name="port">5900</param>
        <param name="password">123456</param>
    </authorize>
</user-mapping>
```

8. Restart guacamole to apply the changes: `sudo systemctl restart guacd`.

9. Open firefox on the webpage: `http://127.0.0.1:8080/guacamole`. 
   > You should see a login page. Your credentials are:
   > **user**: user
   > **pass**: pass
   > 
   > ![vnc_guac|690x433, 50%](upload://jNwpnCd8VoUCAZEjaGEVOBz2l9q.png)

> :partying_face: **Hurray!**
> Now you have a functioning dom0 remote access via the web browser.
>
> *But this is not super useful since it is just local access and you can't give that address for a user to test. In the next section, we'll show you how you can generate an address where your users can test your system.*

## 4. Create a `.onion` address for it

1. `sudo apt install tor`
2. edit the file `/etc/tor/torrc` and add the following text at the end and save it:
```rc
HiddenServiceDir /var/lib/tor/guacamole_vnc
HiddenServicePort 80 127.0.0.1:8080
HiddenServiceVersion 3
```
3. restart Tor to apply the changes
   `sudo systemctl restart tor`
4. Obtain your `.onion` address
    `sudo cat /var/lib/tor/guacamole_vnc/hostname`

    >  :information_source: Save this link as that will be what you share with your participants.
    > Just be aware that they have to install the [Tor Browser](http://torproject.org/download) in order to access it.

4. Grab some tea :tea: while the onion address propagates through the Tor network. (max 10 mins)


## 5. Share the link with your participants

1. Send `yoursite.onion/guacamole` with participants
2. Tell them to log in with:
  **user**: user
  **pass**: pass

----

## When you restart your computer
Everything with  :arrows_counterclockwise:  you have to run every time you restart your computer / remote-admin qube.


## Tips & Tricks

### :ghost: Hiding `remote-admin` qube
Because an extra qube is running it could interfere with a user's experience (e.g. they will see it in the qube domains widget). To hide it, you can delete `sys-whonix` or `sys-usb` and rename `remote-admin` to either one. An unsuspecting users won't see any difference.

### Making this faster

See this [related discussions](https://forum.qubes-os.org/t/the-qubes-os-project-is-now-accepting-donations-on-ethereum/13941).


## Credits

* @fepitre for putting together [qubes-remote-desktop](https://github.com/QubesOS-contrib/qubes-remote-desktop) and pointing me to it

* Inspiration from this [guide](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/screen-share.md) and [this discussion](https://github.com/QubesOS/qubes-issues/issues/6426).

* byzanz developers, which made a tool that can be installed in dom0 through the repos and allows for creating gifs from dom0.