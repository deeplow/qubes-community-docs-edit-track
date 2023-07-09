**Why would anyone want to do this?**

Both evince and okular are very nice PDF viewers and they will do the job 90% of the time. I find however that I frequently have to deal with PDF files from either a government source (forms) or some DocuSign contracts that cannot be opened in any of the available open source PDF viewers on Linux. It is those documents that force me to either user Adobe Reader on a Windows machine or run Adobe Reader 9 for Linux.

The later one is discontinued and one has to deal with 32-bit binaries, but at least I can install it in a debian-11-minimal based template which in turn can be the basis of an offline dispvm. Yes, you could have an offline Windows VM or do wine ... I just think this is easier, lighter and does the job. In any case Adobe Reader and those PDFs that only open in them are for sure spyware. Their very reason for existence is to track when you open those files and what you do with them. Hence: offline qube. :slight_smile: 

**Will I be able to print?**

Yes, using the "Custom..." setting in the Adobe Reader's print dialog, which in turn will use `lp`. Just make sure you have a default printer setup. `lpstat -v` will show you the installed printers, then use `sudo lpadmin -d Your_Printer_Name` to set the default. Verify via `lpstat -d`.

**Here we go...**

1. Get a copy of ftp://ftp.adobe.com/pub/adobe/reader/unix/9.x/9.5.5/enu/AdbeRdr9.5.5-1_i386linux_enu.deb
2. `sudo dpkg --add-architecture i386`
3. `sudo apt update`
4. `sudo apt install --no-install-recommends -y AdbeRdr9.5.5-1_i386linux_enu.deb`
5. `sudo apt install --no-install-recommends -y libgdk-pixbuf2.0-0:i386 gtk2-engines-pixbuf:i386 gtk2-engines-murrine:i386 libidn11:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libxml2:i386 gnome-themes-extra:i386`

No guarantees about step 5 containing all packages for all use cases, but these are the ones I had to install to get no further complaints when running `acroread`.