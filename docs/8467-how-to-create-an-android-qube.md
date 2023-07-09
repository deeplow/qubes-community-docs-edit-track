Step 1.) download the latest android-x86 iso. You can choose to build it instead as well.
Step 2.) create a new standalone hvm with no template. If using 4.1, it will ask you to boot the iso. don't do it yet. Let it silently fail.
Step 3.) go to the hvm's settings and choose advanced. from here we want to make sure our vm is an hvm and that debug mode is enabled. Also depending on the version of amdroid-x86 being used, you might want to have at least 512 MB of RAM available.
Step 4.) choose to boot cdrom image and use the iso you either built or downloaded earlier.
Step 5.) follow normal android-x86 install instructions.
Step 6.) when setting up networking, choose the VirtWifi option.
after that, you are done.