Introduction
-

This guide will help you to quickly configure blue light filter in Qubes OS with XFCE desktop environment.
![](upload://2RlDyMTKjN0J6n8EkhHHWkxbRRi.png)
**[Redshift](https://github.com/jonls/redshift)**

Installation
-
type `sudo qubes-dom0-update redshift` in dom0 terminal and confirm installation by `y`

! 
-
**Remember that installing anything in dom0 is not recommended for security reasons**

Configuration
-

Create confiig file - dom0 terminal:
* `cd .config`
*  `nano redshift.conf`
You will create an empty file in path `~/.config/redshift.conf`. Here you have to set values:
your location*, Day/Night Color. [Here](https://raw.githubusercontent.com/jonls/redshift/master/redshift.conf.sample) is explained sample with more functionality.
Basic configuration looks like: 


        [redshift]
        temp-day=6400
        temp-night=3200
        adjustment-method=randr
        location-provider=manual
    
        [manual]
        lat=xx.xxxxx
        lon=xx.xxxxx

Where xx.xxxxx are my city latitude and longitude

* Save this configuration file
* Type `redshift` in dom0 to start the program. It will load previously saved configuration.

*Location is needed to know when actually sun sets for you. Without that parameter, redshift may not work.
To find city longitude and latitude you can use geonames.org   

Automation/Startup
-

we need to create script `~/.startupscripts/redshift.sh`, open dom0 terminal
* `mkdir .startupscripts`
* `cd .startupscripts`
* `nano redshift.sh`
* paste:     

        #!/bin/sh
        sleep 2
        redshift

* save
* `chmod +x redshift.sh` - (this makes script executable)

* Add `redshift` to autostart in xfce settings

    Name: Redshift
    Description: Blue light filter
    Command: sh /home/USERNAME/.startupscripts/redshift.sh

Documentation
-
* http://jonls.dk/redshift/
* https://github.com/jonls/redshift
* https://wiki.archlinux.org/index.php/Redshift


*If You want to copy this to the Qubes OS documentation, sure :slight_smile: it'll be faster to find.*