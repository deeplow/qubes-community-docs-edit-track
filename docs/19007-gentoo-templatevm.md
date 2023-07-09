If you would like to use a stable, predictable, manageable and reproducible distribution in your AppVMs, you can install the Gentoo template, provided by Qubes in ready to use binary package. For the minimal and Xfce versions, please see the [Minimal TemplateVMs](https://www.qubes-os.org/doc/templates/minimal/) and [Xfce TemplateVMs](https://www.qubes-os.org/doc/templates/xfce/) pages.

# Installation

The standard Gentoo TemplateVM can be installed with the following command in dom0:

```
[user@dom0 ~]$ sudo qubes-dom0-update --enablerepo=qubes-templates-community qubes-template-gentoo
```

To switch, reinstall and uninstall a Gentoo TemplateVM that is already installed in your system, see *How to [switch](https://www.qubes-os.org/doc/templates/#switching), [reinstall](https://www.qubes-os.org/doc/reinstall-template/) and [uninstall](https://www.qubes-os.org/doc/templates/#uninstalling)*.

### After Installing

After a fresh install, we recommend to [Update the TemplateVM](https://www.qubes-os.org/doc/software-update-vm/). We highlight that the template memory/CPU allocation certainly need to be adjusted in some cases. As Gentoo is a *linux source distribution*, the template needs resources to perform updates or installing any packages. By default, each TemplateVM has *2 VCPUs* for *4000 MB Max memory* allocated. If needed, double those values, *4 VCPUs* for *8000 MB Max memory*. For example, it has been observed failing updates or builds with *4 VCPUs* for *4000 MB Max memory* due to out of memory issue. For more general considerations, we refer to the official [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:AMD64).

# Want to contribute?

- [How can I contribute to the Qubes Project?](https://www.qubes-os.org/doc/contributing/)

- [Guidelines for Documentation Contributors](https://www.qubes-os.org/doc/doc-guidelines/)

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/gentoo.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>