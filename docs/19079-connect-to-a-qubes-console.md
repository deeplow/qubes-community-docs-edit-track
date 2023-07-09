In some cases it's not possible to use a standard graphical terminal emulator to interact with a VM. In this case, "serial console" access is still available using two tools.

# qvm-console-dispvm

Usage: `qvm-console-dispvm VMNAME`

Launches a DispVM connected to the VM's console, using the qubes.ShowInTerminal RPC service. This provides a full-featured console.

At the time of writing this command contains a bug whose fix is waiting on release, therefore it may be necessary to use the following.

# xl console

Usage: `sudo xl console VMNAME`

Uses Xenlight to directly access the VM console from dom0. For [security reasons](https://github.com/QubesOS/qubes-vmm-xen/blob/xen-4.8/patch-tools-xenconsole-replace-ESC-char-on-xenconsole-outp.patch) this console is deliberately limited in what it can display.

Line-by-line text will work fine, but if a Curses-style pseudo-graphical-interface comes up the output will be garbled and you will need a tool like [asciinema](https://asciinema.org/) to untangle it. You may need to substitute all dots followed by `[`, `]`, `(` or `)` to the ASCII ESC (0x1b) character, a method that could have false positives.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/system/vm-console.md)
- First commit: 19 Oct 2019. Last commit: 20 Oct 2019.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): awokd, invalid-email-address
- Original author(s) (forum usernames): N/A
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>