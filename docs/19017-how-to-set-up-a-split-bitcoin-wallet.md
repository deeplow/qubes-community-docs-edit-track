# What is a "Split" Bitcoin Wallet?

A "split" bitcoin wallet is a strategy of protecting your bitcoin by having your wallet split into an offline "[cold storage](https://en.bitcoin.it/wiki/Cold_storage)" wallet and an online "watching only" wallet.

# A "Watching" Wallet and a "Cold" Wallet

1.  Create a fedora-25-electrum template using the Qubes VM Manager or running `qvm-clone fedora-25 fedora-25-electrum` in dom0.

2.  Start the new template: `qvm-start fedora-25-electrum` `qvm-run fedora-25-electrum xterm`

3.  Install `electrum` to fedora-25-electrum template VM. From fedora-25-electrum terminal enter: `sudo dnf update`. `sudo dnf install electrum`.

4.  Shut down your `fedora-25-electrum` template

5.  Create an `offline-bitcoin` qube based on `fedora-25-electrum` using the Qubes VM Manager or running `qvm-create -t fedora-25-electrum -l black offline-bitcoin` and `qvm-prefs -s offline-bitcoin netvm none` in dom0.

6.  Follow the [electrum documentation in creating an offline wallet](http://docs.electrum.org/en/latest/coldstorage.html#create-an-offline-wallet)

7.  Create a `watching-bitcoin` qubes based on `fedora-25-electrum` connecting to the internet how ever you prefer using the Qubes VM Manager or running for example `qvm-create -t fedora-25-electrum -l green watching-bitcoin` and `qvm-prefs -s watching-bitcoin netvm sys-whonix` in dom0.

8.  Follow the [electrum documentation in creating an online watching-only wallet](http://docs.electrum.org/en/latest/coldstorage.html#create-a-watching-only-version-of-your-wallet)

# Important Notes

- The private keys (xpriv) should never be moved outside of `offline-bitcoin`.
- For copying out the public keys (xpub), Qubes provides two secure, convenient methods: the [inter-VM clipboard](https://www.qubes-os.org/doc/copy-paste/) and [inter-VM file copy](https://www.qubes-os.org/doc/copying-files/) tools. Compared to traditional physically air-gapped machines, these tools make it very easy to copy out public keys.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/security/split-bitcoin.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>