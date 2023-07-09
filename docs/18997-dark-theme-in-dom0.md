# Dark KDE in Dom0

The following text describes how to change the default light theme to a dark theme. This is just an example, feel free to adjust the appearance to your taste.

The image below shows the default light theme after installation. ![begin light theme](upload://rebzhL3YuwbqGvxYps99o1HPUuy.png)

This is the result after applying the steps described here. ![end result dark theme](upload://bR1sFce7Nm8XW0NExG0c8UkBA3K.png)

1.  Change `Workspace Appearance`

    1.  Open the `Workspace Appearance` window

        ```
         Qubes Menu -> System Tools -> System Settings -> Workspace Appearance
        ```

        ![Workspace Appearance](upload://a4IBnbigoiWBxpdpsUxRfCFit6v.png)

    2.  Go to `Desktop Theme`

        ![Desktop Menu](upload://2etZCztFTZ1Ajkvl8BQcTKRMBhW.png)

    3.  Select `Oxygen` and `Apply` the change

2.  (Optional) Remove blue glowing task items

    ![blue glowing task bar items](upload://4VYpBeL7gMmE1gHpSr43DNgNPQp.png)

    1.  Adjust Oxygen `Details`

        ```
         Qubes Menu -> System Tools -> System Settings -> Workspace Appearance -> Desktop Theme -> Details (Tab)
        ```

    2.  Select `Oxygen`

    3.  Change `Theme Item -> Task Items` from `Oxygen Task Items` to `Air Task Items`

        ![Change Task items look](upload://qRcn8gYbsgdCOw2T4XxuuxW9ZWh.png)

    4.  Apply changes

        ![task bar items blue glowing removed](upload://3HRAh2JJGfbF46qiq8NQetvcAOn.png)

3.  Change `Application Appearance`

    1.  Open the `Application Appearance` window

        ```
         Qubes Menu -> System Tools -> System Settings -> Application Appearance
        ```

    2.  Go to `Colors`

        ![colors tab](upload://4cu6to1kHaAoO4t4HB6Lgdtuehx.png)

    3.  Select `Obsidian Coast`

        ![set to Obsidian Coast](upload://wIt2Vg14QQYgLkmJciUOUaFSMwR.png)

    4.  Apply Changes

        ```
         Qubes VM Manager should now look like the image below.
        ```

        ![result black Qubes Manager](upload://oMOHgMxTlO2fFreQdNbNmX9a4fS.png)

**Note:** Changing the `Window Decorations` from `Plastik for Qubes` will remove the border color and the VM name. The problem with `Plastik for Qubes` is that it does not overwrite the background and text color for Minimize, Maximize and Close buttons. The three buttons are therefore hard to read.

# Dark XCFE in Dom0

The following text describes how to change the default light theme to a dark theme. This is just an example, feel free to adjust the appearance to your taste.

The image below shows the default light theme after installation. ![begin light theme](upload://fWJMiewhpPh4cA7AYbSZhsVOfbx.png)

This is the result after applying the steps described here. ![end result dark theme](upload://jgTgCfnPuPjsRbSsYl5702eSyFC.png)

1.  Change Appearance

    1.  Open the `Appearance` dialog

        ```
         Qubes Menu -> System Tools -> Appearance
        ```

        ![appearance dialog](upload://fpbvuyS0qJ1EQUBmWW58E5405h5.png)

    2.  Change Style to `Albatross`

    **Note:** The black appearance theme `Xfce-dusk` makes the VM names in the `Qubes OS Manager` unreadable.

2.  *(Optional)* Change Window Manager Style

    1.  Open the `Window Manager` dialog

        ```
         Qubes Menu -> System Tools -> Appearance
        ```

        ![window manager dialog](upload://4Jd4KqHCA4iUXFv5Qb4ghr4x2co.png)

    2.  Change the Theme in the `Style` Tab (e. g. Defcon-IV). All available themes work.

# Dark App VM, Template VM, Standalone VM, HVM (Linux Gnome)

Almost all Qubes VMs use default applications based on the GTK toolkit. Therefore the description below is focused on tools from the Gnome Desktop Environment.

# Using "Gnome-Tweak-Tool"

The advantage of creating a dark themed Template VM is, that each AppVM which is derived from the Template VM will be dark themed by default.

**Note:** Gnome-Tweak-Tool crashes under Archlinux. A workaround is to assign the AppVM to another TemplateVM (Debian, Fedora) which has Gnome-Tweak-Tool installed. Start the AppVM and configure the settings. Shutdown the machine and switch the TemplateVM back to Archlinux.

1.  Start VM

    **Note:** Remember that if you want to make the change persistent, the change needs to be made in the TemplateVM, not the AppVM.

2.  Install `Gnome-Tweak-Tool`

    - Fedora

      ```
        sudo dnf install gnome-tweak-tool
      ```

    - Debian

      ```
        sudo apt-get install gnome-tweak-tool
      ```

3.  *(Only AppVM)* Stop TemplateVM and start AppVM

4.  Add `Gnome-Tweak-Tool` to the Application Menu

    1.  `Right-click` on VM entry in `Qubes VM Manager` select `Add/remove app shortcuts`

    2.  Select `Tweak Tool` and press the `>` button to add it

        ![Application Dialog](upload://ivqkXBddHsJBrFkBWGq74qCuZHw.png)

5.  Enable `Global Dark Theme`

    1.  *Debian only*

        ```
         cd ~/.config/
         mkdir gtk-3.0
         cd gtk-3.0/
         touch settings.ini
        ```

    2.  Start `Tweak Tool` from the VM application menu and set the `Global Dark Theme` switch to `on`

        ![Global Dark Theme enabled](upload://lbLM2ylNwnktiom0LNut7ZyX3NM.png)

6.  *(Optional)* Modify Firefox

    **Note:** Firefox uses GTK style settings by default. This can create side effects such as unusable forms or search fields. One way to avoid this is to add the following line to `/rw/config/rc.local`:

    ```
         sed -i.bak "s/Exec=firefox %u/Exec=bash -c 'GTK_THEME=Adwaita:light firefox %u'/g" /usr/share/applications/firefox.desktop
    ```

7.  Restart VM or all applications

# Manually

Manually works for Debian, Fedora and Archlinux.

1.  Start VM

    **Note:** Remember that if you want to make the change persistent, the change needs to be made in the TemplateVM, not the AppVM.

2.  Enable `Global Dark Theme`

    ```
     cd ~/.config/
     mkdir gtk-3.0
     cd gtk-3.0/
     touch settings.ini
    ```

    Add the following lines to `settings.ini`

    ```
     [Settings]
     gtk-application-prefer-dark-theme=1
    ```

3.  Follow steps 6 and 7 in: Using `Gnome-Tweak-Tool`

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/customization/dark-theme.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>