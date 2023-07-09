I observe myself doing this often lately:
1. Click on the Qubes icon in the tray
2. Search for the one disp in a list of multiple dozens
3. Change some settings, usually increasing storage

Im sick of it, so i automated the most tedious part of this process: Opening the correct settings window.

Now i focus a window of the qube i want to change the settings and hit mod1+shift+s and the settings gui opens.

For this i wrote a little script that i place in ` ~/scripts/settings` in *dom0*.
```
#!/bin/bash
# Settings shortcut
#
# Does open the gui settings for the qube running the window in focus

# Get active window
ID=`xdotool getwindowfocus`
TARGET=`xprop _QUBES_VMNAME -id $ID|cut -f2 -d\"`
if [[ "$TARGET" == "_QUBES_VMNAME: not found." ]]; then
  notify-send "Could not get active qube :("
  exit 1
fi

# Open settings
qubes-vm-settings "$TARGET"
```

This simply gets the active window, reads its origin qube name and issues `qubes-vm-settings` on it. Nothing fancy.

Please note, that this script must be executable of course. One can ensure this by calling `chmod +x ~/scripts/settings` (or where you would place such a script).

## xfce
For normal xfce users, you can click on the menu -> Keyboard and add a new shortcut. The command you should use is `sh ~/scripts/settings` (or whatever path you choose for this script).

## Awesome
I use awesome, so i added this snippet to my `~/.config/awesome/rc.lua` where the keyboard shortcuts are:
```
awful.key({ modkey, "Shift" }, "s", function() awful.util.spawn("sh ~/scripts/settings"), end
              {description = "Opens settings for qube in focus", group = "custom"})
```

## KDE and others

The shortcut creation in kde is pretty much the same as with xfce. I am not familiar with i3, so dunno how it would be done there.

In principle this script should be compatible with any window manager.


It ain't much, but it's honest work. Maybe somebody can use this too or get inspired to do other, more awesome stuff!