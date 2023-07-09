Here denotes my attempts to speedup booting as R4.1 on newer hardware is not stable enough and reboot may be required to reset the hardware into known good states.

1. After inputed the correct hard disk encryption password on boot, press F1 to see the actual booting log in real time. Here one can see which step is taking the most of the time along with how much time has been spent on booting.

2. `systemd-analyze` is useful to spot the slowest process and to spot the paths of services, however please take your risk when you want to modify the services by hand. `systemd-analyze blame` can tell directly the slowest step; `systemd-analyze unit-files` can lead you to the config files of corresponding services. If you want to add tracer to them, you may choose to edit the config files. For example `perf`, `strace`, etc.

3. Avoid booting up `sys-net`, `sys-usb`, `sys-firewall` VMs on boot, if you are facing boot time problems - booting such VMs can have unpredictable results, as their booting may fail or take too much time.

4. `sudo systemctl enable debug-shell.service` provide you a [root shell](https://freedesktop.org/wiki/Software/systemd/Debugging/) at /dev/tty9 early at boot. Notice that this will introduce a security hole so disable it after you have done your debugging.

5. If you found that `lvm2` related process takes the majority of your booting time and with step 4 you find out that `thin_check` is the culprit, then [this](https://bugzilla.redhat.com/show_bug.cgi?id=1490517) can be referred. Since I have installed qubes os on a 2T hdd, the booting time for `thin_check` takes as long as 10-20 minutes. (I am still testing this setup out)