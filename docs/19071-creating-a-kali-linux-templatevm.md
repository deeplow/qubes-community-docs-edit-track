# Warnings

- The installation scripts and provided tools may have bugs, be vulnerable to Man in the Middle (MitM) attacks or other vulnerabilities.
- Adding additional repositories or tools for installing software extends your trust to those tool providers.
- Please keep in mind that using such a template for security and privacy critical tasks is not recommended.
- Kali Linux distribution is a rolling distribution based on Debian testing release, so it will always have a newer software base than available in the Qubes OS Debian template. Keep in mind that this may result in problems (especially in regard to package dependencies) not covered by this tutorial.

# From the official ISO file <a name="hvm4_0"/>

Only use this method if you want the full Kali GUI (desktop, fancy menus, etc.). It comes at the cost of much greater resources consumption.

1.  Download the Kali ISO
2.  [Create a new HVM](https://www.qubes-os.org/doc/standalone-and-hvm/)
3.  Start the HVM with attached CD/DVD

``` shell_session
$ qvm-start <hvm-name> --cdrom <vm-name>:/home/user/Downloads/<iso-name>.iso
```

# From a Debian template <a name="templatevm-from-debian4_0"/>

This is the recommended method. Easier to maintain and less demanding on resources, but you won’t have the full Kali GUI.

If you need to install custom kernel modules (wifi drivers, …) you need to use the kernel provided by Kali instead of the kernel provided by Qubes, see [Managing VM Kernel.](https://www.qubes-os.org/doc/managing-vm-kernel/)

The steps can be summarized as:

1.  Install Qubes stable Debian template
2.  Upgrade from Debian `stable` to Debian `testing` for Qubes repositories
3.  Add `testing` and `securitytesting` Qubes repositories
4.  Replace the content of `/etc/apt/sources.list` file with the Kali repository
5.  Update the template

# Get Kali Linux PGP key

**CAUTION:** Before proceeding, please carefully read [On Digital Signatures and Key Verification](https://www.qubes-os.org/security/verifying-signatures/). This website cannot guarantee that any PGP key you download from the Internet is authentic. In order to obtain a trusted fingerprint, check its value against multiple sources. Then, check the keys you download against your trusted fingerprint.

This step is required since by (security) default TemplateVM do not have a direct Internet connectivity. Users understanding the risks of enabling such access can change this configuration in firewall settings for the TemplateVM.

1.  Retrieve the Kali Linux PGP key using a DisposableVM.

``` shell_session
$ gpg --keyserver hkps://keys.openpgp.org --recv-key 44C6513A8E4FB3D30875F758ED444FF07D8D0BF6
$ gpg --list-keys --with-fingerprint 44C6513A8E4FB3D30875F758ED444FF07D8D0BF6
$ gpg --export --armor 44C6513A8E4FB3D30875F758ED444FF07D8D0BF6 > kali-key.asc
```

2.  **DO NOT TURN OFF** the DisposableVM, the `kali-key.asc` file will be copied in the Kali Linux template for a further step.

3.  Make sure the key is the authentic Kali key. See the [Kali website](https://docs.kali.org/introduction/download-official-kali-linux-images) for further advice and instructions on verification.

# Create a Kali Linux (rolling) template

These instructions will show you how to upgrade a Debian TemplateVM to Kali Linux.

1.  (Optional) Check for latest Debian stable template and install it (if not already done)

``` shell_session
# qubes-dom0-update --action="search all" qubes-template-debian
# qubes-dom0-update <latest Debian template>
```

2.  Clone `debian-X` template

``` shell_session
$ qvm-clone debian-<X> kali-rolling
```

3.  Check the name of currently used repository in `/etc/apt/sources.list.d/qubes-r<X>.list` and current testing [Debian release](https://www.debian.org/releases/). Update repository list accordingly

``` shell_session
# sed -i 's/<current stable>/<current testing>/g' /etc/apt/sources.list.d/qubes-r<X>.list
```

e.g. in this example we update `bullseye` stable repository to `bookworm` testing repository

``` shell_session
# sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/qubes-r<X>.list
```

4.  Enable the QubesOS `testing` and `securitytesting` repositories

In `/etc/apt/sources.list.d/qubes-r<X>.list`, enable the `testing` and `securitytesting` repository. We do that to reduce the 'dependency hell' between Qubes repository and Kali repository.

5.  Copy the Kali PGP key from the DisposableVM to the new template:

``` shell_session
$ qvm-copy kali-key.asc
```

The DisposableVM can now be turned off.

6.  Add the Kali PGP key to the list of keys trusted to authenticate packages:

``` shell_session
# cd /home/user/QubesIncoming/dispXXX && gpg --dearmor kali-key.asc
# cp kali-key.asc.gpg /etc/apt/trusted.gpg.d/kali-key.gpg
```

7.  Replace Debian repositories with Kali repository

``` shell_session
# echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list
```

8.  Replace conflicted packages to work around dependency issues

``` shell_session
# apt-get remove <existing_package> && apt-get install <required_package>
```

e.g. in this example we replace `gcc8` with `gcc6`

``` shell_session
# apt-get remove libgcc-8-dev && apt-get install libc6-dev
```

**Note:** This kind of dependency issue will pop up and disappear without notice. Such issues arise because of the differences of dependencies in packages from the Kali repository, the Qubes testing repository and the Debian testing repository. So this step \[step 8\] is currently needed. But it will not always be the case.

9.  Update the template

**Note:** During execution of the update, carefully read list of packages to be removed. If it contains `qubes-vm-dependencies` package, terminate operation and try to resolve missing dependencies first. For other `qubes-*` packages, it is up to you to decide if you need them.

10. Ensure a terminal can be opened in the new template.

``` shell_session
$ qvm-run -a kali-rolling gnome-terminal
```

# Install the Kali tools

At this point you should have a working template and you can install the tools you need. You can find [a list of Kali Linux `Metapackages` here](https://www.kali.org/tools/kali-meta/) Keep in mind that the tools you will install can easily take more than 10 GB, [so you will need to **grow** the size of the VM system storage.](https://www.qubes-os.org/doc/resize-disk-image/)

# Fix Qubes PulseAudio (audio and microphone)

Installing the `kali-defaults` package (which is included in many Kali metapackages including `kali-linux-core`) causes Kali PulseAudio configurations files to be installed that interfere with what Qubes provides. This breaks audio and microphone throughput for that qube.

To fix this, simply do one of the following in the Kali Linux TemplateVM:

## Remove just the conflicting PulseAudio configuration files

1.  Remove the configuration files by running the following command:

``` shell_session
# rm /usr/lib/systemd/user/pulseaudio.service.d/kali_pulseaudio.conf /usr/lib/systemd/user/pulseaudio.socket.d/kali_pulseaudio.socket.conf
```

## Uninstall the entire `kali-defaults` package

1.  Assess the function and contents of the package to see if you need it:
    - See description: `apt show kali-defaults`
    - See installed files: `dpkg -L kali-defaults`
2.  If you determine that the package is unnecessary, then uninstall it
    - `sudo apt remove kali-defaults`

Finally, for both of these options, the Kali Linux qube will have to be restarted for these changes to take effect.

# Alternative Options to Kali Linux

- [PenTester Framework](https://www.trustedsec.com/may-2015/new-tool-the-pentesters-framework-ptf-released/), with [PTF Qubes OS guide](https://www.qubes-os.org/doc/pentesting/ptf/)
- BlackArch Linux, with [BA Qubes OS guide](https://www.qubes-os.org/doc/pentesting/blackarch/)
- more on the [Penetration Testing page](https://www.qubes-os.org/doc/pentesting/)

# Notes

Thanks to the people in [the discussion thread](https://github.com/QubesOS/qubes-issues/issues/1981).

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/pentesting/kali.md)
- First commit: 08 Dec 2020. Last commit: 15 May 2022.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0, 4.1
- Original author(s) (GitHub usernames): wand3rlust, taylorsmcclure, elliotkillick, andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>