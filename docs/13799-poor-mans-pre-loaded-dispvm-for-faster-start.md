I hope one day Qubes OS will have the ability to hold a preloaded DispVM ready to use it immediately when requested instead of having to start it. Until then I've implemented a little workaround / hack that gives me an approximation.

1. create named DispVMs

e.g. `qvm-create --class DispVM --template offline-dvm --label purple offline` and `qvm-create --class DispVM --template online-dvm --label red online`


2. make sure they start automatically either by using the autostart property or by creating shortcuts in dom0's ~/.config/autostart. I prefer the later as it takes effect *after* logging in. XFCE has a nice GUI under "Session and Startup | Application Autostart" in it's preferences to help you create them.

3. create a bash script `qvm-run-in-focused-vm` in dom0 with the following contents (e.g. in ~/bin):

```
#!/bin/bash

window_id=`xdotool getwindowfocus`
qube_name=`xprop _QUBES_VMNAME -id $window_id | cut -f2 -d\"`
command=$1

if [[ "$qube_name" == "_QUBES_VMNAME:  not found." ]]; then
         notify-send "qvm-run-in-focused-vm (dom0)" "$command"
         "$command" &

elif [[ ( "$qube_name" == "offline" || "$qube_name" == "online" ) && "$command" == "sudo poweroff" ]]; then

         notify-send "restarting $qube_name"
         qvm-shutdown --wait "$qube_name"
         qvm-start "$qube_name"

else
         notify-send "qvm-run-in-focused-vm ($qube_name)" "$command"
         qvm-run -a "$qube_name" "$command" &
fi
```

The above takes the first parameter given to the bash script and executes it in whatever qube had the focus (or dom0 if that had the focus). The 'elif' condition is what I specifically added for this workaround. It detects the names of my named DispVMs 'offline' or 'online' and if the command executed is `sudo poweroff`. If that's the case it won't execute the command but instead shutdown the respective qube (same effect) and wait. The when the qube is down, it will restart it.

4. Add a keyboard shortcut in XFCE's settings app under "Keyboard | Application Shortcuts". I choose Shift+Ctrl+W and mapped it to `qvm-run-in-focused-vm 'sudo poweroff'`. [^1]

5. Add or edit your `/etc/qubes/policy.d/30-user.policy` to include these lines:

```
qubes.OpenInVM          *           @anyvm          @dispvm     allow target=offline
qubes.OpenInVM          *           @anyvm          @anyvm      ask
qubes.OpenURL           *           @anyvm          @dispvm     ask default_target=online
qubes.OpenURL           *           @anyvm          @anyvm      ask
```

The effect is that any call of `qvm-open-in-dvm` with a file as parameter will open said file in the 'offline' qube, while any URL given will result in dom0 asking the user which qube to open it in with the default option being the 'online' qube.

6. train yourself to close windows by using Ctrl+Shift+W

Limitations:

* repeated `qvm-open-in-dvm` calls without Ctrl+Shift+W between them will open in the same instance of the named disposable. This can be a security issue as one infected file can then infect others opened in the same instance, but it can also be a feature depending on what you are doing

* if you just close the window using the normal ways (quit app, Ctrl+W or clicking on the respective window decoration) the workaround won't work and the named disposable won't restart (retain state)

Disclaimers:

* use at your own risk!
* know what you are doing!


[^1]: other unrelated nice shortcuts are: Shift+Ctrl+Return for `qvm-run-in-focused-vm nautilus` and Ctrl+Return for `qvm-run-in-focused-vm xterm`. I think you can see how this speeds things up a lot in daily use.