- The installation scripts and provided tools may have bugs, be vulnerable to Man in the Middle (MitM) attacks or other vulnerabilities.

- Adding additional repositories or tools for installing software extends your trust to those tool providers.

Please keep in mind that using such a VM or VM's based on the template for security and privacy critical tasks is not recommended.

# How to create Penetration Testers Framework (PTF) VM

"The PenTesters Framework (PTF) is a Python script designed for Debian/Ubuntu/ArchLinux based distributions to create a similar and familiar distribution for Penetration Testing.

PTF attempts to install all of your penetration testing tools (latest and greatest), compile them, build them, and make it so that you can install/update your distribution on any machine." (source [PTF Readme](https://github.com/trustedsec/ptf/blob/master/README.md))

**Note** PTF works on Debian testing as well as on Debian 8. PTF itself works with Debian 8, but the software tools will have missing dependencies. Metasploit for example requires a newer Ruby version than Debian 8 has in the repositories. Therefore the best way to install PTF is by upgrading a Debian 8 into Debian testing with additional Kali repositories. Instead of installing the tools from Kali, PTF will install and update the newest tools.

# Create Debian Based Penetration Testers Framework (PTF) Template

1.  Create PTF template

    1.  Follow [Create Debian Based Kali Template](https://www.qubes-os.org/doc/pentesting/kali/) till step 7.

    2.  (Optional) Rename the cloned template to `ptf`

2.  Download PTF

    ```
     sudo apt-get install git
     cd /opt
     sudo git clone https://github.com/trustedsec/ptf.git
    ```

    - (Optional) Configure PTF

      1.  Go to configuration directory

          ```
           cd /opt/ptf/config
          ```

      2.  Edit the configuration file

          for example by using vim:

          ```
           sudo vim ptf.config
          ```

          the configuration options are described in the `ptf.config` file

3.  Install PTF

    ```
     cd /opt/ptf
     sudo ./ptf
    ```

    **Note:** the config file has to be in the same directory as the executable. It is not possible to do sudo ptf/ptf

    PTF will put itself into `/usr/local/bin/ptf`. You can use `ptf` from now on.

4.  Install/Update modules (tools)

    1.  Start PTF

        ```
         sudo ptf
        ```

        ![PTF start banner](upload://v44SJM1EUppNhLWeUOKA3QCO4bQ.png)

    2.  Show available modules (tools)

        ```
         ptf> show modules
        ```

    3.  Install/Update modules (all/)

        - Install/Update all tools

          ```
            ptf> use modules/install_update_all
          ```

        - or by category Install/Update

          ```
            ptf> use modules/code-audit/install_update_all
          ```

        - or individually (example Metasploit)

          1.  Search for module

              ```
               ptf> search metasploit
               [*] Search results below:
               modules/exploitation/metasploit
              ```

          2.  Use module

              ```
               ptf> use modules/exploitation/metasploit
               ptf:(modules/exploitation/metasploit)>
              ```

          3.  Install module

              ```
               ptf:(modules/exploitation/metasploit)>install
              ```

          4.  Run Metasploit

              ```
               ptf:(modules/exploitation/metasploit)>exit
               ptf> quit
               [*] Exiting PTF - the easy pentest platform creation framework.
               sudo msfconsole
              ```

5.  Create an AppVM based on the `ptf` template

    - (Optional) Attach necessary devices

# Alternative Options to PTF

- [BlackArch](https://www.qubes-os.org/doc/pentesting/blackarch/)
- [Kali](https://www.qubes-os.org/doc/pentesting/kali/)
- [Pentesting](https://www.qubes-os.org/doc/pentesting/)

------------------------------------------------------------------------

[details="This document was migrated from the qubes-community project"]
- [Page archive](https://github.com/Qubes-Community/Contents/blob/master/docs/os/pentesting/ptf.md)
- First commit: 08 Dec 2020. Last commit: 08 Dec 2020.
- Applicable Qubes OS releases based on commit dates and [supported releases](https://www.qubes-os.org/doc/supported-releases/): 4.0
- Original author(s) (GitHub usernames): andrewdavidwong
- Original author(s) (forum usernames): @adw
- Document license: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
[/details]

<div data-theme-toc="true"> </div>