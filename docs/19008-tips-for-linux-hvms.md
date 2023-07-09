# How to fix bootup kernel error

If the HVM pauses on boot and shows a series of warnings, visit [HVM Troubleshooting](https://www.qubes-os.org/doc/hvm-troubleshooting/#hvm-pauses-on-boot-followed-by-kernel-error) for a fix.

# Screen resolution

Some kernel/Xorg combinations use only 640x480 in HVM, which is quite small. To enable maximum resolution, some changes in the Xorg configuration are needed:

1.  Force "vesa" video driver
2.  Provide wide horizontal synchronization range

To achieve it (all commands to be run as root):

1.  Generate XOrg configuration (if you don't have it):

    ```
    X -configure :1 && mv ~/xorg.conf.new /etc/X11/xorg.conf
    ```

2.  Add HorizSync line to Monitor section, it should look something like:

    ```
    Section "Monitor"
            Identifier   "Monitor0"
            VendorName   "Monitor Vendor"
            ModelName    "Monitor Model"
            HorizSync    30.0 - 60.0
    EndSection
    ```

3.  Change driver to "vesa" in Device section:

    ```
    Section "Device"
            # (...)
            Identifier  "Card0"
            Driver      "vesa"
            VendorName  "Technical Corp."
            BoardName   "Unknown Board"
            BusID       "PCI:0:2:0"
    EndSection
    ```

Now you should get resolution of at least 1280x1024 and should be able to choose other modes.

# Qubes agents

Linux Qubes agents are written primarily for PV qubes, but it is possible to run them also in a HVM qube. However some work may be required to achieve this. Check [this thread](https://groups.google.com/group/qubes-devel/browse_thread/thread/081df4a43e49e7a5).

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/linux-hvm-tips.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>