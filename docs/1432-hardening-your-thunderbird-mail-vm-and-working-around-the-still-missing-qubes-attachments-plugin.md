I finally took the time to upgrade my Thunderbird and think about how I could work around the incompatibility of the Qubes Attachments plugin.

For those who don't know: This plugin provides functionality like "Open in DVM" or "Send to VM" for attachments that you receive in Thunderbird. It is unfortunately not compatible with the new Thunderbird code base and thus is no longer working.

I just posted my workaround to the Github issue dealing with this incompatibility (https://github.com/QubesOS/qubes-issues/issues/5861) and thought it would be a good topic for this forum as well. So here it goes, copy-paste from my Github response:

**Edit: I forgot that the changes would not survive a VM restart. I updated the steps below to fix this.**

**Please note: While the following steps worked for me I know of at least one other Qubes installation in which they somehow didn't work. I currently don't know why this happens, but if someone else experiences some issues we could maybe debug this together.** 

In a Terminal of your mail VM execute the following:

**Edit 2: It seems I specified a wrong path (again, *sigh*). I hope, this time it works.**
* `sudo cp /usr/share/applications/mimeapps.list /home/user/.config/mimeapps.list`
* `sudo sed -i "s/=.*/=open_in_dispvm.desktop;/g" /home/user/.config/mimeapps.list`

These two commands set an application "open_in_dispvm" as the default value for all mime-types that the system knows about. Now create this application and make it execute anything in a VM of your choice:

* `nano /home/user/.local/share/applications/open_in_dispvm.desktop`

Enter the following:

```
[Desktop Entry]
Encoding=UTF-8
Name=Open_in_DispVM
Exec=qvm-open-in-vm <VM_OF_YOUR_CHOICE> %u
Terminal=false
X-MultipleArgs=false
Type=Application
```

Instead of <VM_OF_YOUR_CHOICE>, specify the name of an existing VM. Now, whenever you click on an application it should call "qvm-open-in-vm" instead of opening it inside of the Mail VM. You could also call `qvm-open-in-dvm` instead.

Personally, I combine it with a modified RPC-policy in dom0:

* In a dom0 terminal, do `sudo nano /etc/qubes-rpc/policy/qubes.OpenInVM` . Replace whatever might be there with `<NAME_OF_YOUR_MAIL_VM> $anyvm ask` .

That way, every time I try to open anything in the mail VM Qubes does not just use the <VM_OF_YOUR_CHOICE> that I specified in the .desktop-file, but asks me in which VM I want to open it and I can easily redirect everything as I wish:

* something I want to print goes to my print VM
* a hyperlink could be opened in a new dispVM
* or I could choose to open it in an already existing VM
* ...

I *think* this also leads to hyperlinks being opened in a VM of your choice but since I already had that set up before, I am not sure. So please, let me know if opening links works as expected.

The only "downside" of this approach is that just copying files to a VM of your choice without opening them there is not trivially possible. However, you can still save any attachment in your mail VM locally and then right click -> "Move to other AppVM...". If anyone wants, it should quite easily be possible to create a wrapper script which is then called by the .desktop file.
This script could ask whether you want to copy/move/open a file and act accordingly.

In theory, it should even be possible to make a package out of this and contribute to the new [QubesOS contrib repository](https://forum.qubes-os.org/t/qubes-os-contributed-packages-are-now-available/958).