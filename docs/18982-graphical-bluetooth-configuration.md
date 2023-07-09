Install the package `blueman` in the template of your `sys-usb` qube.

```
sudo dnf install -y blueman
```

Then restart the qube. From now on you should have a tray icon and be ready to connect to bluetooth devices graphically, like so:

![](https://forum.qubes-os.org/uploads/db3820/original/2X/e/e7eb9d14ec38c6a9e3784b319866ba2b105b1621.png)

In the picture above I had a sys-net combined to use USB devices too. The procedure stays the same.

Note: if you're using a separate sys-usb, and need to attach your bluetooth module to a AudioVM or MediaVM, 'blueman-manager' won't run without a recognized adapter from 'blueman-applet'. Once you attach, you can run 'blueman-manager' and with a script like the below in your AppVM's `rc.local` auto-connect to your preffered device:

```
address="XX:XX:XX:XX:XX:XX"

while (sleep 1)
do
connected=`sudo hidd --show` > /dev/null
if [[ ! $connected =~ .*${address}.* ]] ; then
sudo hidd --connect ${address} > /dev/null 2>&1
fi
done

```

The loop should be the last thing in rc.local or appended with `&`. This is a simple solution. (Something more robust would require extra work with `udev` perhaps.)

# AudioVM

For the most secure scenario, one should be running an AudioVM rather than rely on having PulseAudio in dom0. The creation of such a VM is beyond the scope of this guide.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/bluetooth.md)
- First commit: 20 Oct 2022. Last commit: 21 Oct 2022.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.1
- Original author(s) (GitHub usernames): aronowski
- Original author(s) (forum usernames): @aronowski
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>