In some cases you maybe need combine sys-usb with sys-net. But it's less secure than having sys-net and sys-usb separate, so be aware of it before doing it. To do it :

* In the following file :

nano /etc/qubes-rpc/policy/qubes.InputKeyboard
nano /etc/qubes-rpc/policy/qubes.InputMouse

replace from 

`sys-usb dom0 allow,user=root`

to 

`sys-net dom0 allow,user=root`


* Shutdown 

Go in the sys-net terminal and shut it down, for exemple with init 0 
Go in the sys-usb terminal and shut it down, for exemple with init 0

* Transfer the usb controler from sys-usb to sys-net

Go in the settings of your sys-usb Qube and disable "start on boot" and apply your modification 
Go in the settings of your sys-net Qube, and in the devices section, find the usb controler of your computer, selected it and apply your modification.

* You can start now sys-net