People familiar with xfce from other distributions might know the handy wavelan plugin for the panel. Unfortunately due to dom0's nature of being networkless, for obvious security reasons, i quickly hacked a script together to have at least some kind of current network usage.
I'm sure it can be further optimized or customized to be more fancier, but that's something for you to implement :slight_smile:

Note:
This script runs in dom0. You should be aware of the impact. This CAN and WILL be a security issue.
This script is NOT free of bugs.



```

#!/bin/bash

INTERFACE='wls6f0u3'
VMNAME='sys-net'
INTERVAL=1 # seconds
COMMAND="cat /sys/class/net/$INTERFACE/statistics/rx_bytes;cat /sys/class/net/$INTERFACE/statistics/tx_bytes;sleep $INTERVAL;cat /sys/class/net/$INTERFACE/statistics/rx_bytes;cat /sys/class/net/$INTERFACE/statistics/tx_bytes"
SHMFILE='/dev/shm/netspeed'

# read values
if [ -z "$1" ]; then
	if [ -e "$SHMFILE" ];then
		cat "$SHMFILE"
	else
		(setsid "$0" daemon &) &
	fi
	exit 0
fi

# daemon: calculate values in infinite loop
cd /
umask 177 # u+rw,g-rwx,o-rwx

# check for file in atomic operation
(set -o noclobber;>"$SHMFILE") &> /dev/null
if [ "$?" == 1 ]; then
	# file exists, possible race condition, another daemon already running
	exit 1
fi

for fd in $(ls /proc/$$/fd); do
	eval "exec $fd>&-"
done
exec 0< /dev/null #  stdin
exec > /dev/null # stdout
exec 2> /dev/null # stderr

while true; do 
	r=`qvm-run --no-autostart --pass-io --no-gui --no-colour-output --no-colour-stderr "$VMNAME" "$COMMAND"`
	if [ "$?" == 0 ];then
		a=($r)
		r1=${a[0]}
		t1=${a[1]}
		r2=${a[2]}
		t2=${a[3]}
		rkbps=`awk "BEGIN {printf \"%d\", ($r2 - $r1) / 1024 * (1 / $INTERVAL)}"`
        tkbps=`awk "BEGIN {printf \"%d\", ($t2 - $t1) / 1024 * (1 / $INTERVAL)}"`

		echo -n "<txt><span weight='bold' fgcolor='#FFF900' bgcolor='red'> $rkbps kb/s / $tkbps kb/s </span></txt>" > "$SHMFILE"
	else
		echo -n "<txt><span weight='bold' fgcolor='#FFF900' bgcolor='red'> qvm-run failed </span></txt>" > "$SHMFILE"
	fi
done
```




Add a generic monitor to your xfce panel and it will look a bit like this:
![asd|690x29](upload://p2cJgcLQQKTCqUWevhzP788865n.png)

In case you need to restart the daemon for changes to take effect, kill it's pid and rm /dev/shm/netspeed afterwards.