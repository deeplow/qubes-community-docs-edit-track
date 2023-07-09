1.  Create a StandaloneVM with the default template.
2.  Replace `vmlinuz` with the `netbsd-INSTALL_XEN3_DOMU` kernel.
3.  During setup, choose to install on the `xbd1` hard disk.
4.  Attach the CD to the VM.
5.  Configure the networking.
6.  Optionally enable SSHD during the post-install configuration.
7.  Replace the kernel with `netbsd-XEN3_DOMU`.
8.  The VM may fail to boot automatically, in which case you must explicitly specify `xbd1a` as the root device when prompted.

For further discussion, please see this [thread](https://groups.google.com/group/qubes-devel/msg/4015c8900a813985) and this [guide](https://wiki.xen.org/wiki/How_to_install_a_NetBSD_PV_domU_on_a_Debian_Squeeze_host_%28Xen_4.0.1%29).

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/netbsd.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>