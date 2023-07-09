Hi, i would like to handle a vpn access (mull vad).
I did the following things:
- clone the fedora34 template
- install the vpn software in the cloned template (open the firewall temporary)
- made vpn application available for template
- made the network connection available for qubes
- create a "vpn" qube with application vpn.

And it works.

My first question: Is this the right way? 

Next I realized, that when i restart the computer i always have to re-enter the access data for vpn access. probably because the template has read-only permissions(?)

The qube (or template?) does not remember the access data.

My second question: How can i permanent save these access data?