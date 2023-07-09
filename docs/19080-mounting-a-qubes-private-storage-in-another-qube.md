Useful for data recovery. As per [this Reddit post](https://www.reddit.com/r/Qubes/comments/chgb3h/is_it_possible_to_access_files_inside_a_vm/f8ur03m/):

```
[dom0] sudo lvcreate --size 1G --snapshot --name tempsnap /dev/mapper/qubes_dom0-vm--untrusted--private


[dom0] readlink /dev/mapper/qubes_dom0-tempsnap


[dom0] qvm-start --hddisk dom0:/dev/[from previous command] viewervm

(Attaching to a running viewervm was not possible)


[viewervm] mkdir -v /tmp/stuff


[viewervm] sudo mount /dev/xvdi /tmp/stuff
```

If the original VM has more than one partition, have to pick the right one, such as xvdi1 or xvdi2, etcetera.

Could be unmounted, but no commands or options we tried allowed to detach the viewervm until it was stopped. (qvm-block still seems bugged)

Couldn't lvremove until the machine was restarted.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/system/vm-image.md)
- First commit: 05 Jan 2020. Last commit: 05 Jan 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): null
- Original author(s) (forum usernames): N/A
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>