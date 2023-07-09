These are text notes that I made from a presentation Harlo Holmes from Freedom of The Press Foundation (FPF) gave at the HOPE 2020 conference: [Qubes OS for Organizational Security Auditing](https://archive.org/details/hopeconf2020/20200730_1600_QubesOS_for_Organizational_Security_Auditing.mp4). The talk mainly about explaining how Qubes is ideal for this use-case and showing off the tooling Harlo uses to do security audits on Qubes as [part of the Digital Security Team at FPF](https://freedom.press/people/harlo-holmes/).
<div data-theme-toc="true"> </div>

These notes include most of Harlo's remarks and they've been curated to have links to the Qubes documentation and well as other reference material. Some content is also adapted.

The content is released under the [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) License, just like the original video.

# Provisioning Audit Environment
These are the main components of the security audit environment.

## VPN Proxy Qube

Qubes takes a "lego-block" approach to networking meaning that if you have an application running on a qube that is connected to the internet, it's not connected directly to the Internet. Instead it's first connected to a qube called `sys-firewall` - a qube with a firewall dedicated to keep connection the various application qubes you might run separate from one-another. And then `sys-firewall` connects to yet another VM called `sys-firewall`, which is a [Hardware-assisted Virtual Machine](https://qubes-os.org/doc/glossary/#hvm) (`HVM`) - and that allows it to interact with all of the radios, Ethernet card or anything that physically allows you to connect to the internet.

Deals with connectivity. You use this qubes in-between the AppVM that's running your internet-connected applications and your `sys-firewall`.

> *I will not touch your Internet!*
> *I brought by own Internet!*
> *I don't even trust my own Internet!*

Thanks to Qubes' lego-block approach, you can make it so every AppVM has is own route to the internet, no matter how convoluted it is (VPN over Tor, Tor over VPN, etc.)


## Analysis Qube

This is where the bulk of the work happens. Here you analyze and compile all the data. It has your standard [Kali tooling](https://qubes-os.orgdoc/pentesting/kali/).

- **Use of python virtual environments**

  *To install dependencies persistently without modifying the underlying template python virtual environments are used. This essentially installs the dependencies in the user-space. This is also used because by default [TemplateVM](https://qubes-os.org/doc/glossary/#templatevm) are made to only connect to their respective package managers via the internet. So running pip on the TemplateVM would fail.*

- **Inter-team communications**

  *This is the VM where communication among team-members happens (on slack).*


## Antarctica DispVM

Safe space to view sketchy stuff. It's non-networked [DisposableVM](https://qubes-os.org/doc/glossary/#disposablevm) that has tooling to interact with media visually and on metadata level to a modest degree.

- **OSQuery**

  *This is a tool that watches out for OS modifications as it interacts with files*

> **Tip**
>
> Create `.desktop` files for opening each file with the most appropriate application. This is done in the [TemplateVM](https://qubes-os.org/doc/glossary/#templatevm) that serves as base for the Antarctica DisposableVM.


## Network Recon Qube

A way to probe a network with physical interfaces rather than virtual ones.

Pretty much like the default `sys-net` but with network analysis tooling like nmap and wireshark.

### Use inter-qube communication to move recon data into Analysis Qube

The Qubes team always cautions users to always move data from more trusted VMs into less trusted VMs.

So, if in doubt that your Analysis Qube is more trusted than your Recon Qube, just [copy and paste](https://www.qubes-os.org/doc/copy-paste/) the dumps through the clipboard - since in the end it's all just text files.

Another more trustworthy way is to take screenshots (which are taken from dom0) and then [send them over](https://qubes-os.org/doc/copy-from-dom0/#copying-from-dom0) to the Analysis Qube.

### This qube is not connected to sys-firewall

The qube is not connected to any firewall proxy (like `sys-firewall`), so there is a bit more elevated risk - but this is the only actual way to probe the network while using Qubes.

### Plug in in a network peripheral

This qube gets attached a USB WiFi network peripheral (you don't want to mess anything up with your `sys-net`)


# Going beyond this setup

There are a few things you can also explore to go beyond this basic configuration. Here are some examples you can explore.

## Create your own RPC Policies

[Qubes RPC Policies](http://qubes-os.org/doc/rpc-policy/) are the way you configure permissions of which Qubes can interact with other Qubes and define how they can interact.
    
You can see these as the equivalent to you phone's permission system.


## Make one-way communication from Net Recon Qube -> Analysis Qube
    
Make it so the only files that can go out of the Network Recon Qube must go into the Analysis Qube.
        
If you have multiple Analysis Qubes (for different projects), then you'll want to use tags on those and target the RPC policy at those tags.

## Make your templates reproducible

Uniformity and standardization is key. Use SaltStack for provisioning uniform templates and setting up RPC policies.

[SaltStack](https://qubes-os.org/doc/salt/) is a management system similar to Ansible or Puppet. It will ease up your setting up a lot.
    
You can follow this guide by Kushal Das: <https://kushaldas.in/posts/maintaining-your-qubes-system-using-salt-part-1.html>

## Set data-retention policies

How can Qubes assist in a workflow that help mitigate data retention.
    
One example of how this happens is in the full exporting of the Analysis Qube to encrypted cold storage after we're done with the analysis.
    
Qubes makes this easy with its [backup utility](https://www.qubes-os.org/doc/backup-restore/).

> :warning: **Important**
>
> Do not check the box to store the encryption password on dom0!


# Communication

Communication with the clients is key, before, during and after the assessment. And while you as a security specialist may have preference for end-to-end means of communication, you sometimes have to meet your client where they are - especially during a pandemic.


## Zoom Video-conferences

In the particular circumstances of that pandemic we're in, you may find yourself having to use Zoom a lot. And it has received strong critiques from the security community. To this end, we'll use a setup with a DispVM to join zoom calls - so you don't have a persistent zoom identity.

```bash
# Attaches the microphone and webcam to a desired qube
# usage:
#   attach-webcam.sh dest_vmname
for c in mic usb; do
  qvm-device $c a $1 $(qvm-device $c list | grep -E "Camera|Microphone" | cut -d' ' -f1);
done
```

# What's next?

Is there anything that can be improved?

Do you have any other suggestions?

Contact Harlo on twitter [@harlo](https://twitter.com/harlo)