BACKGROUND: Qubes OS R4.1 by default uses LVM volume with snapshot for AppVM private storage, and by default the filesystem is ext4. A large amount of disk writes (for example extracting a linux kernel source code tarball) can be extremely slow.

I have found a simple solution of this problem, and I would like to share it here for anyone in need, and also in the hope of letting more Qubes OS experts help me find out whether this practice has security problem or is not optimal, or I was misunderstanding some Qubes OS mechanisms.

METHOD:

1. Create the LVM volume to remove the snapshot layer. In dom0 the `lvcreate` following command can create a volume that is visible in `qvm-block` and `qvm-device block ls`
```
# vm-pool -> thin pool name (existing)
# custom_testvol1 -> volume name (new)
lvcreate -V 100G --thinpool vm-pool qubes_dom0 -n custom_testvol1
lvremove /dev/qubes_dom0/custom_testvol1
```
Better set a common prefix for names of all custom volumes.

2. (Thanks to @rustybird) Edit dom0 config so that dom0 udev does not parse the block device. Qube can be untrusted, and they are free to edit the volume, which is why we should make sure that dom0 does not parse the volume filesystem by default.
(Apply for Qubes R4.1) Create a file named `/usr/lib/udev/rules.d/20-skip-custom-lvm-devices.rules` in dom0, and insert the following content:
```
ACTION!="remove", SUBSYSTEM=="block", ENV{DM_UUID}=="LVM-*", ENV{DM_LV_NAME}=="custom_*" ENV{DM_UDEV_DISABLE_DISK_RULES_FLAG}="1", ENV{UDEV_DISABLE_PERSISTENT_STORAGE_RULES_FLAG}="1" ENV{QUBES_EXPORT_BLOCK_DEVICE}="1"
```

Note that `custom_*` is the prefix mentioned before, and edit it to fit your use case.

3. attach the block device onto the builder appvm. I usually uses the GUI approach though `qvm-block attach` is possible; when ro is required, `qvm-block attach --ro` seems to be the only solution.

4. format the volume. In your appvm format the block device with the filesystem you like: if you only use it to store large files, ext4 is enough; if you need to store a swarm of small files, btrfs or zfs will be your choice. (btrfs is one of preinstalled kernel modules so can be used across various linux appvms - one only need a `mkfs.btrfs` initially; zfs must be installed manually in template vm and is harder to install)

5. mount it and try it out to see the performance improvement.

DISCUSSION: This setup is advantageous mainly because
(1) no snapshot, no playing with lvm volume creation and deletion. This can improve block device writing speed and accelerate builder VM shutting down (When a VM writing too much memory, the VM will be slow to shutdown)
(2) using custom filesystem like btrfs rather than default ext4 can minimize required disk writes since such filesystem has many advanced features including optimizations for storing smaller files, compression and deduplication.

As a result this is an optimal setup for VM that does extensive building - such behavior can create many small files.

This setup is compatible with [zfs on docker](https://docs.docker.com/storage/storagedriver/zfs-driver/). I tried this and find out that such setup accelerate dockerfile building by a large amount and does not increase shutdown time for builder VM.

With this setup, one volume could also be mounted onto various appvms. Though this could possibly break the VM isolation (one compromise appvm can contaminate the block device), this may be desired in some situations especially when the block device is attached readonly, for example when one want to broadcast certain large files to a range of appVMs, or let VM use the files temporarily without putting the files into VM private storage, etc.