> :warning: **Please note** This is a *work in progress guide* (WIP) created to crowdsource user experience about using Windows in Qubes, optionally with Qubes Windows Tools ("QWT"), following up on [this github issue](https://github.com/QubesOS/qubes-issues/issues/3585).

Please contribute too ! It's easy: edit this wiki page (the edit/'pen' icon at the bottom of the post), copy the content of the [user report template](#template) at the end of this post and paste it in the relevant "Contributed user reports" Windows sections. Even is someone has already added a report with the same version of Windows (and optionally QWT) it's perfectly fine to add another report as your use case (/features you use) might differ.


# General resources

Please read the [Windows qube documentation](https://www.qubes-os.org/doc/windows/) (thanks to @GWeck the community documentation is now updated for Qubes OS R4.1 so this section's content is deleted).

# Contributed user reports

## Windows 7

[details="R4.1 / Windows 7 Pro SP1 updated until Oct 2020 / QWT 4.1.67 of 2022-02-14"]
@GWeck; date: 23 Feb 2022, updated 26 March 2022

Windows:
- installed from scratch as template VM
- build/iso: Windows7ProfSP1.iso of 2016-05-28, downloaded from Microsoft
- updated using WinFuture Patch kit "WinFuture_7SP1_x64_UpdatePack_2.107_Januar_2020-Vollversion.exe" and manual updates after that
- ram used when installing: 4GB
- ram usage after install: 4GB 
- disk space usage after install: 27GB

QWT:
- first installation
- installed just after completing the update horror to get the system current
- features selected during installation:
  - Base Xen PV drivers
  - Network and Disk drivers
  - Move User Profiles
- features that were tested to work:
  - build / use AppVM based on that template
  - seamless mode (dynamic via Qube Manager and static via registry)
  - audio output (needs to activate Windows Audio Endpoint Builder service)
  - copy/paste between qubes (both directions in and out)
  - copy files between qubes (both directions in and out)
  - attaching USB devices to the qube
  - networking (for AppVM based on that template)
  - time/clock synchronization using `qvm-features VMname timezone localtime`
  - setting decent screen resolution for non-seamless mode using Alt-F8 key
  - user migration from `C:` to the qube's private volume (needs to rename drive `D:` to `Q:` **before** QWT installation)

- features that don't work:
  - attaching SATA and NVME devices to the qube (crashes the qube)

Xen disk and network drivers can be installed during installation or after completing the previous steps. This will probably cause Windows activation to become invalid, but the activation can be restored using the Microsoft telephone activation method. After this, USB devices can be attached and used, and booting is about two thirds faster.

Summary / notes: can be reasonably used in seamless mode; access to functions via XFCE menu or by hitting Windows keyboard key in a VM's window and thus displaying the Windows menu 

[/details]

## Windows 10

[details="R4.1 / Windows 21H2 / QWT 4.1.67 - Feb. 2022"]
@taradiddles; date: 20 Feb 2022

Windows:
- installed from scratch
- build/iso: 21H2, downloaded from Microsoft
- ram used when installing: 4GB
- ram usage after install: 1.1GB 
- disk space usage after install: 12GB

QWT:
- first installation
- installed just after windows' first boot
- features selected during installation: Xen PV drivers
- features that were tested to work:
  - copy/paste between qubes
  - copy files between qubes
  - attaching *usb* devices to the qube
  - networking
  - time/clock synchronization
  - XEN PV disk driver
  - XEN PV network driver
- features that don't work:
  - user migration from `c:` to the qubes' private volume

Summary / notes: "vanilla" windows really feels sluggish, it then takes a lot of time and patience to remove bloatware and optimize the vm to make it usable.

[/details]


[details="R4.1 / Windows AME 21H1 / QWT 4.1.67 - Feb. 2022)"]
@taradiddles / 12 Feb 2022

Windows:
- installed from scratch
- build/iso: ameliorated 21H1 (downloaded ISO).
- disk space required by the installer: min is 16GB, I've set it to 20GB
- ram usage after install: <1GB
- windows update status: disabled

QWT:
- first installation 
- installed just after windows' first boot (windows AME has windows update disabled anyway).
- features selected during installation: Xen PV drivers
- features that were tested to work:
  - copy/paste between qubes
  - copy files between qubes
  - attaching *block* devices to the qube (no 'eject' functionality)
  - attaching *usb* devices to the qube
  - networking
  - time/clock synchronization
  - XEN PV drivers
- features that don't work:
  - user migration: the profile on `c:` wasn't migrated (again, maybe because of AME tweaks).

Summary: windows AME is really snappy and works well so far but it lacks features like appx (windows store) that could make it a no-go for some.
[/details]



## Windows 11

[details="R4.1 / Windows 11 Pro 21H2 / QWT 4.1.67 of 2022-02-14"]
@GWeck; date: 23 Feb 2022, updated 26 March 2022

Windows:
- installed from scratch as template VM, using TPM-disable patch during installation
- build/iso: 21H2, downloaded from Microsoft
- ram used when installing: 4GB
- ram usage after install: 4GB 
- disk space usage after install: 15GB

QWT:
- first installation
- features selected during installation:
  - Base Xen PV drivers
  - Network and Disk drivers
  - Move User Profiles
- features that were tested to work:
  - build / use AppVM based on that template
  - setting decent screen resolution for non-seamless mode
  - copy/paste between qubes (both directions in and out)
  - copy files between qubes (both directions in and out)
  - attaching USB devices to the qube
  - audio output (somewhat scratchy)
  - user migration from `C:` to the qubes' private volume `Q:`
  - networking (for AppVM based on that template)
  - time/clock synchronization using `qvm-features VMname timezone localtime`
- features that don't work:
  - attaching SATA and NVME devices to the qube (crashes the qube)
  - seamless mode

Xen disk and network drivers can be installed during installation or after completing the previous steps. Contrary to Windows 7, activation did not become invalid. After this, USB devices can be attached and used, and booting is about one third faster.

Summary / notes: rather slow, as well on booting and shutdown as on using; installation requires disabling the check for TPM 2.0, using the trick described in [Windows 11 in Qubes](https://forum.qubes-os.org/t/windows-11-in-qubes/6759/8) - using Windows 11 is a good motivation for migrating to Linux :-)

[/details]

# <a href="template"></a>User report template

The template below is meant to be improved ! It isn't exhaustive by any means and most of the fields aren't mandatory.

More detailed notes about a given Windows/QWT combination (eg. very detailed installation instructions, workarounds, hints/tips, user workflow, ...) should be posted to a separate post with a "Guide" tag and linked to this wiki page in the user report: that way the post's author is free to use whatever layout and amount of information he/she sees fit, and this keeps relevant questions/answers threads contained in a post rather than in the more "generic" comments here. That said it's OK to add a bit more "free text" to the template when contributing a report to avoid having to create a dedicated post with only a few lines.

(In case you want to change the template's text itself, please discuss any major changes in this post's comments).

> :warning: Copy the text in the text area below including the `[details=...]` and `[/details]` tags


```text
[details="R4.x / Windows XXX / QWT XXX"]
@userxyz ; date: xx month year

Windows
- installed from scratch, or migrated from an older Qubes OS release ?
- build/iso [eg. '21H1', 'ameliorated 20H1', ...]
- disk space required by the installer [if known]
- ram used when installing [doesn't mean it is the required amount]
- ram usage after install [if known]
- disk space usage after install [if known]
- if display resolution was changed, does it work ?
- if audio was tested, does it work ?
- problems running the VM ?

QWT [optional]
- first installation or migration/re-installation over an older version ?
- installed just after windows' first boot, or after a full windows update ?
- features selected during installation if not the default choice [eg. Xen PV drivers].
- features removed during installation if not the default choice [eg. UAC].
- features that were tested to work [delete line that aren't relevant/not tested]:
  - copy/paste between qubes
  - copy files between qubes
  - attaching *block* devices to the qube [with widget under "Data (Block) devices" or with `qvm-block`]
  - attaching *usb* devices to the qube [with widget under "USB devices" or with `qvm-usb`]
  - attaching audio input devices to the qube [with widget under "Audio Input"]
  - networking
  - time/clock synchronization
  - XEN PV disk driver
  - XEN PV network driver
  - user migration from `c:` to the qubes' private volume to be able use the qubes as a TemplateVM).
- features that don't work [possibly with workarounds]: ...

Summary / notes [if any]:

Link to a specific post [if any - it could contain detailed instructions, known issues, workarounds, hints/tips, description of the author's workflow, productivity tips, ...]

[/details]
```


<div data-theme-toc="true"> </div>