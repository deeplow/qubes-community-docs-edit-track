Fedora-based templates out of the box cannot play some common video formats such as mp4. This tutorial installs the VLC Media Player in Fedora. *Installing VLC in debian-based qubes is also an alternative (and may be easier).*

**note:** this post has been edited by @deeplow for clarity
<div data-theme-toc="true"> </div>

---

> **note:** If you're unfamiliar with how to install software on qubes, please first read ["Installing software in TemplateVMs"](https://qubes-os.org/doc/software-update-domu/#installing-software-in-templatevms).

> :warning: This guide enables third party repositories (RPM Fusion) to your Fedora installation. Read more on some of the implications [here](https://docs.fedoraproject.org/en-US/quick-docs/setup_rpmfusion/).

## 1. (option a) Installing VLC in Fedora

This guide was tested in QubesOS `v4.0.3` with the `fedora-30` template. If it worked for you in newer versions, please mention that bellow so.

```shell_session
dnf --enablerepo=rpmfusion-free --enablerepo=rpmfusion-free-updates --enablerepo=rpmfusion-nonfree --enablerepo=rpmfusion-nonfree-updates install vlc
```
VLC should now be installed successfully in the TemplateVM.

## 1. (option b) Installing other media players

just repeat the above command but replacing `vlc` at the end by the packages `ffmpeg mpv`

You should now be able to start the MPV player.

## 2. Shut down TemplateVM and associated VMs

Then shut down the TemplateVM  and any AppVMs [based on that TemplateVM](https://qubes-os.org/doc/glossary/#templatebasedvm) for changes to take effect.

## 3. See if it worked

The you start the Fedora [AppVM](https://qubes-os.org/doc/glossary/#appvm) and you should be able to play video files (they'll open in VLC). If it didn't work, comment down bellow.

### (optional) add a VLC or MPV to your list of applications
Optionally you can also add VLC Media Player [to your list of applications](http://qubes-os.org/doc/managing-appvm-shortcuts/).

-----------------------------------------------------

## Troubleshooting

### No package vlc available.  Error: Unable to find a match.

If you get the error `No package vlc available.  Error: Unable to find a match.` while running `dnf install vlc`, then you should do:

```bash
sudo gedit /etc/yum.repos.d/rpmfusion-free.repo # or any other text editor
```

The line which will need editing will be near the beginning probably 7 lines down:

```
enabled=0
```

Change the `0` to a `1` and then save and exit.

Now re-enter the following lines in the terminal.
```shell_session
sudo dnf -y update
sudo dnf install vlc
```

And then go to [the next step](#shut-down-templatevm-and-associated-vms).