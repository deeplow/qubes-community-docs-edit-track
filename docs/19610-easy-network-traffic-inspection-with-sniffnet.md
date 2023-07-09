Hi, I just found this project https://github.com/GyulyVGC/sniffnet Here is how to use it on sys-net to have a quick overview of what's happening on your network

# Installation

## Fedora based sys-net

1. Get the download link for the latest release: https://github.com/GyulyVGC/sniffnet/releases , depending of your sys-net system, pick `Sniffnet_LinuxRPM_x86_64.rpm`
2. Download the file in sys-net
3. Open a terminal in sys-net
4. Type the following command to install the program: `sudo rpm -i Sniffnet_LinuxRPM_x86_64.rpm`
5. Type the following command to run the program: `sniffnet`

## Debian based sys-net

1. Get the download link for the latest release: https://github.com/GyulyVGC/sniffnet/releases , depending of your sys-net system, pick `Sniffnet_LinuxDEB_amd64.deb`
2. Download the file in sys-net, if it's an AppVM, you can store the file in the home directory
3. Open a terminal in sys-net
4. Type the following command to install the program: `sudo dpkg -i Sniffnet_LinuxDEB_amd64.deb`
5. Type the following command to run the program: `sniffnet`

# Persistency

sys-net should either be an AppVM or fully disposable, so installing a package in it like we did above won't persist after a reboot. There are different solutions though:

## Install on an AppVM sys-net

If you are a wifi user, you are likely to have an AppVM where /home/ is persistent.

In order to install sniffnet automatically at every boot, modify the file `/rw/config/rc.local` to add the command installing the program as explained above, make sure to use the full path to the file, like `/home/user/Sniffnet_LinuxDEB_amd64.deb` (example using the Debian file name).

## Install sniffnet everywhere

This is my least favorite but the most practical. You can install sniffnet in the template used by sys-net (or the template for the dvm template). Sniffnet can be barely trusted, it's not ideal to do that, but this would provide siffnet in all your qubes.

## Install in a disposable sys-net

This setup is trickier, the easiest way (but not really bandwidth efficient) is to download the file at every boot and install it, but this should be done in the DVM template. I won't go into details, it's meant for users who understand the process.

- edit the rc.local file for the DVM template
- use something like this (not tested)

```
if [ "$(hostname)" = "sys-net" ]
then
  cd /tmp/
  curl -OL https://path/to/package_file
  rpm -i package_file # for fedora
  dpkg -i package_file # for debian
fi
```

# Screenshots

## Startup screen to select a network interface
![sniffnet_01|690x414, 100%](upload://1vlwrnj5lrZOgHQMkL0qJfRmML7.png)

## Realtime traffic
![sniffnet_02|690x414](upload://4AOdtwv1SARPGJivAsRNnN71bjt.png)

## Traffic inspection, allowing filters
![sniffnet_03|690x414](upload://avkkXkiiQ4yGVCIRERy9zSdDrmQ.png)