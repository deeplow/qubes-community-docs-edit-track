Fellow Qubies, setting up networking for HVM can be a little tricky.

Therefore I would like to share a little bash script which I collected while reading different postings in this forum and on github:
```
#! /bin/bash

# set NetVM in dom0 for your HVM 
# everytime you change that setting with Qube Manager or
# in dom0's CLI eth0 in your HVM will get "down".
# and this script has to run again with correct IPs

# as root in your HVM terminal
systemctl disable --now NetworkManager

# set up your HVM's ip address and fire up device
ip a add 10.137.0.41/32 dev eth0
ip l set dev eth0 up

# if you are using a neighbor VM as uplink (i.e. sys-wireshark)
# setting up your route would look like this:
ip r add 10.137.0.9 dev eth0
ip r add default via 10.137.0.9 

# if you are using a disposable VM as uplink (i.e. sys-firewall)
# setting up your route would look like this:
ip r add 10.138.21.32 dev eth0
ip r add default via 10.138.21.32

sleep 10

# check your networking like this
ip -br a
ip r
curl http://1.1.1.1
curl http://google.com

# enjoy
```

**edit**:
1. added a `sleep` to script.
2. exchanged `ping` for `curl` since `ping` doesn't work with whonix-uplink