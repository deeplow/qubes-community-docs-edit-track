Hello, I just decided to try out this distro and was having problems getting my Wifi to work using a Broadcom card with the BCM4360 chipset and WL drivers. After a few days of troubleshooting, here are my steps to get it to work. This guide is an abridged version of [this](https://forum.qubes-os.org/t/hcl-apple-macbook-pro-11-1/15944/15) guide, with one additional step to make it work.

First, I created a new Debian 11 TemplateVM with the following settings:
```
Net Qube: None
Advanced -> Include in memory balancing: False
Advanced -> Mode: HVH
```

I then created a new AppVM using the network template I just created and attached my wireless card by using the 'qvm-pci' command in Dom0 as follows:
`"sudo qvm-pci attach *VM* *Device* --persistent -o no-strict-reset=True -o permissive=True"`

You can retrieve the ID of your device by using "sudo qvm-pci" and finding the Broadcom Network controller entry.

Using the new template VM, I installed the "broadcom-sta-dkms" package (version 6.30.223.271-17) using the package manager. I had no ethernet connection, so using a flash drive with an offline repo was necessary.

Next, I configured the AppVM as follows:

```
Start Qube Automatically on Boot: True
Advanced -> Provides Network: True
Services: Add clocksync and network-manager
```

Start the AppVM, and you should be using the correct (WL) drivers since the Broadcom package blacklists all the other ones by default. If you try to connect to a network, it will fail. I found that this chipset does not like it when Network Manager tries to assign a MAC address. Open Network Manager and select your network. Edit the entry and set "Cloned MAC Address" to "permanent." You should now be connected to your network.

I'm making this guide from memory, so if there are any issues, please let me know. I basically followed [this](https://forum.qubes-os.org/t/hcl-apple-macbook-pro-11-1/15944/15) guide, which was written for Fedora. The main things were to attach the network card with the "no-strict-reset" and "permissive" flags and set the "Cloned MAC Address" to be permanent. I would have never figured it out without that guide and ChatGPT to help debug things.