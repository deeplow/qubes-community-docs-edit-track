*This summary is based on (and quotes) the Qubes Community [guide](https://github.com/Qubes-Community/Contents/blob/master/docs/customization/dark-theme.md), [this](https://forum.qubes-os.org/t/dark-mode-in-debian-10-vm/3855) and [that](https://forum.qubes-os.org/t/4-1-dark-mode-issue-solved/10472) — especially @Sven’s extensive work, see also this [thread](https://forum.qubes-os.org/t/dark-theme-for-qubes-manager-not-working-in-4-1/4917).*

# Dom0, Fedora & Debian

* * *

The following text and screenshots describe how to change the default light theme to a global dark theme. It's just an example; feel free to adjust the appearance to your taste.

And here are the final results:

![xfce-end-result|690x388, 75%](upload://2Ag5VdgyYcXmY39peLsQvTXYy22.png)


*Dom0 Qube Manager, Dom0 Terminal, Fedora 35 VMs, Debian 11 VM; desktop background color #3B3941 (external full HD display)*
<br>
![qubes-applications-menu|468x500, 75%](upload://pmFLZJo7sWvoQKrBMUhEhLcLggf.png)


*Qubes Applications Menu is darkened as well*
<br>
**Note:** Of course, several apps (e.g., Terminal and Gedit) can be styled in the app itself. Here, Dom0 Terminal’s background color is set to the desktop background color — because fusion. 😉

## Dom0

* * *

**Change Appearance**

- Open the `Appearance` window:
    
- Qubes Applications Menu --> `System Tools` --\> `Appearance`
 <br>
![dom0-appearance|355x500, 75%](upload://4nq4gvF1zi5r9x9BccijEznKjyy.png)
<br>
- Select `Style` --\> `Adwaita-dark`. It’s probably the most ›classic‹ and readable/contrasty of the dark styles here. But, of course, feel free …
    
- Adjust `Icons`, `Fonts` and `Settings` to your taste. In all these examples here, icons are always set to `Gnome` and fonts to `DejaVu Sans` family.
<br>

**Change Style in Window Manager**

- Open the `Window Manager` dialog:
    
	Qubes Applications Menu --> `System Tools` --> `Window Manager` --> `Style`
<br>
![dom0-window-manager|554x499, 75%](upload://odT1B1FRURGWHNQYe8jnEgvnBoC.png)
<br>
- Change `Theme` in `Style` tab to `G2`, `Wallis`, or `Bluebird`. These are probably the most ›classic‹ and readable/contrasty. `Bluebird`'s borders appear more elegant, but it could be difficult to grab the window’s edges in order to resize. But feel free …
<br>

**Qubes tools**
    
Most of the Qubes OS UI in dom0 is now Qt5 based and doesn’t adhere to the selected theme by default.

more info: https://wiki.archlinux.org/title/Uniform_look_for_Qt_and_GTK_applications

This can be remedied by:
  - using a native Qt style
```
sudo qubes-dom0-update adwaita-qt5
```
Then add `QT_STYLE_OVERRIDE=adwaita-dark` to `/etc/environment`.
Reboot.

  - using a theme engines
```
sudo qubes-dom0-update qt5-qtstyleplugins
```
Then add `QT_QPA_PLATFORMTHEME=gtk2` to `/etc/environment`.
Reboot.

  - add a menu option to qube manager

That avoid to install anything in dom0,
but it **require** to review the few lines of code being added.
[qube-manager dark mode (built-in method)](https://forum.qubes-os.org/t/qube-manager-dark-mode-built-in-method/15241)
<br>
## Fedora 34 / 35

* * *

**Install and use Gnome Tweaks**

In templateVM:

```
sudo dnf install gnome-tweaks
```

**Note:** See [How to update](https://www.qubes-os.org/doc/how-to-update/#command-line-interface).

- Shutdown templateVM and add `Tweaks` to `App shortcuts` of appVM in Qube Manager.
    
- Start `Tweaks` in appVM.
    
- Select `Appearance` --\> `Themes` --\> `Applications` --\> `Adwaita-dark` (adjust also all the other options to your taste):
<br>
![fedora-gnome-tweaks|690x411, 75%](upload://u7NcAlPNSsuhF7ZCylKHBQOwxmq.png)
<br>

**Notes:** You have to do this in the templateVM *and* all appVMs; changes you make in the home directory of a templateVM will not reflect in the template based VM by design. For dispVMs see [this](https://forum.qubes-os.org/t/dark-mode-in-debian-10-vm/3855/4).

If you want to use `gnome-settings-daemon` *and* Gnome Tweaks, it’s probably best to delete `settings.ini` and `.gtkrc-2.0` (see following Debian section).

To make sure QT apps look good, too: In templateVM install `qt5-qtstyleplugins`, `gtk-murrine-engine` and `gnome-themes-standard`. Add `QT_QPA_PLATFORMTHEME=gtk2` to `/etc/environment`.
<br>

## Debian 10 / 11

---

In Debian, things are getting a little bit trickier …

AppVMs seem to work best without `gnome-settings-daemon` (see end of Fedora section above). In that case set DPI in `/etc/X11/Xresources/x11-common` using `Xft.dpi:` (probably `96`) in template VM.

Make sure your appVMs have both `~/.config/gtk-3.0/settings.ini` and `~/.gtkrc-2.0`:

**settings.ini**

```
[Settings]
gtk-application-prefer-dark-theme=1
gtk-font-name=DejaVu Sans Book 12 
gtk-theme-name=Adwaita-dark
gtk-icon-theme-name=gnome
```
`gtk-application-prefer-dark-theme=1` is not necessary, it's forces usage of dark variation of selected theme. Since we are choosing theme that is already Dark it can be omitted.  

**.gtkrc-2.0**

```
include "/usr/share/themes/Adwaita-dark/gtk-2.0/gtkrc" 
style "user-font" 
{ 
		font_name="DejaVu Sans Book" 
}
widget_class "*" style "user-font"
gtk-font-name="DejaVu Sans Book 12" 
gtk-theme-name="Adwaita-dark"
gtk-icon-theme-name="gnome"
```
**Note:** The icon theme name is the name of its directory, *not* the name property in its `index.theme` . 
According to: [https://wiki.archlinux.org/title/GTK](https://wiki.archlinux.org/title/GTK)

Put these files to `/etc/skel` of the templateVM, so they get created automatically if you set up a new appVM based on that templateVM.

To make sure QT apps look good, too: In templateVM install `qt5-style-plugins, gtk2-engines-murrine`, and `gnome-themes-standard`. Then add these two lines to `/etc/environment`:

```
QT_QPA_PLATFORMTHEME=gtk2
QT_SCALE_FACTOR=1
```

This work for debian-11-minimal but for debian-11 You have to uninstall `xsettingsd` or edit `~/xsettingsd`  config file instead of using `~/.config/gtk-3.0/settings.ini` and `~/.gtkrc-2.0`.

**Done!**
<br>

---


**To do?** Darken Firefox websites and Thunderbird emails just with `userChrome.css` and `userContent.css`, *not* via extensions/add-ons.

**Note:** Some panel (applet) icons, e.g., NetworkManager — see ›global‹ screenshot at the beginning of this guide —, `notification-daemon`, Joplin and Keybase, remain with white instead of dark resp. transparent backgrounds. For NetworkManager icon, see [Qubes issue #2846](https://github.com/QubesOS/qubes-issues/issues/2846).

<div data-theme-toc="true"> </div>