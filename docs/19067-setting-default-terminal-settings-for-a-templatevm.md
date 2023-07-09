When you create a VM based on a TemplateVM, the `gnome-terminal` settings (font, color) are not inherited by default. This document describes how to set terminal defaults for all VMs *subsequently* created off a TemplateVM.

(Previously-created VMs are unaffected.)

This document only applies to `gnome-terminal` (the standard terminal) and not XTerm, etc.

Thanks to `unman` on qubes-users for explaining how to do this.

# Define your defaults

In dom0: `qvm-run MYTEMPLATE gnome-terminal`

In the terminal that pops up, adjust settings to your liking.

# Save settings template-wide

In the templateVM's terminal:

```
sudo mkdir -p /etc/skel/.config/dconf
sudo cp ~/.config/dconf/user /etc/skel/.config/dconf/
sudo reboot
```

Subsequently-created VMs should now use the chosen settings by default.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/customization/terminal-defaults.md)
- First commit: 19 Oct 2019. Last commit: 19 Oct 2019.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): null
- Original author(s) (forum usernames): N/A
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>