For compartmentalization and security I normally multiply my Fedora TemplateVM into multiple specialized clones like so:

```
fedora-37 (untouched)
     |
    fedora-37-general (adds broadly useful, widely-used open source packages)
        |
       fedora-37-print (sketchy printer drivers)
        |
       fedora-37-talk (Zoom, Slack packages)
        |
       fedora-37-media (Commercial Russian video ripping software etc) 
``` 
It is painful to manage these by hand since Fedora releases frequently. I have been using a text file with instructions to myself for configuring each clone of fedora.

This year I finally figured out how to use Salt for this purpose. Here is how I do it, in case anyone is looking for example files as a starting place to learn how to manage Qubes with salt. I am still a beginner myself. Feedback / ideas welcome.

If you need an even more basic example, see [the one I posted last year](https://forum.qubes-os.org/t/using-salt-to-install-packages-in-template-vm-simple-example/13345), which introduces super rudimentary Salt concepts in relation to Qubes.

All files below live in `dom0`.

## Top-level shell commands

This is the top-level shell script that runs all the salt sls files. Obviously you can extract the individual commands after `else` if you want to develop your own custom solution iteratively. I call this file with one argument, the number of the fedora version I am customizing, e.g. `fedora-multiply.sh 37`.

**`/home/user/bin/fedora-multiply.sh`:**

```
#!/usr/bin/bash

set -e #quit on error

if [ -z "$1" ]
then
    echo "USAGE: fedora-multiply FVERSION"
else
    sudo qubesctl state.apply fedora-clone-to-general pillar="{\"fedorav\": \"$1\"}"
    sudo qubesctl --skip-dom0 --targets=fedora-$1-general state.apply fedora-general-configure
    sudo qubesctl state.apply fedora-general-multiply pillar="{\"fedorav\": \"$1\"}"
    sudo qubesctl --skip-dom0 --targets=fedora-$1-media state.apply fedora-media-configure
fi
```
Each command specifies an SLS file to apply after `state.apply` minus the `.sls` extension. So `state.apply fedora-clone-to-general` applies the file at `/srv/salt/fedora-clone-to-general.sls`.

You will notice some commands have `--skip-dom0 --targets=fedora-...`. These are dispatched from dom0 to run their SLS files on the VMs listed under `--targets=`. The commands that do not use these flags run their SLS files only on `dom0`. 

Also, some commands have a pillar passed in as a JSON object with the key "fedorav". This is the fedora version and is used to render jinja templates in the SLS files that name and identify the templateVMs.

Below are the SLS files.

## Clone fedora to fedora-general
This one clones `fedora-XX` to `fedora-XX-general`  and copies the open source IBM Plex font out of `dom0` into the `fedora-XX-general` template as well, since I like that font :-)

Note the first use of jinja templates, using the key/value ("fedorav": "37") we passed in on the command line (in `/home/user/bin/fedora-multiply.sh`) as a JSON object.

**`/srv/salt/fedora-clone-to-general.sls`**

```
fedora-clone-to-general:
  qvm.clone:
    - source: fedora-{{ pillar['fedorav'] }}
    - name: fedora-{{ pillar['fedorav'] }}-general

plex-to-fedora-general:
  cmd.run:
    - name: qvm-copy-to-vm fedora-{{ pillar['fedorav'] }}-general /home/user/Plex
```

## Configure fedora-general
Configuring `fedora-XX-general`:

**`/srv/salt/fedora-general-configure.sls`**

```
fedora-general-enable-repos: 
  cmd.run: 
    - name: sudo dnf config-manager --set-enabled rpmfusion-free rpmfusion-free-updates rpmfusion-nonfree rpmfusion-nonfree-updates && sudo dnf upgrade -y --refresh #parameter

fedora-general-installs:
  pkg.installed:
    - pkgs:
      - libreoffice
      - keepassxc
      - emacs 
      - libgnome-keyring
      - inotify-tools
      - seahorse
      - seahorse-nautilus
      - brasero
      - xsel
      - zbar
      - evolution
      - aspell
      - aspell-en
      - ruby
      - pavucontrol
      - bind-utils
      - cloc
      - onionshare
      - gimp
      - traceroute
      - whois
      - xclip
      - geteltorito
      - genisoimage
      - java-17-openjdk
      - postgresql
      - python3-psycopg2
      - postgresql-server
      - postgresql-upgrade
      - gpgme
      - dnf-utils
      - python3-gpg
      - youtube-dl
      - transmission
      - zstd
      - libzstd
      - ffmpeg-libs
      - ffmpeg
      - vlc

install-plex:
  cmd.run:
    - name: sudo mv /home/user/QubesIncoming/dom0/Plex/IBM* /usr/share/fonts && sudo fc-cache -f -v
```

## Clone fedora-general into specialized templates
Cloning `fedora-XX-general` into specialized templates like `fedora-XX-print`, `fedora-XX-media`, etc. Notice this first shuts down `fedora-XX-general` so that its new configuration is saved before it is cloned:

**`/srv/salt/fedora-general-multiply.sls`**

```
fedora-general-shutdown:
  qvm.shutdown:
    - name: fedora-{{ pillar['fedorav'] }}-general

fedora-general-clone-to-talk:
  qvm.clone:
    - source: fedora-{{ pillar['fedorav'] }}-general
    - name: fedora-{{ pillar['fedorav'] }}-talk

fedora-general-clone-to-media:
  qvm.clone:
    - source: fedora-{{ pillar['fedorav'] }}-general
    - name: fedora-{{ pillar['fedorav'] }}-media

fedora-general-clone-to-print:
  qvm.clone:
    - source: fedora-{{ pillar['fedorav'] }}-general
    - name: fedora-{{ pillar['fedorav'] }}-print

```

## Configure a specialized template

I automate the setup of `fedora-XX-media` since it has many additional packages. This uses some more advanced/esoteric packaging options (much of which is to provide prerequisites for specialized media software I need to compile by hand).

**`/srv/salt/fedora-media-configure.sls`**

```
development-tools:
  pkg.group_installed:
    - name:  development-tools

ctools:
  pkg.group_installed:
    - name: 'C Development Tools and Libraries'

installs:         
  pkg.installed:
    - pkgs:
        - gst-devtools
        - HandBrake
        - HandBrake-gui
        - asunder
        - fdkaac
        - zlib-devel
        - openssl-devel
        - expat-devel
        - ffmpeg
        - ffmpeg-devel
        - qt5-qtbase-devel
        - pkgconf-pkg-config
        - glibc-devel
        - mesa-libGLU-devel
        - mesa-libGL-devel

```

## What I do manually

You will notice there is no Salt configuration for `fedora-XX-print` or `fedora-XX-talk`. That's because it's easier to install the very few additional packages in these templates by hand. They all need to be downloaded manually from various websites. The print driver even needs to be run via an interactive script that asks various configuration questions.

## Gotchas

The Qubes-Salt [page on qubes-os.org lists](https://www.qubes-os.org/doc/salt/#all-qubes-specific-states) what it erroneously calls "All Qubes-specific states"; there is a presumably newer and definitely longer list of Qubes states [on github](https://github.com/QubesOS/qubes-mgmt-salt-dom0-qvm#available-state-commands).

As has been previously noted in this forum, the `qubesctl` command will *always* target `dom0`, even if you provide an explicit list of `--targets=...` that does not include `dom0`. To exclude `dom0` as a target always pass the `--skip-dom0` flag as I do above.

In my last example [tutorial](https://forum.qubes-os.org/t/using-salt-to-install-packages-in-template-vm-simple-example/13345) I used top files alongside SLS files. The purpose of top files is to map SLS files to particular machines. I find it easier to simply do these mappings by customizing my call to `qubesctl` with an explicit `--targets=...` command (with `--skip-dom0` if needed) and then calling a particular SLS file via `state.apply`. I believe @unman suggested this approach in his reply to my last example tutorial. If you do try and use top files, be aware that each target in the top file can target one or more VMs but *will still be run on dom0* regardless of whether this matches the target specification. You need to pass `--skip-dom0` to thwart this behavior.