- The installation scripts and provided tools may have bugs, be vulnerable to Man in the Middle (MitM) attacks or other vulnerabilities.

- Adding additional repositories or tools for installing software extends your trust to those tool providers.

Please keep in mind that using such a VM or VMs based on the template for security and privacy critical tasks is not recommended.

# How to Create a BlackArch VM

[BlackArch](https://www.blackarch.org) Linux is an [Arch Linux](https://www.archlinux.org)-based distribution for penetration testers and security researchers. The repository contains [1434](https://www.blackarch.org/tools.html) tools.

- List of [tools](https://www.blackarch.org/tools.html)
- [Installation Instructions](https://www.blackarch.org/downloads.html)

# Create ArchLinux Based BlackArch Template

1.  Create ArchlLinux Template

    - Follow the [Archlinux Template instructions](https://www.qubes-os.org/doc/building-archlinux-template/)

2.  Update Template

    ```
     sudo pacman -Syyu
    ```

3.  Clone template

    1.  Via Qubes VM Manager

    2.  Via command line

        ```
         qvm-clone archlinux blackarch
        ```

4.  Install BlackArch repository

    ```
     $ curl -O https://blackarch.org/strap.sh

     # The SHA1 sum should match: 34b1a3698a4c971807fb1fe41463b9d25e1a4a09
     $ sha1sum strap.sh

     # Set execute bit
     $ chmod +x strap.sh

     # Run strap.sh
     $ sudo ./strap.sh
    ```

5.  Install tools

    - install all tools

      ```
        sudo pacman -S blackarch
      ```

    - or by category:

      ```
        # list available categories
        pacman -Sg | grep blackarch

        # install category
        sudo pacman -S blackarch-<category>

        # example
        sudo pacman -S blackarch-forensic
      ```

    - or specific tool

      ```
        # Search for tool
        pacman -Ss <tool-name>

        # Install tool
        sudo pacman -S <tool-name>

        # Example
        pacman -Ss burpsuite
        sudo pacman -S burpsuite
      ```

6.  Create a AppVMs based on the `blackarch` template

    - (Optional) Attach necessary devices

# Alternative Options to BlackArch

- [Kali](https://www.qubes-os.org/doc/pentesting/kali/)
- [PenTester Framework (PTF)](https://www.qubes-os.org/doc/pentesting/ptf/)
- [Pentesting](https://www.qubes-os.org/doc/pentesting/)

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/pentesting/blackarch.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>