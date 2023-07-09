Just to be on the safe side, you may want to open all documents / files in a disposable qube. This prevents you from accidentally duoble-clicking a file and opening it on your work qube. This tutorial helps on that.

---

> :warning: **Reminder**: As always, this is the internet. Don't follow instructions from here unless you know what you are doing.

It's as easy as pasting two files in your App qube (AppVM). 

1. Create a file `.local/share/applications/open-in-dvm.desktop` with the following:

   ```
   [Desktop Entry]
   Type=Application
   Version=1.0
   Name=Open in Disposable VM
   Comment=Open file in a Disposable VM
   TryExec=/usr/bin/qvm-open-in-vm
   Exec=/usr/bin/qvm-open-in-vm --view-only '@dispvm' %f
   Terminal=false
   Categories=Qubes;Utility;
   ```

2. Create a file `.local/share/applications/mimeapps.list` with the following:

     File was too long to put here. Get it [here|attachment](https://raw.githubusercontent.com/freedomofpress/securedrop-debian-packaging/2dcb936f07773dfe643b1730d717a188728dd79c/securedrop-workstation-config/mimeapps.list.sd-app)

## Troubleshooting

If it is not opening anything, open the qube's settings, then open the "Advanced" tab and make sure you select something other than "None" in <kbd>Default DisposableVM Template</kbd>.

## Advanced stuff you can do

That's beyond the scope of this guide, but you can then:
* Making the disposable viewing qube be offline (not default)
* open all applications in the same qube (to avoid having a new disposable qube open every time you open a document).


## Further reading
  - https://github.com/Qubes-Community/Contents/blob/master/docs/common-tasks/opening-urls-in-vms.md

Credits:
  - [SecureDrop](https://github.com/freedomofpress/securedrop-debian-packaging/blob/2dcb936f07773dfe643b1730d717a188728dd79c/securedrop-workstation-config/mimeapps.list.sd-app)