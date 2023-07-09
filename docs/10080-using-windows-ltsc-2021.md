@elliotkillick
@brendanhoar
@jevank 
@GWeck

So I finally got around to installing the 2021 edition of Windows 10 Enterprise LTSC. I have the full licensed IoT version which is good until 2032, and it runs pretty well so far. The final result is two templates in my Qubes 4.1 machine:

1. Development template. This has a large root drive (100Gb) and large private drive (50Gb).
2. General purpose template wired up to use sys-whonix. This has a smaller root drive (50Gb) and smaller private drive (30Gb).

Each template serves as the basis for 
  * A single persistent appVM
  * A named DVM that serves up disposable appVM's

Displays work up to 2560x1600.

**Pre-reqs**
* An existing Windows 10 Enterprise LTSC 2019 template to upgrade from. I couldn't get the 2021 version to work from scratch. This means you also need:
  * A working install of Elliot Killick's repo, [**qvm-create-windows-qube**](https://github.com/elliotkillick/qvm-create-windows-qube) and the windows-mgmt qube.
  * The latest Qubes-Windows-Tools msi (QWT). I used the version that I compiled last year, v4.1.65, until I realised there's a later version available. See [the repo here](https://github.com/tabit-pro/qubes-windows-tools-cross) and the [forum post here](https://forum.qubes-os.org/t/qwt-cross-4-1-66-is-available/8309).

* A copy of Windows 10 Enterprise LTSC 2021 iso. IoT or non-IoT will do. You can use the Evaluation version if you want but you will have to re-enable or re-arm the 90-day eval period for a maximum of 4 re-arming attempts. I ended up buying a license for under $75 to avoid the hassle; theoretically I'm now good for the next 10 years.

**Outline of the Upgrade Process**

1. In `dom0` edit the `/usr/bin/qvm-create-windows-qube` script and change the pre-defined sizes for the root and private images to whatever you want.
2. Because the `qvm-create-windows-qube` script always fails for me at the stage where it attempts to automatically install QWT, I run things manually from that point. To assist in that I added the QWT msi and the Post-install scripts (optimize.bat, etc..) to the `auto-qwt.iso` that gets attached in Windows.  Just place what you want into the `auto-qwt` directory and run the command `genisoimage -JR -o "auto-qwt.iso" "auto-qwt"`. That will now be mounted in Windows at that part of the script.
3. Either create a new LTSC 2019 template that uses your new disk size parameters or use an existing one if you're not bothered. Whichever you choose, ensure that QWT and the Post-install scripts are installed, and then put the template through a full windows update. Don't forget to break the airgap that the `qvm-create-windows-qube` script creates.
4. Clone it and name the clone for your new upgraded LTSC 2021 template.
5. Copy the LTSC 2021 iso to your new template's C:\ drive. Start the template and mount it from within and click on `setup.exe`.
6. Let the install do it's thing. If you have a product key, this is where you enter it. Expect the install to take time and perform several reboots. Eventually you'll get back to a logged in desktop.
7. Re-install QWT and the post-install scripts. Reboot and put it through a full update.

That's it in a nutshell. It took me about half a day, perhaps a bit longer. Most of that is elapsed time waiting for the Windows updates and install to finish, but it's worth it to have a long-term non-bloated release of Windows 10 for those times when I need it.

I have yet to install Docker in the dev machine. That makes use of the latest WSL2 / Hyper-V container capability not available in LTSC 2019.

Thanks to all the guys who work on the tools mentioned here, it's very much appreciated.