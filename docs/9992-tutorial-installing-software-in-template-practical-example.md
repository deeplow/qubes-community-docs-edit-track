Continuing the discussion from [Installing software in templates](https://forum.qubes-os.org/t/installing-software-in-templates/9989):

A very important step in using Qubes is being able to install applications on your qubes. Installing software in a template, is generally the normal way of doing it.

You should always look on the official documentation first. https://www.qubes-os.org/doc/how-to-install-software/#instructions I'll give a particular example, following the instructions on the documentation.

[details="Background reading on package managers"]

## Background
This is a big question. Most qubes (which are just *virtual machines* under the hood) are running linux. Or rather a flavor of linux (fedora, debian, etc.).

Just like on MacOS or Windows you can install software by downloading from the developer's website, generally the safest way is to find it on the App Store / Microsoft store. Easy central way of finding software.

On Linux, that's pretty much the same thing. That "store" is called the package manager. There are some graphical user interfaces (GUIs) but these [don't work under Qubes](https://github.com/QubesOS/qubes-issues/issues/6310) since they require an internet connection. *So the only way to install software in templates is by using the terminal*.

[/details]


## Practical example

**Goal**: install a music player on `personal` qube

1. I learn about the template on which the `personal` qube is based by going to the qubes's settings. I learn its template is `fedora-34`.
2. I search online for "best music player for fedora" to find a piece of software that's already shipped for fedora (in it's "app store"). I found the software `clementine` works there.

   > There I look for the installation command that should look like 
   >
   > `sudo dnf install clementine`
   >
   > What I wanted to find is really the package name `clementine`. 

3. I follow the [instructions from the documentation](https://www.qubes-os.org/doc/how-to-install-software/#instructions):
    1. **I open the `gnome-terminal` application** from the `fedora-34` template qube. (a terminal window will pop up)
    2. **I type `sudo dnf install clementine`**
    3. **I shut down the `fedora-34` template**, with the command `sudo shutdown`, for example.
   4. **I shut down the `personal` qube** if it was already running (so it can get the freshly installed `clementine` player from the `fedora-34`)

    5. I add the `clementine` application to the `personal` qube - follow the [step 6 in the documentation](https://www.qubes-os.org/doc/how-to-install-software/#instructions)
 
       > This is needed because even though you installed clementine for the template, you probably won't want to see the audio player now listed on all the qubes based on that template (work, unstrusted, etc.)

4. Start `clementine` on your  `personal` qube by clicking on the `app menu` » `personal` » `clementine`

5. :partying_face: it should open clementine!

## What if the software is not available?

Good question. If the software is not available in the package manager / app store of the template, you need to look into other ways. See the following resource:

https://forum.qubes-os.org/t/9991