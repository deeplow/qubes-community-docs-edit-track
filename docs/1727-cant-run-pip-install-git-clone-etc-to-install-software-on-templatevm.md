Sometimes users need to install software on TemplateVMs that is _not_  available on the software respository for that templateVM's distribution. But first please try the [recommended (simpler and safer) method](https://www.qubes-os.org/doc/software-update-domu/#installing-software-in-templatevms) and to see if it's available.  In this post, I try to break down some of the alternatives.<div data-theme-toc="true"> </div>

> **Required reading**: from the official docs on [Trusting your TemplateVMs](https://www.qubes-os.org/doc/templates/#trusting-your-templatevms)

There are at least 3 methods:
- Temporarily allowing networking for software installation
- Updates proxy
- Copy from another VM

### Some examples of similar questions
[quote="tava, post:1, topic:1722"]
I use NordVPN, it uses wget, to download package, to template VM.
For security, Template VM has no internet access, but wget need Internet connection.
So I attach sys-net to template VM for temporary, to download NordVPN.
It means security has been compromised.
[/quote]

> I'm trying to build BitcoinArmory from source into a template VM but get the following error:
> $ git clone git://github.com/etotheipi/BitcoinArmory.git
> Cloning into 'BitcoinArmory'...
> fatal: unable to access 'https://github.com/etotheipi/BitcoinArmory.git/': Could not resolve host: github.com
> -- Zhang9000 at [google groups](https://groups.google.com/g/qubes-users/c/o-EO4QEUqhU/m/TTHO2rULBwAJ)

## (method 1) Temporarily allowing networking for software installation

This is by far the easiest (GUI only), but you're giving unchecked network access to the VM, but at least you don't forget to turn it off (as would happen if you say connect it to sys-firewall).

**Before proceeding**, read [this explanation](https://www.qubes-os.org/doc/software-update-domu/#temporarily-allowing-networking-for-software-installation) from the docs about this process.

1. open the TemplateVM's qube settings
2. on the "Basic" tab change networking to `sys-firewall` (never `sys-net` since sys-firewall [enforces network isolation between qubes](https://www.qubes-os.org/doc/firewall/#understanding-firewalling-in-qubes))
3. **Important**: go to the "Firewall rules" tab and select "Limit outgoing internet connections to..." and then on the bottom click the checkbox saying `Allow full network access for 5 min`.

4. You then have 5 min to do the network required part for installing the program on the template.

5. Go back to the Qube settings "Basic" tab and set the `Networking` to `None`.

![qube-settings|605x500](upload://c2ztaAqoCWE9RAT1KAHxJnBYHVf.png) 

(solution based on [this post](https://groups.google.com/g/qubes-users/c/o-EO4QEUqhU/m/TTHO2rULBwAJ))

## (method 2) Updates proxy

The [updates proxy](https://www.qubes-os.org/doc/software-update-domu/#updates-proxy) is how templateVMs are able to update software, even though they're not connected to the internet.

So if you want to `wget`, `pip install` or `git clone` for example you can proxy those applications to the updates proxy (running on `127.0.0.1:8082`).

Se bellow an example of this in practice
https://forum.qubes-os.org/t/external-repositories-pip-snap-appimage-persistent-installations-in-template-appvm/561/4

## (method 3) Copy from another VM

You can also download the required files on another VM (or even a DisposableVM) and [copy those files ](https://www.qubes-os.org/doc/copying-files/) to the TemplateVM.