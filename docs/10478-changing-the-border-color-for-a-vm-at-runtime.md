If you want to play with GUI in Qubes OS, you can try this:

(Take your risk)

(works in R4.1)

In dom0 terminal, `ps -ef|grep guid`

The listed processes are the dom0 side graphical programs for each VM.

Remember the command line, and pick one of the processes to kill.

After you have killed the guid, all the windows of mentioned VM will be hidden. You will see them later.

Say you killed:

```
/usr/bin/qubes-guid -N sys-net -c 0xcc0000 -i /usr/share/icons/hicolor/128x128/devices/appvm-red.png -l 1 -q -C /var/run/qubes/guid-conf.17 -d 17 -n
```

`-c 0xcc0000` is the color of the VM window border in hex.

Rerun the command line, with only the color value different, and then you can find out the hidden windows reappears with different borders.

You can put a color that is not configured in Qubes OS at all, for example light pink.

Only for everyday laugh. Wish you a happy day.

(Actually the original story is not so happy - just now I found out that all the `guid` have exited, so I have to restart them up manually one by one)