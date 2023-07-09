This guide explains the process of installing and using Trezor cryptocurrency hardware wallets on Qubes OS. Many people have been having issues using Trezor on Qubes so I compiled an exhaustive and ultimate guide on the process. Please comment any issues and I will help troubleshoot. 

I am posting the brief instructions here. If you require more detail please see my [Github](https://github.com/UrsidaeCyber/Trezor-Qubes#in-depth-instructions).

Written by Ursidae: https://ursidaecyber.com

#### Step 1: Install Trezor Suite

1. Install the Trezor Suite .AppImage from the Trezor website along with the signature and signing key in a new Whonix AppVM dedicated to Trezor.

2. Verify the download.

3. Execute code:

```
sudo chmod u+x /Downloads/Trezor-Suite-23.4.2-linux-x86_64.AppImage
```

4. Right click on the .AppImage file and press execute to open the application.

#### Step 2: Port Listening

In Trezor Whonix AppVM:

1. Execute command:

```
sudo nano /rw/config/rc.local
```

2. Add the following code to the file:

```
socat TCP-LISTEN:21325,fork EXEC:”qrexec-client-vm sys-usb trezord-service” &
```

3. Save and exit.

#### Step 3: Dom0 Trezor Policy

In Dom0:

1. Execute:

```
sudo nano /etc/qubes-rpc/policy/trezord-service 
```

2. Add this code to the new file:

```
$anyvm $anyvm allow,user=trezord,target=sys-usb 
```

3. Save and exit.

#### Step 4: Fedora Cloning

1. Clone your current regular fedora-37 template Qube and name it fedora-37-sys.

2. Clone the fedora-37-dvm Qube and name it fedora-37-sys-dvm.

3. Set the template for the fedora-37-sys-dvm as fedora-37-sys.

4. Set sys-usb’s template as fedora-37-sys-dvm.

#### Step 5: Trezord Service

In fedora-37-sys-dvm:

1. Execute in terminal:

```
sudo mkdir /usr/local/etc/qubes-rpc
```

2. Execute:

```
 sudo nano /usr/local/etc/qubes-rpc/trezord-service
```

3. Add this code to the file:

```
socat – TCP:localhost:21325 
```

4. Save and exit.

5. Execute:

```
sudo chmod +x /usr/local/etc/qubes-rpc/trezord-service
```

#### Step 6: Trezor Bridge

In fedora-37-sys:

Download the Trezor Bridge .rpm file from Trezor.

1. Execute:

```
sudo chmod u+x /Downloads/trezor-bridge-2.0.27-1.x86_64.rpm
```

2. Then execute:

```
sudo rpm -i /Downloads/trezor-bridge-2.0.27-1.x86_64.rpm
```

#### Step 7: Udev rules

Note on Udev rpm use: Using the Trezor-provided Udev rpm file does not work for Qubes. See in-depth explanation section below. Use the provided Method 1 or 2 here. Use method 1 if comforable with enabling networking in template and method 2 if not.

**Method 1: Manual Build**

In fedora-37-sys:

1. Run:

```
sudo nano /etc/udev/rules.d/51-trezor.rules
```

Copy and paste this code into the file:

```
# Trezor
```

```
SUBSYSTEM=="usb", ATTR{idVendor}=="534c", ATTR{idProduct}=="0001", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
```

```
KERNEL=="hidraw*", ATTRS{idVendor}=="534c", ATTRS{idProduct}=="0001", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
```

```
# Trezor v2
```

```
SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="53c0", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
```

```
SUBSYSTEM=="usb", ATTR{idVendor}=="1209", ATTR{idProduct}=="53c1", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="trezor%n"
```

```
KERNEL=="hidraw*", ATTRS{idVendor}=="1209", ATTRS{idProduct}=="53c1", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
```


2. Save and exit.

3. Execute:

```
sudo chmod +x /etc/udev/rules.d/51-trezor.rules
```

**OR**

**Method 2: Curl Installation**

1. In fedora-37-sys enable networking.

2. Install curl:

```
sudo dnf install curl
```

3. Download Udev rules:

```
sudo curl https://data.trezor.io/udev/51-trezor.rules -o /etc/udev/rules.d/51-trezor.rules
```

4. Allow execution:

```
sudo chmod +x /etc/udev/rules.d/51-trezor.rules
```

5. Revoke fedora-37-sys networking permissions.

#### Step 8: Install Trezor Dependencies

In the Trezor Whonix AppVM:

1. Install pip:

```
sudo apt install pip
```

2. Execute:

```
pip3 install –user trezor
```

**AND**

In fedora-37-sys:

1. Allow networking.

2. Execute:

```
sudo dnf install trezor-common
```

3. Revoke networking permissions in fedora-37-sys.

Done.