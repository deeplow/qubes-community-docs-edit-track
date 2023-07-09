I have a script. It does stuff.

1. Copies my default AppVM to a create a new AppVM, sets sys-whonix as a temporary netVM
2. Launches a terminal where i can drop a docker-compose.yml and start the container once to fetch it
3. Makes the container persistent
4. Creates stuff to autostart the container when the AppVM starts.
5. Sets the production netvm to none

Here is the code, maybe it is of some use to others:

```
#!/bin/bash
# This script creates a new docker AppVM
#
# Usage <name>
#
# Parameter
#       <name> the name of the new Docker AppVM

DOCKER_BASE_SOURCE="debian-11-app"
DOCKER_COLOR="gray"
DOCKER_INSTALL_NETVM="sys-whonix"
DOCKER_PRODUCTION_NETVM="none"
TERMINAL_COMMAND="\"gnome-terminal --wait\""

# Clone the source
qvm-clone $DOCKER_BASE_SOURCE $1

# Set netvm for installation
qvm-prefs --set $1 netvm $DOCKER_INSTALL_NETVM

# Remove the dispvm-template flag if it is enabled
qvm-prefs --set $1 template_for_dispvms False

# Make /var/lib/docker persistant
qvm-run -p -u root $1 'mkdir -p /rw/config/qubes-bind-dirs.d'
qvm-run -p -u root $1 'echo "binds+=( /var/lib/docker ) " >> /rw/config/qubes-bind-dirs.d/>

# Enable docker service on startup
qvm-run -p $1 'echo "sudo systemctl start docker" >> ~/.profile'

# Restart
qvm-shutdown --wait $1

# Open Terminal, so user can install stuff
qvm-run -p $1 "gnome-terminal --wait"


# User is done with installing, we can change the netvm to whatever she wants
qvm-prefs --set $1 netvm $DOCKER_PRODUCTION_NETVM
```

This needs to be run in *dom0*.
This does not install docker! It only automates the steps described above, so you need to have docker (and docker-compose if you want that) installed in your template.