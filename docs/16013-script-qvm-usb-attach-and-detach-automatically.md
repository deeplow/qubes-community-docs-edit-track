Just in case someone need that little script to copy paste in dom0

**Use case :** 

I have two USB key. But I will plug them on the same port.
So for qvm-usb, they will have the same port number so I can't use --persistent as  : 
- I want USB A to automatically attach to Vault 
- USB B to stay on usb-net

I did it fast, I will improve it later 

```
#!/bin/sh

while true 
do 
   	usb=$(qvm-usb| grep usbA) 
        #echo Result + $usb
        if [ -n "$usb" ]; 
        then
            	qvm-usb attach Vault sys-net:2-2
                echo "Attach"
        else 
                qvm-usb detach Vault sys-net:2-2
                echo "Detach"   
        fi
        sleep 5
done

```