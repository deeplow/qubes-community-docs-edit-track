# :placard: Navigating the Waters: *Installing Software in Qubes*

Installing software in Qubes OS can be a daunting experience. This guide's goal is to serve as a crossroad sign to help you navigate this landscape.


[details="Note for users coming from Windows or MacOS"]
If you're used proprietary tool like Microsoft office or Photoshop, you won't be able to run them on your regular app qubes (though you can [run Windows on Qubes](http://qubes-os.org/doc/windows/), but it's a subpar experience).

Fortunately, *there are easy ways to find alternatives:*
   * **AlternativeTo**
     [AlternativeTo.net](https://alternativeto.net/software/adobe-photoshop/?platform=linux) is a website that lets you find alternatives to software. Make use of the filters to look for software compatible on Linux (and preferably with open source license). 

     *example: [Photoshop open source alternatives on Linux](https://alternativeto.net/software/adobe-photoshop/?license=opensource&platform=linux)*

   * **Search Engine**
   Looking for a music player or a video player? Just search for it. Most likely all your app qubes are running the Fedora Linux "version", so you search: `best music player for fedora` and you;ve got your answer.
[/details]



> :information_source: **Note**
> Because Qubes and Linux are diverse, you'll have various methods to install the same thing.
> Some are easier and some harder.

## Which installation ways do you see on the official website?

1. **Visit the official website for the software**
    Check the listed methods for installing it.


    > **:scream: The official instructions are too complicated?**
    > Instead search on your favorite search engine for the following and repeat:
    >  - how to install _______ on Fedora
    >  - how to install _______ on Debian
   > 
   > *And pick whichever is easier* -- with a suspicious mind, of course



2. **Install according to table bellow**
    Based on the instalation instructions you'll have a different method of installing and a different place where to install (app qube, template, standalone qube).

    > :bulb: **It is possible many apply**
    > Generally you should choose the first on the list bellow.

    |  **If you find something like...** | Then you install in...       | Instructions | 
    |-------------------------------------------|-------------------------------|-----------------| 
    | `sudo dnf install _____`             | fedora template           | [jump to guide](#installing-in-template-qube-3)
    | `sudo apt install   _____`                        | debian template          | [jump to guide](#installing-in-template-qube-3)
    | 
    | `flatpak`                                      | app qube                    | [jump to guide](#flatpak-6)
    | `snap`                                         | app qube                    | [jump to guide](#snap-5)
    |  | |    
    | `.deb`                                          | debian standalone     | [jump to guide](#installing-in-a-dedicated-qube-standalone-qube-7)
    | `.rpm`                                          | fedora standalone     | [jump to guide](#installing-in-a-dedicated-qube-standalone-qube-7)

---

> :stop_sign: **Stop reading here**
> What follows are the reference material that is linked to in the above table

-----

## Installing in Template qube
A [template qube](https://www.qubes-os.org/doc/templates/) is like a boilerplace for app qubes based on it. When you install a piece of software on it all qubes based on the template will also get that piece of software.

When you install it like this, you get updates via [routine updates](https://www.qubes-os.org/doc/how-to-update/#routine-updates) (normal way of updating).

   - **When software is already available in template's package manager**
 <kbd>**difficulty**:  "easy" </kbd><kbd>recommended way (if possible)</kbd>

      Just follow the [official documentation](https://www.qubes-os.org/doc/how-to-install-software/#installing-software-from-default-repositories) or see a practical example [here](https://forum.qubes-os.org/t/9992/1).

   - **When software is available as an additional package repository only** 
   <kbd>**difficulty**:  medium </kbd>
    Follow it on the official documentation: [How to Install Software | Installing software from other sources](https://www.qubes-os.org/doc/how-to-install-software/#installing-software-from-other-sources). Examples include [installing signal](https://forum.qubes-os.org/t/5221/1).

[details="other methods (advanced)"]
> :warning: This is for **advanced users only**. Updates are manual.

Using the [updates proxy](https://www.qubes-os.org/doc/how-to-install-software/#updates-proxy) to give software management programs internet access in the template.

In case this software installs stuff in [non-persistent directories](https://www.whonix.org/wiki/Qubes#Qubes_Persistence) you'll need to use [bind-dirs](https://www.qubes-os.org/doc/bind-dirs/) those directories persist when starting an app qube based on the template.

Examples of what can be achieved with this
  - `pip install` in template - https://forum.qubes-os.org/t/external-repositories-pip-snap-appimage-persistent-installations-in-template-appvm/561/4 (**Note** if using pip, you're probably better off installing it in an *app qube* with a [python virtual environment](https://docs.python.org/3/library/venv.html))
[/details]


## Installing in App qube
App qubes are your regular qubes (e.g. `personal` or `work` qubes). If you install like this the application will only be available in that [app qube](https://www.qubes-os.org/doc/glossary/#app-qube) where you installed it.

### Snap
Read more at [Installing Snap Packages](https://www.qubes-os.org/doc/how-to-install-software/#installing-snap-packages)  (official documentation). Updates [should be done automatically](https://snapcraft.io/docs/getting-started#heading--refreshing) but you should double-check this.

### Flatpak
[Qube Apps](https://micahflee.com/2021/11/introducing-qube-apps/) - developed by Micah Lee, a trusted community member.
   > :warning: Updates **are manual** but just one-click. 

- **When an [AppImage](https://appimage.github.io/) is available**. Just download the AppImage and [follow the installation instructions](https://docs.appimage.org/introduction/quickstart.html#ref-how-to-run-appimage).
   > :warning: Updates **are manual** and tiresome. It's basically repeating the whole install process! Plus, you'll have to figure out a way to know when there are updates. This bad security practice means it will probably be outdated for a long time.


## Installing in a dedicated qube (standalone qube)

[Standalone qubes](https://www.qubes-os.org/doc/standalone-and-hvm/) are dedicated qubes. They are good if you want to install random software that you don't trust to be installed on your main templates, only really need to use in a single qube.

> :bulb: **Want this software in 2+ qubes?** 
> If you want to have this software made available for multiple qubes, then you may want to consider cloning a template and installing all of that there. See an example comment of this [here](https://forum.qubes-os.org/t/installing-software-in-qubes-all-methods/9991/14).

Regardless, the security isolation and flexibility may make this a way to go for very particular pieces of software.

- **Install individual `.deb` or `.rpm`** that you download form a website. See how to do this here: https://forum.qubes-os.org/t/2890/1
   > :warning: Updates **are manual** and tiresome. It's basically repeating the whole install process! (bad security practice). [There are ways of automating](https://forum.qubes-os.org/t/update-scripts-for-ms-teams-zoom-or-chrome-etc-in-standalone-qube/16881/5) them but they are not trivial.
- [**install like a template**](https://forum.qubes-os.org/t/installing-software-in-qubes-all-methods/9991#installing-in-template-qube-2)
   You can install stuff as if you were in a template see the first section
- [**install like an app qube**](https://forum.qubes-os.org/t/installing-software-in-qubes-all-methods/9991#installing-in-app-qube-3)
  Install as if you were on an app qube with the methods in the section above.
<a name="testinganchors" class="anchor" href="#testinganchors"></a>
<div data-theme-toc="true"> </div>