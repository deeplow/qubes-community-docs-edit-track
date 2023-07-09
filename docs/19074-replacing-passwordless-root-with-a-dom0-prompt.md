For context, please see [passwordless root](https://www.qubes-os.org/doc/passwordless-root/).

Some Qubes users may wish to enable user/root isolation in VMs. This is not officially supported, but of course nothing is preventing the user from modifying his or her own system. A list of steps to do so is provided here **without any guarantee of safety, accuracy, or completeness. Proceed at your own risk. Do not rely on this for extra security.**

1.  Adding Dom0 "VMAuth" service:

    ```
    [root@dom0 /]# echo "/usr/bin/echo 1" >/etc/qubes-rpc/qubes.VMAuth
    [root@dom0 /]# echo "@anyvm dom0 ask,default_target=dom0" \
    >/etc/qubes-rpc/policy/qubes.VMAuth
    [root@dom0 /]# chmod +x /etc/qubes-rpc/qubes.VMAuth
    ```

    (Note: any VMs you would like still to have passwordless root access (e.g. Templates) can be specified in the second file with "\<vmname> dom0 allow")

2.  Configuring Fedora template to prompt Dom0 for any authorization request:

    - In `/etc/pam.d/system-auth`, replace all lines beginning with "auth" with these lines:

      ```
      auth  [success=1 default=ignore]  pam_exec.so seteuid /usr/lib/qubes/qrexec-client-vm dom0 qubes.VMAuth /bin/grep -q ^1$
      auth  requisite  pam_deny.so
      auth  required   pam_permit.so
      ```

    - Require authentication for sudo. Replace the first line of `/etc/sudoers.d/qubes` with:

      ```
      user ALL=(ALL) ALL
      ```

    - Disable PolKit's default-allow behavior:

      ```
      [root@fedora-20-x64]# rm /etc/polkit-1/rules.d/00-qubes-allow-all.rules
      [root@fedora-20-x64]# rm /etc/polkit-1/localauthority/50-local.d/qubes-allow-all.pkla
      ```

3.  Configuring Debian/Whonix template to prompt Dom0 for any authorization request:

    - In `/etc/pam.d/common-auth`, replace all lines beginning with "auth" with these lines:

      ```
      auth  [success=1 default=ignore]  pam_exec.so seteuid /usr/lib/qubes/qrexec-client-vm dom0 qubes.VMAuth /bin/grep -q ^1$
      auth  requisite  pam_deny.so
      auth  required   pam_permit.so
      ```

    - Require authentication for sudo. Replace the first line of `/etc/sudoers.d/qubes` with:

      ```
      user ALL=(ALL) ALL
      ```

    - Disable PolKit's default-allow behavior:

      ```
      [root@debian-8]# rm /etc/polkit-1/rules.d/00-qubes-allow-all.rules
      [root@debian-8]# rm /etc/polkit-1/localauthority/50-local.d/qubes-allow-all.pkla
      ```

    - In `/etc/pam.d/su.qubes`, comment out this line near the bottom of the file:

      ```
      auth sufficient pam_permit.so
      ```

    - For Whonix, if a prompts appear during boot, this is [unsupported](https://forums.whonix.org/t/passwordless-root-prompt-at-boot/16370) by Whonix because this feature is not yet supported by Qubes either.

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/security/replacing-passwordless-root-with-dom0-prompt.md)
- First commit: 15 Feb 2023. Last commit: 17 Feb 2023.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.1
- Original author(s) (GitHub usernames): adrelanos, andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
[/details]

<div data-theme-toc="true"> </div>