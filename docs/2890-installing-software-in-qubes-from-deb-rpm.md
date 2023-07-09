Continuing the discussion from [How do I create a standalone VM?](https://forum.qubes-os.org/t/how-do-i-create-a-standalone-vm/2884):

> **Please note:** This is not the standard method of installing software in Qubes. Only use this when [you've exhausted all other options](https://www.qubes-os.org/doc/software-update-domu/#installing-software-in-templatevms), if at all.

## :warning: Security disclaimers
In this guide multiple sacrifices are made for convenience. Make sure you understand their implications and proceed only if these are acceptable for your particular situation. These include:
  * **Not verifying software signatures** (due to their unavailability)
    *When you install software [in the regular way](https://www.qubes-os.org/doc/software-update-domu/#installing-software-in-templatevms) (from the repos) that is done automatically for you. However with this method you have to verify software manually. However many times this is not available, so you cannot confirm the authenticity of the software.*

  * **Lack of updates**
    *By installing software from `.deb` or `.rpm` packages manually, the applications require manual updates. It is extremely likely the user will forget to update them and thus run the risk of running software with known security vulnerabilities*

But please do keep in mind that even with these security sacrifices it is still safer for you to run these programs on Qubes than running them on regular systems (regarding the isolation it can provide to other qubes).

## Introduction

All I'm writing here can be found on the [documentation](https://www.qubes-os.org/doc/) with a bit of digging and experimentation. But I'm writing it here as I couldn't find a consolidated guide on how to install this.

This guide is way more extensive than it would need to be, but the goal here is to be didactic. Hopefully as you follow it you end up understanding a few things that can help you use Qubes more independently.

We'll be following the installation of the "[LocalWP](https://localwp.com)" proprietary software. But you can follow this with any other piece of software available for linux as a `.deb` or `.rpm` package.

## 1. Download software

We first go to the  download page for the software, in this case https://localwp.com/releases/. On the download page we should find either a `.deb`, an `.rpm` or both. Each qube can run a different operating system -- some run Debian, some Fedora and others run something else. But the file you download will condition which one you have to choose (and keep this choice on the back of your mind).

* **.rpm -> fedora**
  *If you choose a `.rpm` then the rest of the instructions will be done on a Fedora-based StandaloneVM*

* **.deb -> debian**
  *If you choose a `.deb` then the rest of the instructions will be done on a Debian-based StandaloneVM*

You can download this in any of your qubes. Later you'll move it to the qube where you'll install it.

## 2. Create a StandaloneVM

We will be installing it as a [StandaloneVM](https://www.qubes-os.org/doc/standalone-and-hvm/) for convenience. You typically do it this way when you want to install some software that you will only use in one virtual machine (VM) and can't really install via the usual methods. It is also possible to do it [on TemplateVMs](https://www.qubes-os.org/doc/software-update-domu/#installing-software-in-templatevms) but that is a bit more involved -- let's leave that as homework.

To do this you click on the ![localwp-4|40x32](upload://51gGtQ48lphg6V43MVrRJRbI8Nb.png) "start menu" and open the <kbd>Create new qube</kbd> application. Here you change the following:

* **Name:** we're calling it `develop`, but you can name it whatever you want
*  **Type:** Standalone qube copied from a template
*  **Template**: based on the previous step you either choose `fedora` or `debian`
* **Launch settings after creation**: tick this for the next step

![localwp-2|622x326](upload://4Jcod5Zu5i1hq2FVtqvz4AKakt1.png) 

Then the qube settings window will pop up. Here we'll increase the <kbd>Private storage max. size</kbd> to `20G`. This is basically the size of your home folder (where you'll keep all of your stuff). But you can always increase this later by going to the qube's settings.

![localwp-3|602x500](upload://dteFMKV0quPvWD45eMN7WxerkMO.png) 

After this, hit <kbd>OK</kbd>.

## 3. Installing the software

> **Note**: Now this part will change a bit depending on whether or not you have fedora or debian.

Firstly, copy your download to the `develop` qube (or the name you gave it). If you don't know how to do this, check:

https://www.qubes-os.org/doc/copying-files/

Then you open the terminal application on the `develop` qube and depending on your choice you go either route:

### If on Fedora StandaloneVM

When you moved the file to the StandaloneVM, it landed on the folder `~/QubesIncoming/<SOME_VM>/<FILE>.rpm`. So in our case we ran on the terminal:

```bash
sudo rpm --define '_pkgverify_level digest'  -i ~/QubesIncoming/disp3741/local-5.9.9-linux.rpm
```

> **:warning: Warning:** the "`--define '_pkgverify_level digest' `" a security workaround as Qubes disabled unsigned `.rpm` packages. Read more [on the related announcement](https://github.com/QubesOS/qubes-secpack/blob/master/QSBs/qsb-067-2021.txt).

Most likely it will show you some dependency errors like this:

![wp-local-5|659x167](upload://tWknC6LnYFbXg42ckHJDQ8JKK1w.png) 

This happens because on Linux the software you install most often than not depends on other tools which need to be installed on your system first. This part will very much depend on your situation and you'll have to figure out how to install these dependencies. In our case it told as (see above). So we installed these with:

```bash
sudo dnf install libaio ncurses-compat-libs nss-tools
```
And it should work out well :)

> **Dependencies do not exist / will not be installed?**
> There is the chance this happens to you. In this case you'll probably be wasting a lot of time looking for these. If there was a `.deb` as well, try repeating the process in Debian instead.

After the dependencies are installed you should be ready for installing the actual software you want. Repeat your first install command:

```bash
sudo rpm --define '_pkgverify_level digest' -i ~/QubesIncoming/disp3741/local-5.9.9-linux.rpm
```

This time, it should run without complaining about any dependencies. Skip the debian part by going to [step `4.`](#4-adding-shortcut-to-start-menu)


### If on Debian StandaloneVM

When you moved the file to the StandaloneVM, it landed on the folder `~/QubesIncoming/<SOME_VM>/<FILE>.deb`. So in our case we ran on the terminal:

```bash
sudo apt install ~/QubesIncoming/disp3741/local-5.9.9-linux.deb
```

> **Note** if you see some errors like the following, feel free to ignore it (see why [here](https://forum.qubes-os.org/t/installing-software-in-qubes-from-deb-rpm/2890/14))
> `/home/user/QubesIncoming/<SOME_VM>/<FILE>.deb’ couldn’t be accessed by user ‘_apt`sudo apt install``

## 4. Adding shortcut to start menu

Now the application should be installed but it won't show up in the application's menu. To add it, open the qube settings for the develop qube (the app should be named `<QUBE_NAME>: Qube Settings`). Then open the ![wp-local-6|105x26](upload://bgCZZJd3fXXt1LwxhvD31rRv1w1.png) tab. 

You'll want to add your application's name to the right column. If you don't see it, click on <kbd>Refresh Applications</kbd> button. That will take a couple of seconds but afterwards it should show up. 

> **Still don't see it?**
> If after refreshing your applications, your newly installed application doesn't show up it might be that your `.deb` or `.rpm` didn't include a shortcut (which sucks). If this is the case [read here](https://www.qubes-os.org/doc/managing-appvm-shortcuts/#what-if-my-application-has-not-been-automatically-included-in-the-list-of-available-apps) to try to salvage the situation.

Move you newly installed to the right column and hit <kbd>OK</kbd>. As you can see on the following picture, the `Local` application is selected.

![wp-local-7|679x500](upload://zt5bpL9v0qoFxVBtBrWDsok5UMs.png) 

Then you should see a shortcut for this application on your  ![localwp-4|40x32](upload://51gGtQ48lphg6V43MVrRJRbI8Nb.png) "start menu"  under the `develop` qube.

For more information on this step, [consult the docs](https://www.qubes-os.org/doc/managing-appvm-shortcuts/).

## 5. You're done! :partying_face: 

Now, all you have to do is open the application!

![wp-local-8|689x472](upload://okAvQekkC2TWnWBrj1NasfUNupU.png)

## 6. Update it!

Now, because you installed it manually, whenever there is an update for this application you'll have to remember to update it by repeating this exact process with the new version.

You'll remember to do this, right?! ;)