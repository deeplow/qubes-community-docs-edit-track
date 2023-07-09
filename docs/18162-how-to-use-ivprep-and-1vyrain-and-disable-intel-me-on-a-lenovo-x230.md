HOW TO USE IVPREP AND 1VYRAIN

TO DISABLE INTEL MANAGEMENT ENGINE

ON A LENOVO X230

STEP BY STEP INSTRUCTIONS

WARNING AND DISCLAIMER: Based on all I read and based on my own experience, this is a fairly safe process. However, I am only a low level nerd, and my skills are limited. I wrote this up for my own records so I could retrace my steps in the future; this was never meant as instructions for others. So while the following could be useful for some people and is to the best of my understanding, it is absolutely possible that I'm wrong in parts of it. Keep your brain switched on, make your own decisions. I'm not responsible if you break anything, or if your laptop suddenly becomes sentient and hails an alien space ship the inhabitants of which end up abducting you to torture you with bad poems, so proceed at your own risk. I recommend having a towel and a copy of the hitchhiker's guide to the galaxy handy. Happy travels!

PLEASE SHARE THE LOVE: If you find these instructions helpful, and if you can and want to improve them and / or spread them to more people, you are absolutely welcome to do so. The more people level up their skills, the better for all of us. Thank you for helping others to join us!

Sorry for bad formatting, didn't have the time to fix that. Feel free to copy paste into a text editor and format any way you like :-)

Here goes:

-----

STEP 0

BEFORE DOING ANYTHING: SET,  WRITE DOWN, then DISABLE *all* BIOS, supervisor, hardware, and other passwords. You must know all passwords even if they are disabled!

Ensure that Windows 10 is installed on the X230

-----

STEP 1: IVPREP - FLASH OLDER, EXPLOITABLE BIOS

Download IVprep zip file
    Start the X230 with Windows 10
    Go to https://github.com/n4ru/IVprep/
    Click "Code", then "Download zip"
    Save IVprep-master.zip to the X230 hard drive

Extract zip file
    In File Explorer, create a folder called IVprep; e.g. in "Documents" folder
    Navigate to where you saved the downloaded zip file
    Move the downloaded zip file into the new IVprep folder
    Right click the zip file, select "7Zip" and "Extract here"

Boot X230 into BIOS
    In Windows 10 menu, search for "BIOS"
    This will lead you to "Change advanced startup options"
    Click "Restart now"
    Select "Turn off your PC"
    The X230 will restart
    Start into BIOS by hitting F1 repeatedly as it restarts

Set BIOS to allow end user BIOS flashing
    In the BIOS, go to "Security" => UEFI BIOS Update Option"
    Set "Flash BIOS Updating by End-Users" to "Enabled"
    Set "Secure RollBack Prevention" to "Disabled"
    X230 must be plugged in and have a full battery
    Save and exit the BIOS, reboot into Windows 10

Run IVprep, flash older, hackable BIOS
    In the extracted zip file folder called "IVprep-master", run the file "downgrade.bat" by double clicking it
    but NOT as Windows administrator!
    The system will reboot and flash the BIOS back to an older version that is compatible / suitable to then do 1vyrain next
    Windows warns and asks if you want Winflash64.exe to run - say yes
    Windows warns computer will shut down in 5 seconds - let it
    Computer shuts down and reboots
    Older, hackable BIOS version gets flashed, you can watch the process on a white on black screen
    X230 shuts down and reboots into Windows

Verify older BIOS got flashed
    Boot X230 into BIOS again
        In Windows 10 menu, search for "BIOS"
        This will lead you to "Change advanced startup options"
        Click "Restart now"
        Select "Turn off your PC"
        The X230 will restart
        Start into BIOS by hitting F1 repeatedly as it restarts
    At the "Main" BIOS screen, top row, read entry behind "UEFI BIOS Version"
    The number in brackets at the end of the line, in black, is the installed BIOS number; e.g. G2EFA0BZ (2.60)
    Compare this number with the list of BIOS versions that are compatible with 1vyrain, here:
        https://github.com/gch1p/thinkpad-bios-software-flashing-guide#bios-versions
    As of March 2023, those are:
        X230         2.60
        X230t         2.58
        T430         2.64
        T430s         2.59
        T530         2.60
        W530         2.58

-----

STEP 2: 1VYRAIN: FLASH MODIFIED BIOS, WHICH ENABLES DISABLING OF INTEL ME AND MORE

STEP 2.1 - ON A SEPARATE LINUX MACHINE:

Download 1vyrain image
    Go here:
        https://1vyra.in/
    Or here (same target destination):
        https://drive.google.com/open?id=1yusq98ja6NmI4G4txKVueFqY_ZEwaZvO
    Top left corner says "1vyrain.iso" - on the right side of the screen, same line, there's a download arrow icon - click it
    "Google drive can't scan this file for viruses" - download anyway
    Downloading the file can take a while, especially via a VPN
    Copy or move the 1vyrain.iso file to the "Documents" folder

Write the downloaded 1vyrain.iso file to a flash drive, in DD mode
    DD mode writes the image file itself directly to the drive, preserving the image's filesystem
    While ISO mode extracts the image's files on the drive with a newly formatted filesystem, usually FAT32 for best compatibility
    One method do identify the /dev/sd... path for the CORRECT flash drive
        Plug in the flash drive
        Open USB Image Writer
        Select the .iso image
        Click the down arrow on the "to" field
        See all USB devices in the drop down list
        Note their size
        Note /dev/sdX path, where X is e.g. a, b, c etc
        Unplug the flash drive, observe which one disappears
        That's the one you want to write to - note down its full path
        CLOSE USB Image Writer - we are not using this to actually write the image

    For the example /dev/sdc:
    sudo dd if="./1vyrain.iso" of="/dev/sdc" status="progress" conv="fsync"

    Write the image
        INFO: https://itsfoss.com/live-usb-with-dd-command/
        sudo dd if="./Documents/1vyrain.iso" of="/dev/sdX" status="progress" conv="fsync"
        Be sure to replace the X  with the letter that corresponds to the correct flash drive that you want to write the ISO to
        as identified before!
        After that, just let dd do it’s thing, and it’ll print a completion message once it’s done.

STEP 2.2 - ON THE X230, STILL ON WINDOWS 10

Some people have to turn off fast startup (Control Panel > Power Options > Choose what the power buttons do > Uncheck "Fast Startup". You may have to click on "Change settings that are currenly unavailable" to unclick fast start.

Boot X230 into BIOS
    In Windows 10 menu, search for "BIOS"
    This will lead you to "Change advanced startup options"
    Click "Restart now"
    Select "Turn off your PC"
    The X230 will restart
    Start into BIOS by hitting F1 repeatedly as it restarts

Set BIOS to boot in UEFI mode only, plug in flash drive, restart
    Set "Startup" => "UEFI / Legacy Boot" to "UEFI Only":
    	Make sure that you are booting "UEFI only" (not "both" or "Legacy") and the CSM is disabled.
	Save and allow restart.
    	You can shut the machine down at the login screen if you want.
    Disable CSM
    Disable "Secure boot"
    Plug in flash drive
    F10 Save and exit
    Restart X230:
    	Insert the thumb drive and boot the machine again, this time using F12 to the boot menu (F12 at the splash screen).
    	Select the 1vyrain bootable thumb drive you inserted earlier. Hit enter.
    	Wait til the machine hibernates.
    	Make sure it's really hibernated ((can take five minutes or more in some cases).
    	I think I remember it asks you if you want to load a modified bios (selection1) or a custom one (option 2).
    	Choose 1.
    	Hit the power button once to restart the thing and let the process finish. Five, maybe ten minutes?

The white on black 1vyrain menu appears and asks you to press "Enter" to start flashing the modifid BIOS

"Please enter a choice: ..." - select option 1 to flash a standard 1vyrain modified BIOS here
    1 Flash modified Lenovo BIOS - this is what to use to simply install 1vyrain on an X230, without any payload
    0 Flash LVDS Modified Lenovo BIOS for X330 (X230 FHD/QHD)
    2 Flash a custom BIOS from URL; this is where a payload such as Skulls can be added to 1vyrain
    3 Shutdown / Abort Procedure

Now 1vyrain flashes the modified BIOS onto the chip.

Don’t be alarmed if your ThinkPad/ThinkLight power cycles a few times after a flash, or you get a CRC Security error. That is normal and will go away after another restart.

There is an initial error flagged on the next boot. Ignore it. I think I remember there are some questions asked, too. Ignore them - don't respond. They time out. Just let the machine boot.

Or, you could hit F1 on boot and check to see if the advanced option is available and can be used to change stuff. This would confirm your jailbreak.

-----

STEP 3: DISABLE INTEL ME

Boot into BIOS
Go into the "advanced" tab
Find the option to disable Intel ME
Disable
Save and exit BIOS
Reboot

-----

STEP 4: CHECK INTEL ME IS ACTUALLY DISABLED

Info on this:
https://github.com/corna/me_cleaner
https://github.com/corna/me_cleaner/wiki/Get-the-status-of-Intel-ME

Make a Linux live image flash drive

Start X230 and boot into Linux live image on flash drive

Connect to the internet

Install a TEMPORARY Linux Mint - details:

a) If you want to keep your Windows install until you have positively confirmed that Intel ME is disabled (so you can use the Windows OS again to retry 1vyrain, if that should be needed) then you can choose "Install Linux Mint alongside Windows 10"

b) If you want to install QUBES and then Mint on top of that in a VM, then in any case this is only a temporary Linux install just to do the Intel ME disabled check (the check doesn't seem to work on a Linux Live Image unfortunately)

c) If parallel install to Windows fails (which it often does), the only remaining option is to try a full disk wipe and install of only Linux Mint, losing your Windows installation.

Use intelmetool to check current status of Intel ME.
    If git is not installed, install it now:
        sudo apt install git
        Or you can also do that via the Linux Mint Software Centre
    Clone coreboot repository:
        git clone --depth=1 https://review.coreboot.org/coreboot
    Run:
        cd coreboot/util/intelmetool
        make
        if Error 1 / "please install libpci-dev and zlib1g-dev""
            sudo apt install libpci-dev
            sudo apt install zlib1g-dev
        ./intelmetool -m
    Compare the output of intelmetool with the table on the bottom of this page:
        https://github.com/corna/me_cleaner/wiki/Get-the-status-of-Intel-ME
    Also, read the output and interpret it with the help of the following information:
        If it reads "Bad news, you have a XYZ chipset so your ME can't be controlled or disabled", don't worry
        Intelmetool seems to just make that statement at the beginning based on just the type of hardware that you have
        What really counts is the status report of Intel ME that follows below that
        1. Firmware init complete - NO
            means ME was unable to finish initializing
        2. Current operation state - Bring up
            means ME is stuck in "bring up" mode, which is essentially its booting phase
        3. Current operation mode - soft temporary disable
            means ME is stuck in "temporary" disable, except it's actually permanent
        4. Progress phase state - ME in temp disable
            again means ME is "temporarily" disabled, except it's actually permanent
        5. ME: failed to become ready
            means ME was unable to get ready, can't be used by anyone, and can't do anything

All this demonstrates nicely that 1vyrain really does what it claims: It can not remove Intel ME, the code is still on the chip - but it can "crash" Intel ME and lock it up permanently, sort of like in a jail cell that it can't get out of (unless you go into the modified advanced BIOS and enable it again, but why would you)

-----

STEP 5: INSTALLING THE OS OF YOUR CHOICE

CONGRATULATIONS! You now have an X230 with a disabled Intel ME.

It either has a dual install of Linux and Windows 10 right now, or just Linux.

If you want to install a different OS, this is the time to do that now.

-----

STEP 6: UPDATING 1VYRAIN

Keep it updated.

To my understanding, at the time of writing this, March 2023, to be able to do this, Windows 10 needs to be reinstalled first. Correct me if I'm wrong here.

To update from an older version of 1vyrain, to a newer version follow the follwing steps. Updates may include security bug fixes.

    1 Write down and remove any BIOS passwords, including supervisor passwords
    2 It is suggested to reset BIOS to default settings, and save
    3 Take out any non-whitelisted devices because the FL1's are untouched
    4 Use IVprep to downgrade to a flashable stock BIOS version (very important, do not skip!)
    5 Obtain the latest 1vyrain image compatible with your machine.
    6 Follow the original installation steps above.

DO NOT SKIP the IVprep process at step 4. This is needed to safely reset to a stock BIOS version. This is different from using IVprep during installation to ensure you are using the proper image. Do not skip step 4 above, this is a crucial step.

The steps to upgrade are essentially the same for downgrading, or moving to any version. Ensure you obtain a compatible 1vyrain image for your machine, reset all passwords, reset to default, and use IVprep to downgrade. You would then go through the installation steps to install the desired 1vyrain version.

-----

I hope this is helpful. Don't forget to help others learn more and set themselves up with more private and secure tech and communication options! Keep being awesome!