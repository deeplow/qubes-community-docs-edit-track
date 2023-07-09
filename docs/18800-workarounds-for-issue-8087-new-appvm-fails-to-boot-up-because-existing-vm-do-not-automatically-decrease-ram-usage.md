I have long suffered from the issue below, and it does not seems to be discussed ever since though it still exists on the latest system. Now I find out a quick workaround (in dom0):

https://github.com/QubesOS/qubes-issues/issues/8087

Workaround is to do it manually. (in dom0, sudo)

```
virsh setmem --domain large_ram_appvm --size 8000M --current
```

This command exactly shrinks the ram of vm named "large_ram_appvm" into 8000M and recovers later. This command provides a time window to boot another VM.

Wish this will be helpful for someone.