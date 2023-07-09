I wanted to monitor the thermal info to see if my CPU cooling works well or if there is a problem and my CPU is overheating.
But `sensors` can't find the coretemp device and don't show CPU temperature.
I've searched for this problem and found that in Xeb 4.8 it was possible for linux driver to get the thermal information but with this commit:
https://xenbits.xen.org/gitweb/?p=xen.git;a=commitdiff;h=72e038450d3d5de1a39f0cfa2d2b0f9b3d43c6c6
The thermal/performance leaf from CPUID was hidden from guests.
See related discussions:
https://xen.markmail.org/message/zmm4ug2ivp6y3uxo
https://xen.markmail.org/message/lufcl76bpbdnewpb
https://xen.markmail.org/thread/7dsviqxnchiyt456

Even without linux driver it is still possible to get the termal information by reading MSR in Xen up to version 4.14 like this:
0x1a2 - address of MSR_TEMPERATURE_TARGET and bits 24:16 is a value of target temperature. For my CPU it's 100.
0x1b1 - address of IA32_PACKAGE_THERM_STATUS and bits 22:16 is a target temperature minus current temperature value.
So this command gives me the current temperature value:
echo $(($(eval "rdmsr -f 24:16 -u 0x1a2")-$(eval "rdmsr -p 0 -f 22:16 -u 0x1b1")))

But in Xen 4.15 this was restricted as well:
https://xen.markmail.org/message/7rjl55ag5bosadvg
So before Xen devs make some interface to get thermal info from guests it will be impossible to see the CPU temperature starting with Xen 4.15.

I just wanted to share this info for those who will look for why they can't see the CPU thermal info with `sensors`.