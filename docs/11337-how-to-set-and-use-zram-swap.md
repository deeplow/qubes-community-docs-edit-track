https://forum.qubes-os.org/t/how-to-turn-off-swap-the-cost-of-doing-so/8474/17?u=enmus

Continuing from the topic and making guide for those interested in, as well as a reminder for myself after clean install someday.
# Goals / Possible Benefits
- To minimize dedicated amounts of RAM
- To maximize utilizing total amount of RAM
- To extend lifespan of a SSD
- Hopefully to reduce Qubes footprint
- To increase overall performance
- To prevent performance hits to a level at least as without zram.

# Why?
By default swappiness is set to 60. This means that when 40% of RAM is used, swapping is started. According to experience, even decreasing swappiness to 0 didn't prevent swapping to start much earlier than RAM is exhausted. So, obviously, different approach is needed (beside disabling swap at all)
# Prerequsite
It is advisable to disable `zswap` prior to activate `zram` module, in order to prevent zswap intercepting memory pages being swapped out before they reach zram. The difference compared to zram is that zswap works in conjunction with a swap device while zram is a swap device in RAM that does not require a backing swap device, but in my guide I will as well set a swap as a backup device to avoid system crash once the (z)RAM is exhausted.

# How To
I have added kernel parameter to disable zswap just in case
>GRUB_CMDLINE_LINUX="... quiet zswap.enabled=0"

For other qubes, it can be done by adding `kerenlopts`
>qvm-prefs -s *VMname* kernelopts "zswap.enabled=0"

Or, we can do it the other way
>$ sudo bash -c "echo 0 > /sys/module/zswap/parameters/enabled"

Now, we will disable all active swaps
>$ sudo swapoff --all

If you want to completely disable swap devices in fstab, edit it 
> $ sudo nano /etc/fstab

and comment out swap entries.

 **I) Starting zram for the first time**

**The **zram** module is controlled by **systemd**, so there's no need for a fstab entry**, so let's load the module
> $ sudo modprobe zram num_devices=1

Please note that it is advisable to set one module per CPU. If you have more than 1 CPU, set `num_devices` above accordingly.

Check supported compression algorithms
>$ cat /sys/block/zram0/comp_algorithm

the one in `[]` is currently set. Let's set `lz4hc`
>$ sudo bash -c "echo lz4hc > /sys/block/zram0/comp_algorithm"

Now we have to set disk size. I have decreased dom0's `maxmem` size to 1536MB so for sure all of that will be used, and the rest it'll be taken - from RAM! So I blindly set 8GB and watching its use.
> $ sudo bash -c "echo 8G > /sys/block/zram0/disksize"

Now to activate `zram0`
>$ sudo mkswap --label zram0 /dev/zram0

Since I will use swap as a backup device, I will set it with the highest possible priority to ensure it will be used first
> $ sudo swapon --priority 32767 /dev/zram0

Now to check what we've done so far
> zramctl


```
NAME       ALGORITHM DISKSIZE DATA COMPR TOTAL STREAMS MOUNTPOINT
/dev/zram0 lz4hc            8G   4K   64B    4K       4 [SWAP]
```
Everything seems to be OK.

**II) Let's stop zram swap**
>$ sudo swapoff /dev/zram0

Let's free already allocated memory to device, reset disksize to 0, and unload the module
> $ sudo bash -c "echo 1 > /sys/block/zram0/reset"
$ sudo modprobe -r zram

**III) Starting zram at boot**
In order zram to start on boot we will need to create 2 scripts (`zram_start` and `zram_stop` - *copy these files to /usr/local/bin*) and a service - zram_swap.service.

**zram_start** script
```
#!/usr/bin/env bash
# Create a swap device in RAM with the 'zram' kernel module. Copy this file to /usr/local/bin.

# Show supported compression algorithms...
#  cat /sys/block/zram0/comp_algorithm
compress="lz4hc"

disksize="8G" #Set this accordingly to available RAM
priority="32767"  # give zram device highest priority

# Disable zswap  in order to prevent zswap intercepting memory pages being swapped out before they reach zram
echo 0 > /sys/module/zswap/parameters/enabled
# Disable any active swaps (I don't want to disable swap to prevent crashes that - uncomment if want to completely disable swap)
# swapoff --all
# Load module
modprobe zram num_devices=1
# Set compression algorithm
echo $compress > /sys/block/zram0/comp_algorithm
# Set disk size
echo $disksize > /sys/block/zram0/disksize
# Activate
mkswap --label zram0 /dev/zram0
swapon --priority $priority /dev/zram0

# View info with zramctl
```
**zram_stop** script
```
#!/usr/bin/env bash
# Deactivate zram0 swap device in RAM. Copy this file to /usr/local/bin.

swapoff /dev/zram0

# Free already allocated memory to device, reset disksize to 0, and unload the module
echo 1 > /sys/block/zram0/reset

sleep 1
modprobe -r zram
```
Create service file as `/etc/systemd/system/zram_swap.service`
```
[Unit]
Description=Configure zram swap device
After=local-fs.target

[Service]
Type=oneshot
ExecStart=/bin/bash /usr/local/bin/zram_start
ExecStop=/bin/bash /usr/local/bin/zram_stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
Enable service
> $ sudo systemctl enable zram-swap.service

**IV) (Additional) Kernel parameters**

We can fine tune the kernel to get the most of the zram.
I have chosen these parameters:
>    `vm.vfs_cache_pressure` - increase frequency of clearing caches to free RAM
    `vm.swappiness` - increase percentage to start using zram earlier
    `vm.dirty_background_ratio` and `vm.dirty_ratio` - amount of memory pages permitted to be "dirty" before writing to zram
`vm.oom_kill_allocating_task` - if set to non-zero, OOM killer  kills the task that triggered the out-of-memory condition. This avoids the expensive tasklist scan which is unlikely to ever be finished in such a situation. Set as a precaution.

Check default values
>$ cat /proc/sys/vm/vfs_cache_pressure
100
$ cat /proc/sys/vm/swappiness
60
$ cat /proc/sys/vm/dirty_background_ratio
10
$ sudo cat /proc/sys/vm/dirty_ratio
20

Set new parameters `/etc/sysctl.d/99-sysctl.conf` or if you prefer ( it is not advisable) directly to `/etc/sysctl.conf` 
>vm.vfs_cache_pressure=500
vm.swappiness=100
vm.dirty_background_ratio=1
vm.dirty_ratio=50
vm.oom_kill_allocating_task=1

You may now reload the deamon
>sudo systemctl daemon-reload

and check the parameters:
>$ sudo sysctl -p
vm.vfs_cache_pressure = 500
vm.swappiness = 100
vm.dirty_background_ratio = 1
vm.dirty_ratio = 50
vm.oom_kill_allocating_task = 1

**V) Reboot and enjoy**
Checking
>$ cat /proc/swaps (or `swapon --show)

```
Filename				Type		Size		Used	Priority
/dev/dm-x                               partition	4136956		0	0
/dev/zram0                              partition	6291452		463616	32767
```
Obviously, SSD swap partition is not used.

# Findings
- It looks that swapping starts almost at the same time after ballooning starts too. Given the fact (?), that is one reason more to try zram to avoid swappines and performances hits.
- Since RAM can hold much more information, for obvious reasons CPU will be used more, so this is something you might want to consider when deciding. I have too old CPU and using zram anyway (see below).
- Still, it is much quicker than swapping to a SSD. Since I set `dom0's maxmem` to 1536MB (thus leaving more for qubes), system often falls back to swap, and this improves responsiveness while achieving goals from the beginning.
- I'm using zram0 for more than 2 weeks and *I haven't faced any performance hits*, or at least not other than without zram0, again goals achieved.
- ZRAM has to be set for each template if you'd like to use it everywhere.

#To Do
Creating salt formula to implement zram as `highstate` to avoid manual qube-by-qube setting. Contribution with this highly appreciated.

Please let me know if I made some mistakes here, or if the guide can be improved, I'd be happy to edit it.

# Helpful links
 * https://wiki.archlinux.org/title/Improving_performance#zram_or_zswap
* [Toggling zswap](https://wiki.archlinux.org/title/Zswap#Toggling_zswap) 
 * https://www.kernel.org/doc/html/latest/admin-guide/blockdev/zram.html
 * https://linuxreviews.org/Zram
* https://wiki.archlinux.org/title/Zswap