For anyone curious about how to batch-install Qubes OS, this guide by the Fedora Project is incredibly helpful:

----

https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/advanced/Kickstart_Installations/#chap-kickstart-installations

----

https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/advanced/Network_based_Installations/#chap-pxe-server-setup

------

https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/advanced/Boot_Options/#sect-boot-options-kickstart

-----

This will be helpful for:
-  Anyone considering deploying Qubes OS in a work environment
    - Quick and easy remote installation of work machines
    - Can be deployed onto a PXE server, via NFS, FTP, HTTP and HTTPS
    - Initial Install and First Boot options can be completely customised.  
    - Every Qubes OS install already comes with Kickstart files.  For anyone curious, check your dom0 root directory for `/root/anaconda-ks.cfg` and `/root/initial-setup-ks.cfg`.
    - The PXE server could even potentially be an AppVM on another Qubes OS machine :scream:

-  Anyone who needs a "quick and painless" zero-interaction way to install Qubes OS
    - Maybe your laptop is lost/stolen/damaged/seized, and you want to get back your custom-configured Qubes OS back up and running ASAP.  Just plug it in, PXE network boot, go get a coffee, and you'll have your Qubes OS machine back before you know it!
    - Maybe you created an awesome Qubes OS which you've spent a long time configuring and tweaking, and you want to share it with other people.  You could set up a PXE server with the ISO and your Kickstart file.  All the other person needs to do is boot from your PXE server, and the installer does the rest!
    -  Maybe you just want to run your Qubes OS dom0 in RAM.  With a bit of tweaking this guide could be adapted to that purpose...

----

I'm writing a Qubes OS-specific guide derived from these guides, and I will upload it when it's ready.  (It's on my list of things to do :kissing:)

Now all we need is a GUI tool for developing SaltStack configs that create 100% custom VMs (I'm not going to lie, I'm a little confused by the .top and .sls files, where they go, why they can't just be a single file etc., but I'm trying!), and we've got a 100% automated, easy-to-use, and zero-interaction method to set up every single aspect of a Qubes OS machine :sunglasses: