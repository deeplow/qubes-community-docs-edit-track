I spent a little bit of time of this, so in case someone runs into the same issue it could help.

I was using the qubes-template-builder with F32 minimal to create an archlinux template,
"make template" threw an error so I had to make a little modification to get it built:

It was breaking due to a dependency issue - so the fix was to **comment out "font-bitstream-speedo" in the qubes-src/builder-archlinux/scripts/packages.list**


So then the template was about to build, and install
But another issue was the qubes-gui-common etc files for the thunar dropdown to copy/view etc between VMs were unavailable (apparently due to some package conflicts).

**The solution without downgrading any packages was:**
In thunar file manager, click view > configure custom actions, and recreate the menus from a working vm, like for like. 
Then if you have more arch vms, you can take this file from /home/user/.config/Thunar/ and copy it to any other affected arch templates/appvms.

Hope this helps someone.