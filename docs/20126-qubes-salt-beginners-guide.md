<div data-theme-toc="true"></div>

# Qubes Salt Beginner's Guide

## Part 1: Creating our first qubes

As a beginner, [Salt](https://www.qubes-os.org/doc/salt/) seemed daunting to me at first. It took me some efforts to learn but I love it now! I'm writing this guide for beginners who enjoy an hands-on introduction with examples.

### 1.1 Creating personal state configuration directories

Our journey starts with a file found in the base Salt configuration directory in dom0: `/srv/salt/qubes/README.rst` ([GitHub link](https://github.com/QubesOS/qubes-mgmt-salt-base-config/blob/b3d2837/README.rst)). In this file we can read:

> #### `qubes.user-dirs`
>
> Install and maintain user salt and pillar directories for personal state configurations:
>
> ```txt
> /srv/user_salt
> /srv/user_pillar
> ```
>
> User defined scripts will not be removed on removal of qubes-mgmt-salt by design nor will they be modified on any updates, other than permissions being enforced.

We can activate `qubes.user-dirs` to create personal state configuration directories. What is this, and how do we activate it? This is what we call a *state configuration*. It is a configuration file that tells Salt what to do to reach a particular state.

To activate `qubes.user-dirs`, we can follow the instructions found in its configuration file, `/srv/salt/qubes/user-dirs.sls` ([GitHub link](https://github.com/QubesOS/qubes-mgmt-salt-base-config/blob/b3d2837/qubes/user-dirs.sls)):

> ```txt
> qubes.user-dirs
> ===============
>
> Install and maintain user salt and pillar directories for personal state
> configurations:
>
>   Includes a simple locale state file
>
>   User defined scripts will not be removed on removal of qubes-mgmt-salt
>   by design nor will they be modified on any updates, other than permissions
>   being enforced.
>
> Execute:
> --------
>   qubesctl state.sls qubes.user-dirs
> ```

We run the command `sudo qubesctl state.sls qubes.user-dirs`. Salt applies the corresponding state, and tell us that some files and directories were created. Among these directories we can find `/srv/user_salt/`: this is the main directory where we'll place our state configuration files.

### 1.2 The top file and running highstate

Running the state `qubes.user-dirs` will also create the file `/srv/user_salt/top.sls`. Here is what this file looks like before we modify it ([GitHub link](https://github.com/QubesOS/qubes-mgmt-salt-base-config/blob/b3d2837/qubes/files/top.sls)):


> ```yaml
> # vim: set syntax=yaml ts=2 sw=2 sts=2 et :
> #
> # 1) Intial Setup: sync any modules, etc
> # --> qubesctl saltutil.sync_all
> #
> # 2) Initial Key Import:
> # --> qubesctl state.sls salt.gnupg
> #
> # 3) Highstate will execute all states
> # --> qubesctl state.highstate
> #
> # 4) Highstate test mode only.  Note note all states seem to conform to test
> #    mode and may apply state anyway.  Needs more testing to confirm or not!
> # --> qubesctl state.highstate test=True
> 
> # === User Defined Salt States ================================================
> #user:
> #  '*':
> #    - locale
> ```

This file is called the *top file*.

In the future, when we have many state configuration files, it will become quite tedious to run each state one by one with the command `sudo qubesctl state.sls my-custom-state`. The top file solves that. If we write in this file how to run each state, we get the ability to run all of them with a single command: `sudo qubesctl state.highstate`. We call this "running highstate".

### 1.3 Targeting qubes

There are three lines that are commented out at the end of the top file `/srv/user_salt/top.sls`:

> ```yaml
> user:
>   '*':
>     - locale
> ```

If we were to uncomment those lines and run highstate, Salt would run in *all* targeted qubes (this is what is meant by the `*` character) the state `locale`, for which the state configuration file is either `/srv/user_salt/locale.sls` or `/srv/user_salt/locale/init.sls`.

How do we target a qube? By default, the  commands `qubesctl state.sls my-custom-state` and `qubesctl state.highstate` only target dom0. To make Salt target additional qubes, we can give their names to the `--targets` argument:

* `sudo qubesctl --targets=fedora-38 state.sls my-custom-state` will run `my-custom-state` targeting dom0 and fedora-38.
* `sudo qubesctl --skip-dom0 --targets=debian-12,untrusted state.highstate` will run highstate targeting the qubes debian-12 and untrusted but not dom0.

### 1.4. Creating a qube with Salt

We have a [template](https://www.qubes-os.org/doc/glossary/#template) called fedora-38. We would like Salt to create a purple qube named "salty" based on this template. We write the state configuration file `/srv/user_salt/salty.sls` as follows:

```yaml
salty--create-qube:
  qvm.vm:
    - name: salty
    - present:
      - template: fedora-38
      - label: purple
    - prefs:
      - label: purple
```

That's it! Running `sudo qubesctl state.sls salty saltenv=user` will make Salt create a purple qube named salty. If salty is already present, Salt will just make sure it's purple but won't do anything else.

[details=Note on `saltenv=user`]
Note that we always need to add the extra argument `saltenv=user` to the command  `sudo qubesctl state.sls my-custom-state` when we run individual states from the user directory `/srv/user_salt/`.
[/details]

To make things easier, we would like to automatically run this state when we run highstate. We add the following to the top file `/srv/user_salt/top.sls`:

```yaml
user:
  dom0:
    - salty
```

Great! Now, the command `sudo qubesctl state.highstate` will automatically create salty.

### 1.5 Creating a disconnected qube

We have a template called debian-11. We would like Salt to create a green qube named "disconnected" based on this template, but that has no web browser and no internet access. We write the state configuration file `/srv/user_salt/disconnected.sls` as follows:

```yaml
{% set gui_user = salt['cmd.shell']('groupmems -l -g qubes') %}

disconnected--create-qube:
  qvm.vm:
    - name: disconnected
    - present:
      - template: debian-11
      - label: green
    - prefs:
      - label: green
      - netvm: none
    - features:
      - set:
        - menu-items: org.gnome.Terminal.desktop org.gnome.Nautilus.desktop

disconnected--update-app-menu:
  cmd.run:
    - name: qvm-appmenus --update disconnected
    - runas: {{ gui_user }}
    - require:
      - qvm: disconnected--create-qube
```

Perfect! We can now make Salt create this qube with the command `sudo qubesctl state.sls disconnected saltenv=user`.

[details=Note on the `{}` characters]
Note that by default, `cmd.run` makes Salt run commands as root. The command `qvm-appmenus` does not work as root, so we have to make Salt run this command as a regular user. To do so, in the first line of the file we use a templating language called [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/) to retrieve our username, we save our username in the `gui_user` variable, and we use this variable when needed. Salt will always execute all the templating instructions between `{}` before running a state configuration file.
[/details]

To make things easier, we would like to automatically run this state when we run highstate. We add the following lines to the top file `/srv/user_salt/top.sls`:

```yaml
user:
  dom0:
    - disconnected
```

Great! Now, the command `sudo qubesctl state.highstate` will automatically create our disconnected qube.

[details=Tip: How to make Salt create both "salty" and "disconnected" when we run highstate?]
We can write the top file `/srv/user_salt/top.sls` as follows:

```yaml
user:
  dom0:
    - salty
    - disconnected
```
[/details]

### 1.6 Useful links

I hope this was clear. Here are some links if you'd like to go further:

* [Qubes docs on Salt](https://www.qubes-os.org/doc/salt/)
* [unman's notes](https://github.com/unman/notes/blob/master/salt/Index), my first reference whenever I need help with Salt in Qubes
* [qvm commands](https://github.com/QubesOS/qubes-mgmt-salt-dom0-qvm#readme), list of all qubes-specific salt commands and what they do
* [Salt docs](https://docs.saltproject.io/en/latest/contents.html), great when looking for something specific but intimidating to start with
* [Qubes state configuration files](https://github.com/QubesOS/qubes-mgmt-salt-dom0-virtual-machines/tree/main/qvm) used to create the first qubes when installing Qubes OS

The next part of this guide will be about creating new templates and installing packages in them. See you soon!

## Part 2: Apps and templates

In this part we'll learn how use Salt to make qubes with [new software](https://www.qubes-os.org/doc/how-to-install-software/) (including apps that are not in the official repositories!), and create new templates.

### 2.1 Activating pre-installed apps

We have a [template](https://www.qubes-os.org/doc/glossary/#template) called debian-12. We would like Salt to create a "vault" qube based on debian-12 that is never connected to the internet, and that we will only use for the app KeepassXC.

Luckily, KeepassXC comes pre-installed in the template debian-12, so we can simply tell Salt to make it available in the app menu. We write our state configuration file `/srv/user_salt/vault.sls` as follows:

```yaml
{% set gui_user = salt['cmd.shell']('groupmems -l -g qubes') %}

vault--create-qube:
  qvm.vm:
    - name: vault
    - present:
      - template: debian-12
      - label: black
    - prefs:
      - label: black
      - netvm: none
    - features:
      - set:
        - menu-items: org.keepassxc.KeePassXC.desktop org.gnome.Terminal.desktop

vault--update-app-menu:
  cmd.run:
    - name: qvm-appmenus --update vault
    - runas: {{ gui_user }}
    - require:
      - qvm: vault--create-qube
```

As a result, running `sudo qubesctl state.sls vault saltenv=user` will make Salt create the vault qube if it's not there, and make sure that it has KeePassXC in its app menu.

To make things easier, we would like Salt to automatically take care of the vault when we run highstate. We write the following in the top file `/srv/user_salt/top.sls`:

```yaml
user:
  dom0:
    - vault
```

The command `sudo qubesctl state.highstate` will now automatically run the "vault" state.

### 2.2 Installing new apps

We would like to have a "messaging" qube for communicating with our friends through an app called Telegram. However,  Telegram is not part of the debian-12 template, so we'll have to install it.

Luckily, Telegram is available in the official repository. We can therefore tell Salt to create the "messaging" qube and make sure that Telegram is installed in the debian-12 template by writing the state configuration file `/srv/user_salt/messaging.sls` as follows:

```yaml
{% set gui_user = salt['cmd.shell']('groupmems -l -g qubes') %}

{% if grains['id'] == 'dom0' %}

messaging--create-qube:
  qvm.vm:
    - name: messaging
    - present:
      - template: debian-12
      - label: yellow
    - prefs:
      - label: yellow
    - features:
      - set:
        - menu-items: org.telegram.desktop.desktop org.gnome.Nautilus.desktop

messaging--update-app-menu:
  cmd.run:
    - name: qvm-appmenus --update messaging
    - runas: {{ gui_user }}
    - require:
      - qvm: messaging--create-qube

{% elif grains['id'] == 'debian-12' %}

messaging--install-apps-in-template:
  pkg.installed:
    - pkgs:
      - telegram-desktop

{% endif %}
```

There you go! As we need to run the install process in the debian-12 template, we have to [target](https://forum.qubes-os.org/t/qubes-salt-beginners-guide/20126#h-13-targeting-qubes-5) debian-12 when we make Salt execute this state: `sudo qubesctl --targets=debian-12 --show-output state.sls messaging saltenv=user`. 

[details=Note on the `{% ... %}` syntax]
This state configuration file has two parts. In the first part, we wrote the instructions that Salt has to execute while running in the admin qube dom0, while the second part is about installing Telegram, which must be executed in the template debian-12. To have everything in the same file, but ensure that the right part get executed in the right qube, we decided to use a Jinja ["if statement"](https://jinja.palletsprojects.com/en/3.0.x/templates/#if) to modify the state configuration file depending on in what qube Salt is running the instructions for.
[/details]

Similarly, we can also have Salt apply this state targeting both dom0 and debian-12 when running highstate. We add the following to the top file `/srv/user_salt/top.sls`:

```yaml
user:
  dom0 or debian-12:
    - messaging
```

This makes the command `sudo qubesctl --targets=debian-12 --show-output state.highstate` automatically create a messaging qube with Telegram as part of its app menu.

### 2.3 Creating a "non-free" template

We would like to create a "conferencing" qube with the software Skype to communicate with our family. Skype, however, is not available from the official debian-12 repository because it is distributed under a proprietary software licence: we will have to add an external repository to be able to install it.

As Skype is not from the official repository, we consider that there is a non-zero risk that it compromises the security of the template during its installation process. Because we want to [trust our default templates](https://www.qubes-os.org/doc/templates/#trusting-your-templates), we decide to create a new "nonfree" template to install this proprietary software.

We start by downloading the cryptographic key that signs the Skype repository. From a trusted qube called "disp2956" that is connected to the internet, we run the command:

```sh
curl --output skype.asc https://repo.skype.com/data/SKYPE-GPG-KEY
```

We check the file's contents with the command `cat skype.asc` to make sure that the file is not malicious. Only if we are completely sure that it is not malicious, we can [copy the file to dom0](https://www.qubes-os.org/doc/how-to-copy-from-dom0/#copying-to-dom0) by opening a dom0 terminal and running:

[details=A malicious file or qube could compromise your system through this command!]
```sh
qvm-run --pass-io disp2956 'cat skype.asc' > skype.asc
```
[/details]

We can then convert the file to a GPG keyring format with:

```sh
gpg --dearmor --output skype.gpg skype.asc
```

The keyring is ready to be used by Salt, so we can move it under a new directory at `/srv/user_salt/conferencing/skype.gpg`.

For practical purposes, we will write our state configuration file under the same directory, at `/srv/user_salt/conferencing/init.sls`. The state configuration file reads:

```yaml
{% set gui_user = salt['cmd.shell']('groupmems -l -g qubes') %}

{% if grains['id'] == 'dom0' %}

conferencing--create-nonfree-template:
  qvm.clone:
    - name: nonfree
    - source: debian-12

conferencing--create-app-qube:
  qvm.vm:
    - name: conferencing
    - present:
      - template: nonfree
      - label: yellow
    - prefs:
      - label: yellow
    - features:
      - set:
        - menu-items: skypeforlinux.desktop org.gnome.Nautilus.desktop
    - require:
      - qvm: conferencing--create-nonfree-template

conferencing--update-app-menu:
  cmd.run:
    - name: qvm-appmenus --update conferencing
    - runas: {{ gui_user }}
    - require:
      - qvm: conferencing--create-app-qube

{% elif grains['id'] == 'nonfree' %}

conferencing--add-repository:
  pkgrepo.managed:
    - name: deb [signed-by=/etc/apt/keyrings/skype.gpg] https://repo.skype.com/deb stable main
    - file: /etc/apt/sources.list.d/skype-stable.list
    - key_url: salt://conferencing/skype.gpg
    - aptkey: False
    - require_in:
      - pkg: conferencing--install-apps

conferencing--install-apps:
  pkg.installed:
    - pkgs:
      - skypeforlinux

{% endif %}
```

Running this state makes Salt create a "conferencing" app qube based on a new template called "nonfree", in which Salt makes sure that Skype is installed through the external repository. To run this state, we target our new "nonfree" template with the command:

```sh
sudo qubesctl --targets=nonfree --show-output state.sls messaging saltenv=user
```

Let's add this state to the top file, so that it is applied automatically when we run highstate! At the end of the top file `/srv/user_salt/top.sls`, we write:

```yaml
user:
  dom0 or nonfree:
    - conferencing
```

We can now run highstate with the command:

```sh
sudo qubesctl --targets=nonfree --show-output state.highstate
```

[details=Tip: Here is what our top file would look like if we would include all the states from this guide so far.]
```yaml
user:
  dom0:
    - salty
    - disconnected
    - vault
  dom0 or debian-12:
    - messaging
  dom0 or nonfree:
    - conferencing
```

With this top file, we would run highstate with:

```sh
sudo qubesctl --targets=debian-12,nonfree --show-output state.highstate
```
[/details]

### 2.4 Useful links

I tried to be as concise as I could. Please let me know if you have any further questions! Here are some related links.

* [Qubes docs on installing software](https://www.qubes-os.org/doc/how-to-install-software/)
* [Qubes docs on trusting your templates](https://www.qubes-os.org/doc/templates/#trusting-your-templates)
* [Basic Salt syntax](https://docs.saltproject.io/salt/user-guide/en/latest/topics/requisites.html), an extremely useful primer from the official Salt documentation
* [extrepo-data](https://salsa.debian.org/extrepo-team/extrepo-data), a list of external repositories for many apps that are not in the official repositories

In the next part of this guide, we will learn how to make Salt perform automated backups of our qubes with [Wyng](https://github.com/tasket/wyng-backup)!