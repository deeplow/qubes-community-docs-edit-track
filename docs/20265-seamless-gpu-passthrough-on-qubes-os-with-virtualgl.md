We are presenting to you a guide regarding GPU passthrough created in collaboration with peers.

Qubes OS already has extensive documentation available about GPU passthrough for 3D accelerated tasks but they all require in depth configuration, extra displays, and extra input devices. With VirtualGL (https://virtualgl.org) one can take advantage of the existing Qubes OS framework for audio/display by offloading OpenGL onto the secondary graphics card directly with VirtualGL. This document will mostly be working off of the Neowutran (https://neowutran.ovh/qubes/articles/gaming_windows_hvm.html) guide with a few tweaks. 

Casual applications will work but some games require capturing the mouse cursor and Qubes OS doesn't support this, so the camera will not work with the emulated input device. An extra gamepad etc. will probably be desired.

Device compatibility:
Nvidia: Works but lower FPS reported on Nouveau/Mesa driver, proprietary driver is fine.
AMD: RadeonSI Mesa driver has issues with EGL on the tested card, but nothing should be an endemic problem with the brand. It is assumed propietary OpenGL will work but it remains untested due to difficulties in patching Ubuntu driver for Debian template. Alternatively, GLX offloading to a dedicated X server works. Conflicts occurred having Nvidia drivers installed with the AMD card, VirtualGL reports no EGL devices while they are installed. A simple fix is possibly preloading the proper libraries.

Both graphics cards seem to support Xen's memory balancing, but only up to the amount of initial memory at boot.

Instructions:
Edit GRUB configuration in **/etc/default/grub** to restrict the secondary graphics card from dom0 with the **rd.qubes.hide_pci** kernel option. Reconfigure GRUB with **grub2-mkconfig -o /boot/grub2/grub.cfg**. Reboot.

Create a new template to hold graphics drivers and VirtualGL configuration.

Follow the instructions to install desired graphics drivers for the specific OS template.

Download VirtualGL from its SourceForge repository and install it to the template.

Run **vglserver_config** as root and configure for EGL, respond no to the prompt about framebuffer access.

Edit **/etc/profile** and append **export VGL_DISPLAY=egl** to the bottom.

Shutdown the template. Create a new VM from it. Set virtualization mode to HVM and kernel to Qube provided. Attach secondary graphics card to it. Boot, and execute **vglrun** with a command to get accelerated graphics. Wrapping a shell also works (**vglrun bash**) to avoid having to type it every time, but there is no obvious way to automate this at startup.

Donations:
Monero/XMR:87ZPgPnYTdvMnVpdhvoNhvjQ4AvnEPZvQP3XmULGxpjTJCTtpnB9cgmYoRe8Bj6Dh9867CUn67yqQbCU2jwCVeykPjEdMu9