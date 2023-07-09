This is a guide to getting windows 10 resolution all the way up to 4k 3840x2160!
I've not tested but i believe this may work for different windows versions.
We'll be patching seabios for it to see higher screens resolutions.
I've got it working great with this great tool from Elliotkillick
https://github.com/elliotkillick/qvm-create-windows-qube

1.) First step is to install some necessary build dependencies: I suggest doing it all on a Debian 10 DispVM!

> sudo apt-get install dpkg-dev devscripts quilt
> sudo apt-get build-dep seabios

2.) Setup quilt as described!
Create an alias dquilt in ~/.bashrc:
> alias dquilt="quilt --quiltrc=${HOME}/.quiltrc-dpkg"
> complete -F _quilt_completion -o filenames dquilt

3.) Then let's create ~/.quiltrc-dpkg as follows:

> d=. ; while [ ! -d $d/debian -a $(readlink -e $d) != / ]; do d=$d/..; done
> if [ -d $d/debian ] && [ -z $QUILT_PATCHES ]; then
>     # if in Debian packaging tree with unset $QUILT_PATCHES
>     QUILT_PATCHES="debian/patches"
>     QUILT_PATCH_OPTS="--reject-format=unified"
>     QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
>     QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
>     QUILT_COLORS="diff_hdr=1;32:diff_add=1;34:diff_rem=1;31:diff_hunk=1;33:diff_ctx=35:diff_cctx=33"
>     if ! [ -d $d/debian/patches ]; then mkdir $d/debian/patches; fi
> fi

4.) let’s create a new directory and do everything within it:

> mkdir seabios-patch
> cd seabios-patch

5.) Get the sources for the seabios package so that we can patch it and rebuild it:
The seabios version i got from debian 10 is: 1.12.0

> apt-get source seabios
> cd seabios-1.12.0

6.) The following command creates a new entry in the changelog file and generates a new local version. Provide a description for the change such as “Adding new custom 4K resolution 3840x2160”.

> EMAIL=your.email@example.com dch --local custom
The generated version will be 1.12.0-1custom1.

7.) Now let’s start modifying the bios. We’ll create a new patch called custom-resolutions.patch and use dquilt to track it. The file we’ll need to change is vgasrc/bochsvga.c

> mkdir debian/patches
> dquilt new custom-resolutions.patch
> dquilt add vgasrc/bochsvga.c

8.) Edit vgasrc/bochsvga.c. Add the following lines at the appropriate position, just after the last resolution definition: (You'll find it in the beginning of the file, its easy to find it)
PS: Here I'll be adding two resolutions: 3832x2077 and 3840x2160

> /* custom resolutions */
> { 0x193, { MM_DIRECT, 3832, 2077, 16, 8, 16, SEG_GRAPH } },
> { 0x194, { MM_DIRECT, 3832, 2077, 24, 8, 16, SEG_GRAPH } },
> { 0x195, { MM_DIRECT, 3832, 2077, 32, 8, 16, SEG_GRAPH } },
> { 0x196, { MM_DIRECT, 3840, 2160, 16, 8, 16, SEG_GRAPH } },
> { 0x197, { MM_DIRECT, 3840, 2160, 24, 8, 16, SEG_GRAPH } },
> { 0x198, { MM_DIRECT, 3840, 2160, 32, 8, 16, SEG_GRAPH } },

9.) The following commands will record the patch in the file and save a description alongside the patch.

> dquilt refresh
> dquilt header -e # and add a description, like "adding custom 4k resolutions 3840x2160 and 3832x2077"

10.) Last step is to actually rebuild the package and create a new deb file, ready to be installed:

> dpkg-buildpackage -us -uc

The generated .deb package is availabe in the parent directory.

Then:

After that you will have a Debian (.deb) package, problem is Dom0 is
Fedora and does not use QEMU directly but instead QEMU inside Xen
(qemu-xen):

1. cd .. ; mkdir deb

2. cp seabios_1.12.0-1custom1_all.deb deb #### and cd into the deb directory!

3. dpkg -x <seabios_package_name>.deb . #### This last dot, is the target directory!

4. Go into usr/share/seabios in current directory

5. You only need one file: vgabios-stdvga.bin
Copy that file to Dom0 now, we'll be placing it in the appropriate directory later! you may leave it in dom0 home directory for now.

> Important: Before beginning, backup your stub domain:

We'll continue from Dom0 now!

> cp /usr/lib/xen/boot/stubdom-linux-rootfs stubdom-linux-rootfs-backup

Unpack stub domain in dom0:

```
mkdir /usr/lib/xen/boot/stubroot
cp /usr/lib/xen/boot/stubdom-linux-rootfs stubroot/stubdom-linux-rootfs.gz
cd stubroot
gunzip stubdom-linux-rootfs.gz
cpio -i -d -H newc --no-absolute-filenames < stubdom-linux-rootfs
rm stubdom-linux-rootfs
```
Go to: /usr/lib/xen/boot/stubroot/share/qemu/
Replace vgabios-stdvga.bin with the one you have created! It should be on your dom0 home directory.

On the folder: /usr/lib/xen/boot/stubroot/

Apply the changes: must be with root account, sudo doesnt work!
```
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../stubdom-linux-rootfs
```

Note: You will have to reapply your new vgabios-stdvga.bin every time
Dom0 receives an updates for qemu-xen, so keep it around!

You should have your windows 10 working on any resolution all the way up to 4K 3840x2160 now.

Don't hesitate to give your feedback!
 
Those are the reference links I used to accomplish this fix:
https://groups.google.com/g/qubes-devel/c/aCCGpYysZTQ/m/4yMYxIgoBAAJ
https://adangel.org/2015/09/11/qemu-kvm-custom-resolutions/