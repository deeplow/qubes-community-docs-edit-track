Howdy,

At the moment when we use Ctrl+Shift+v the notification we receive is:

"**Qubes Clipboard**
Qubes Clipboard has been copied to the VM and wiped..."

Which I believe means that Dom0 clipboard is wiped. Not the original outgoing VM, nor the receiving VM.

What I would like to learn how to configure is when certain steps of the Copy & Paste sequence between VMs are completed, for that to trigger a countdown timer that will automatically wipe the outgoing and incoming VM clipboard. 

Time Trigger Example:

1. (vm1) Ctrl+c: Bytes copied to vm1 clipboard, and 30 second wipe timer begins for vm1 clipboard; 
if Ctrl+c is used again in vm1 before 30 seconds has elapsed, it will wipe the previously copied bytes and replace with new.

2. (vm1) Ctrl+Shift+c: Bytes transferred from vm1 clipboard to Qubes Clipboard.

3. (vm2) Ctrl+Shift+v: Bytes transferred from Qubes Clipboard to vm2 clipboard, and immediately wipe Qubes Clipboard (already happens).

4. (vm2) Ctrl+v: Bytes pasted from vm2 clipboard, and 30 second wipe timer begins for vm2 clipboard; 
if Ctrl+Shift+v is used again to transfer bytes from Qubes Clipboard to vm2 clipboard before 30 seconds has elapsed, it will wipe the previously copied bytes in vm2 clipboard and replace with new.