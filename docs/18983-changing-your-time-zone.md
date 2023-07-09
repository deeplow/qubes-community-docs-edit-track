# Command line

If you use the i3 window manager or would prefer to change the system's time zone in terminal you can issue the `timedatectl` command with the option `set-timezone`.

For example, to set the system's time zone to Berlin, Germany type in a dom0 terminal:

```
$ sudo timedatectl set-timezone 'Europe/Berlin'
```

You can list the available time zones with the option `list-timezones` and show the current settings of the system clock and time zone with option `status`.

Example output status of `timedatectl` on a system with time zone set to Europe/Berlin:

```
[user@dom0 ~]$ timedatectl status
      Local time: Sun 2018-10-14 06:20:00 CEST
  Universal time: Sun 2018-10-14 04:20:00 UTC
        RTC time: Sun 2018-10-14 04:20:00
       Time zone: Europe/Berlin (CEST, +0200)
 Network time on: no
NTP synchronized: no
 RTC in local TZ: no
```

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/configuration/change-time-zone.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>