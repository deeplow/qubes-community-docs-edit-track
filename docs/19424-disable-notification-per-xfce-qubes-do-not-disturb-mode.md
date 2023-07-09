Hi,

For fedora-xfce templates based AppVm, it's possible to desactivate the notification per Qube.

A first step is to run the program `xfce4-notifyd-config` in each AppVM, this is required to create the required entries in xfconf (gconf equivalent in XFCE, a settings database), and click on "Do not disturb" to enable, click again to disable.

You can stick with this procedure if it's good enough for you.

For advanced users who prefer using the command line, once the procedure above was done, you can use:

* display current setting: `xfconf-query -c xfce4-notifyd -p /do-not-disturb`
* enable do not disturb: `xfconf-query -c xfce4-notifyd -p /do-not-disturb --set true`
* disable do not disturb: `xfconf-query -c xfce4-notifyd -p /do-not-disturb --set false`
* toggle: `xfconf-query -c xfce4-notifyd -p /do-not-disturb -T`