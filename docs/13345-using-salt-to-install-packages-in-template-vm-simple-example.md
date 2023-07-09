**Backstory**

I've been wanting to use Salt Stack for a long time to provision new Qubes templates but never seemed to get around to it. Perhaps because the official Salt docs are not great or perhaps because I got sidetracked into bigger Qubes + Salt possibilities.

Today I decided to just buckle down and focus on a narrow, simple task: Use Salt to install packages into a new template VM (already existing on my machine). I usually do this manually, using a text file I maintain with instructions and lists of packages, typing and pasting things into the terminal.

Being focused helped me cut through all the complexity of Salt and finally get something done.

**I'm a beginner**

These are literally my first Salt files, **I am open to feedback**. Hopefully this helps other newbs. That said these are tested and do work for me.

**Howto**

Let's assume you have a list of packages to install in one or more template VMs. Let's assume for purposes of this guide that you call the list **fedora-general**. This is a conceptual name and is not used to select templates so it can be anything. Just know that anywhere you see "fedora-general" here, replace with your own name if different. (I chose this name because I always have a fedora template ending "-general" - "fedora-33-general", "fedora-34-general" and so forth. In these I install broadly useful packages.)

*1. State file*

Make a salt state file in dom0 at `/srv/salt/fedora-general.sls` that looks like this (replace the packages with your own choices, obviously):

```
#salt state file

fedora-general-enable-repos: #state-id
  cmd.run: #execution module
    - name: sudo dnf config-manager --set-enabled rpmfusion-free rpmfusion-free-updates rpmfusion-nonfree rpmfusion-nonfree-updates && sudo dnf upgrade -y --refresh #parameter

#you can have multiple states in a file. I think (?) they are applied
#in the order they appear in file.

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
      - brasero-nautilus
      - xsel
      - zbar
      - evolution
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
```

A Salt State file describes a state you want the machine/VM to reach and is composed of a series of sections like the above:

```
stateid:
  execution-module:
    - param
    - param
```

Docs for some of the more interesting execution modules are [linked here under "further reading" at the bottom](https://www.qubes-os.org/doc/salt/#further-reading).

*2. Top file* 

Make a salt top file in dom0 at `/srv/salt/fedora-general.top` that looks like this, replacing "fedora-36-general" with the name of the VM you wish to install packages into:


```
#top file

base: #environment (always "base"?)
  fedora-36-general: #vm selector (regexes are possible too) (called "target" in salt)
   - fedora-general #sls file reference, omitting ".sls"
```

If you want to install into multiple VMs, instead of specifying "fedora-36-general" or whatever you can use  a regex syntax, described [in the "top files" section here](https://www.qubes-os.org/doc/salt/#top-files).

The top file maps state files to machines, basically.

*3. Enable top file*

In dom0, run

```
sudo qubesctl top.enable fedora-general
```

(The last argument is the name of your top file minus ".top")

*4. Execute state change*

Let's assume you want to run this state change on a template VM called `fedora-36-general`, you next should run:

```
sudo qubesctl --targets=fedora-36-general state.highstate
```
(You can add additional template vms using commas in `--targets=`. There are further options, like "all", in the help for `qubesctl`. Just make sure these template vms are also selected in  your top file above.)

If this works, various VMs will spin up and there will be a delay while everything installs. If there is a failure or an abrupt ending (even if it says "OK"), check the log:

```
sudo tail -n 100 /var/log/qubes/mgmt-fedora-36-general.log
```
(replacing "fedora-36-general" with the name of your template vm)

If you get something like `State 'foo' in SLS 'bar' is not formed as a list`, it means either your YAML is invalid OR that the YAML is valid but does not constitute valid syntax for an SLS file. In my case it gave me this error when I forgot the dash and space before `pkgs:` in my SLS above.

**Further reading**

The [Qubes docs on Salt](https://www.qubes-os.org/doc/salt/) are my favorite Salt docs. A nice concise explanation of Salt (better than on the official tutorial) and then a nice explanation of Qubes integration. The Salt [docs on package state](https://docs.saltproject.io/en/latest/ref/states/all/salt.states.pkg.html) are linked from the previous and are perhaps useful for customizing the above. The [further reading section](https://www.qubes-os.org/doc/salt/#further-reading) of the Qubes docs on salt, at the bottom, is also useful. 

**Annoyances**

Why is the big main command called `state.highstate`? I have no idea. In addition to being redundant (two uses of "state", why not `state.high`?), it's also unclear what "high" means. Are there "low" states? Medium? Why not, like, `state.apply`? (I know this forum is not the place to complain about this stuff except I think other newbs might feel some comfort at knowing they are not the only ones who wonder what the heck is up with this weird phrasing.) 

Also, right now the top file concept feels a little like boilerplate to me. Couldn't I just invoke the states through a command line composition that specifies machines? Anyway, I'm new, maybe it will all make sense in time as I learn more.