# Custom Installation /boot in USB with FDE 

After booting your installation media until 'choose your language', switch to shell with ```ctrl + alt + f2```

Look your block device to make sure your device.
```
[anaconda root@localhost /]# lsblk
```

## Reformat USB Devices.
```
##EFI PARTITION /dev/sdb1
[anaconda root@localhost /]# gdisk /dev/sdb
n
1
2048
1230845
EF00

##BOOT PARTITION /dev/sdb2
n
2
1230848
3278842
8300

##Write changes to disk
```

![QubesOS-2021-07-03-03-32-04 - Copy|666x500](upload://8Fzk9X0yXJ6WludI6UTJsX77SfM.png)

![QubesOS-2021-07-03-03-33-57|666x500](upload://apR3saZgPcTfeMiqp7D8ijoDNJt.png)


## Preparing LUKS on /dev/sda
In this step we will using twofish-xts-plain64 chiper with sha512 hash and 512B keysize.

```
[anaconda root@localhost /]# cryptsetup -c twofish-xts-plain64 -h sha512 -s 512 --use-random -y -i 10000 luksFormat /dev/sda
```

![QubesOS-2021-07-03-03-39-56|666x500](upload://i7MhPtOu9Qs6MTWW4i5z5ogfsA7.png)

Override data and enter your disk passphrase, then open your encrypted disk.

```
[anaconda root@localhost /]# crypsetup luksOpen /dev/sda luks
```

## Create LVM
```
[anaconda root@localhost /]# pvcreate /dev/mapper/luks

[anaconda root@localhost /]# vgcreate qubes_dom0 /dev/mapper/luks

[anaconda root@localhost /]# lvcreate -n swap -L 8G qubes_dom0 ## You can change size value according to your need, I use 8G

[anaconda root@localhost /]# lvcreate -T -L 20G qubes_dom0/root-pool ## 20G is enough for dom0 and I use LVM Thin Provisioning

[anaconda root@localhost /]# lvcreate -T -l +100%FREE qubes_dom0/vm-pool ## +100%FREE means I use the rest of disk spaces to vm pool 

[anaconda root@localhost /]# lvs ## Verified if pool is created or not

[anaconda root@localhost /]# lvcreate -V20G -T qubes_dom0/root-pool -n root

[anaconda root@localhost /]# lvcreate -V51.84G -T qubes_dom0/vm-pool -n vm

[anaconda root@localhost /]# mkfs.ext4 /dev/qubes_dom0/vm ## Create a file system on vm LVM because *remember* we can't reformat this volume at installer gui
```

![QubesOS-2021-07-03-03-56-21|666x500](upload://8AeVyTxSPBbv5eIoiEmKLviD1TJ.png)

![QubesOS-2021-07-03-03-59-53|666x500](upload://rmnzlhtfymMERBZyzELM6aUJbvX.png)

Back to installation gui with ```ctrl + alt + f6``` and choose your language installation then follow the guide inside.

## Setup Disk

Go to installation destination, click *refresh on bottom right*, after wait for sometime, click on your 2 disk and click done in top left.

![QubesOS-2021-07-03-04-01-05|666x500](upload://lH5Uwmr82TtjXmLqIaz5H7GUssG.png)

There are some partition we created before, but in here you need to reformat the partition and select mount point.

![QubesOS-2021-07-03-04-03-39|666x500](upload://fLkvCc9rkWEfjYG5mxMWrnA5Wut.png)

qubes_dom0-root click reformat, ext4 FS, / mount point, then update settings.
qubes_dom0-swap reformat, swap mount point, update.
sdb1 reformat efi, /boot/efi mount point, update.
sdb2 reformat ext4, /boot mount point, update.
don't configure anything on qubes_dom0-vm.
click done on top left. 

![QubesOS-2021-07-03-04-07-35|666x500](upload://9k2H5z3mq3TeRa0hvCCNQnGYf8J.png)

and there will be summary of your changes just click accept changes. 

![QubesOS-2021-07-03-04-08-37|666x500](upload://2MoQlwuRtqrA3kQil4HuO98WYFt.png)

## Installation

Click begin and grab coffe, my installation would take long because i use hdd in this step and with vmware. Patient is a key :D 

And when the loading screen isn't animate it's okay just wait.

![QubesOS-2021-07-03-04-13-25|666x500](upload://hLX0uzEBWnbRRhIozjtHrZQKSZ6.png)

Reboot when it's finished and enter your disk passphrase and configure how you want to use qubes.

Just use default if you haven't experienced with creating qube system.

## YOU'VE BEEN WARNED

DON'T CREATE SYS-USB! YOUR USB DRIVE WILL GET REMOVED AND YOUR SYSTEM WILL CRASH BECAUSE YOU NEED TO FIGURE IT OUT HOW TO TWEAKS.

The reason I choose installing all template and just create critical system is to make sure if anything is okay and i'm planning to make an Minimal Template setup guide later.

Click done and make another cup of coffe :D 

![QubesOS-2021-07-03-04-40-56|666x500](upload://ftEDzfARLBblAWa8h1Prj7pfCbd.png)

After long time wait here there come our lovely os :3

![QubesOS-2021-07-03-05-28-59|666x500](upload://5qEgbEv4tWFXPKv5a4xUl5VZAHv.png)

I normally use current-security repo, because it's latest and stable for my device, well i can say that if you have modern device, you really need 4.1 with latest kernel if possible.

![QubesOS-2021-07-03-05-38-58|666x500](upload://r34pxZvwUedsJgYrfIHNIIu59KE.png)

And here's some log about the system.

```
LUKS header information
Version:       	2
Epoch:         	3
Metadata area: 	16384 [bytes]
Keyslots area: 	16744448 [bytes]
UUID:          	77807f8c-6be8-435e-be23-b645c272745e
Label:         	(no label)
Subsystem:     	(no subsystem)
Flags:       	(no flags)

Data segments:
  0: crypt
	offset: 16777216 [bytes]
	length: (whole device)
	cipher: twofish-xts-plain64
	sector: 512 [bytes]

Keyslots:
  0: luks2
	Key:        512 bits
	Priority:   normal
	Cipher:     twofish-xts-plain64
	Cipher key: 512 bits
	PBKDF:      argon2i
	Time cost:  5
	Memory:     1048576
	Threads:    2
	Salt:       b5 3f 58 4a 20 17 df c9 f2 89 1d 50 7a ef 17 58 
	            82 8e de 01 e7 bc 6e 93 3b ac da 2d 61 56 12 39 
	AF stripes: 4000
	AF hash:    sha512
	Area offset:32768 [bytes]
	Area length:258048 [bytes]
	Digest ID:  0
Tokens:
Digests:
  0: pbkdf2
	Hash:       sha512
	Iterations: 146122
	Salt:       5c 74 f5 3d 0e 51 89 36 f3 82 c6 95 27 db 70 58 
	            bf e3 f9 5d a9 7f 3d 6e b1 08 fb 35 67 bf 08 af 
	Digest:     92 2c f2 6b 57 ef 62 a9 33 49 cc a4 9b d9 dc 26 
	            89 59 e6 c3 e0 13 d3 bd 42 51 ef 28 30 1f 4d 80 
	            2e 09 0d 4d 16 5a 6b 14 08 1f 2a 5c 39 a7 5c b9 
	            04 af 32 f9 48 06 7b d3 80 f6 26 a4 54 86 4e 29 
```
```
NAME                                                            MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                                                               8:0    0   80G  0 disk  
└─luks-77807f8c-6be8-435e-be23-b645c272745e                     253:0    0   80G  0 crypt 
  ├─qubes_dom0-root--pool_tmeta                                 253:1    0   20M  0 lvm   
  │ └─qubes_dom0-root--pool-tpool                               253:3    0   20G  0 lvm   
  │   ├─qubes_dom0-root                                         253:4    0   20G  0 lvm   /
  │   └─qubes_dom0-root--pool                                   253:6    0   20G  1 lvm   
  ├─qubes_dom0-root--pool_tdata                                 253:2    0   20G  0 lvm   
  │ └─qubes_dom0-root--pool-tpool                               253:3    0   20G  0 lvm   
  │   ├─qubes_dom0-root                                         253:4    0   20G  0 lvm   /
  │   └─qubes_dom0-root--pool                                   253:6    0   20G  1 lvm   
  ├─qubes_dom0-swap                                             253:5    0    8G  0 lvm   [SWAP]
  ├─qubes_dom0-vm--pool_tmeta                                   253:7    0   52M  0 lvm   
  │ └─qubes_dom0-vm--pool-tpool                                 253:9    0 51.9G  0 lvm   
  │   ├─qubes_dom0-vm--pool                                     253:10   0 51.9G  1 lvm   
  │   ├─qubes_dom0-vm                                           253:11   0 51.9G  0 lvm   
  │   ├─qubes_dom0-vm--sys--net--private--1625290080--back      253:12   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--fedora--33--root--1625288095--back       253:13   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--fedora--33--root--1625288169--back       253:14   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--fedora--33--root                         253:15   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--debian--10--root--1625288707--back       253:16   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--fedora--33--private                      253:17   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--debian--10--root--1625288783--back       253:18   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--gw--15--root--1625289127--back   253:19   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--debian--10--private                      253:20   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--debian--10--root                         253:21   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--gw--15--root--1625289200--back   253:22   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--ws--15--root--1625289651--back   253:23   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--gw--15--root                     253:24   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--gw--15--private                  253:25   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--ws--15--root--1625289726--back   253:26   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--fedora--33--dvm--private                 253:27   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--ws--15--private                  253:28   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--whonix--ws--15--root                     253:29   0   10G  0 lvm   
  │   ├─qubes_dom0-vm--sys--firewall--private--1625289951--back 253:30   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--default--mgmt--dvm--private              253:31   0    2G  0 lvm   
  │   ├─qubes_dom0-vm--sys--net--private                        253:33   0    2G  0 lvm   
  │   └─qubes_dom0-vm--sys--firewall--private                   253:35   0    2G  0 lvm   
  └─qubes_dom0-vm--pool_tdata                                   253:8    0 51.9G  0 lvm   
    └─qubes_dom0-vm--pool-tpool                                 253:9    0 51.9G  0 lvm   
      ├─qubes_dom0-vm--pool                                     253:10   0 51.9G  1 lvm   
      ├─qubes_dom0-vm                                           253:11   0 51.9G  0 lvm   
      ├─qubes_dom0-vm--sys--net--private--1625290080--back      253:12   0    2G  0 lvm   
      ├─qubes_dom0-vm--fedora--33--root--1625288095--back       253:13   0   10G  0 lvm   
      ├─qubes_dom0-vm--fedora--33--root--1625288169--back       253:14   0   10G  0 lvm   
      ├─qubes_dom0-vm--fedora--33--root                         253:15   0   10G  0 lvm   
      ├─qubes_dom0-vm--debian--10--root--1625288707--back       253:16   0   10G  0 lvm   
      ├─qubes_dom0-vm--fedora--33--private                      253:17   0    2G  0 lvm   
      ├─qubes_dom0-vm--debian--10--root--1625288783--back       253:18   0   10G  0 lvm   
      ├─qubes_dom0-vm--whonix--gw--15--root--1625289127--back   253:19   0   10G  0 lvm   
      ├─qubes_dom0-vm--debian--10--private                      253:20   0    2G  0 lvm   
      ├─qubes_dom0-vm--debian--10--root                         253:21   0   10G  0 lvm   
      ├─qubes_dom0-vm--whonix--gw--15--root--1625289200--back   253:22   0   10G  0 lvm   
      ├─qubes_dom0-vm--whonix--ws--15--root--1625289651--back   253:23   0   10G  0 lvm   
      ├─qubes_dom0-vm--whonix--gw--15--root                     253:24   0   10G  0 lvm   
      ├─qubes_dom0-vm--whonix--gw--15--private                  253:25   0    2G  0 lvm   
      ├─qubes_dom0-vm--whonix--ws--15--root--1625289726--back   253:26   0   10G  0 lvm   
      ├─qubes_dom0-vm--fedora--33--dvm--private                 253:27   0    2G  0 lvm   
      ├─qubes_dom0-vm--whonix--ws--15--private                  253:28   0    2G  0 lvm   
      ├─qubes_dom0-vm--whonix--ws--15--root                     253:29   0   10G  0 lvm   
      ├─qubes_dom0-vm--sys--firewall--private--1625289951--back 253:30   0    2G  0 lvm   
      ├─qubes_dom0-vm--default--mgmt--dvm--private              253:31   0    2G  0 lvm   
      ├─qubes_dom0-vm--sys--net--private                        253:33   0    2G  0 lvm   
      └─qubes_dom0-vm--sys--firewall--private                   253:35   0    2G  0 lvm   
sdb                                                               8:16   0    4G  0 disk  
├─sdb1                                                            8:17   0  600M  0 part  /boot/efi
└─sdb2                                                            8:18   0 1000M  0 part  /boot
sr0                                                              11:0    1  5.4G  0 rom   
```
```
Linux dom0 5.12.10-1.fc32.qubes.x86_64 #1 SMP Wed Jun 16 14:35:48 CEST 2021 x86_64 x86_64 x86_64 GNU/Linux
```