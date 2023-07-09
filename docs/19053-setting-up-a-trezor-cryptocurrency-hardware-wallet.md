using a Fedora-based sys-usb VM and a Whonix WS-based application VM:

- navigate to the [Trezor instructions](https://wiki.trezor.io/Qubes_OS) page and read them. They are more frequently updated than this document.

- in dom0: `sudo vim /etc/qubes-rpc/policy/trezord-service` add this line: `$anyvm $anyvm allow,user=trezord,target=sys-usb` replace `sys-usb` with `disp-sys-usb` if you are using a disposable sys-usb

- in the sys-usb VM, or for disp-sys-usb, the VM on which it is based (in both cases, assumed to use a fedora-3x template): `sudo mkdir /usr/local/etc/qubes-rpc` `sudo vim /usr/local/etc/qubes-rpc/trezord-service` and add this line to trezord-service: `socat - TCP:localhost:21325`

- in the whonix-based application VM: `pip3 install --user trezor` `sudo vim /rw/config/rc.local` add this line (note the "&" at the end): `socat TCP-LISTEN:21325,fork EXEC:"qrexec-client-vm sys-usb trezord-service" &`

- in the fedora-3x template: `sudo dnf install trezor-common`

- download the bridge RPM from <https://wallet.trezor.io/#/bridge> and remember to verify it!

- copy to fedora-3x

- in fedora-3x `sudo rpm -i /path/to/trezor.rpm`

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/common-tasks/setup-trezor-cryptocurrency-hardware-wallet.md)
- First commit: 27 Aug 2021. Last commit: 27 Aug 2021.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): null
- Original author(s) (forum usernames): N/A
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>