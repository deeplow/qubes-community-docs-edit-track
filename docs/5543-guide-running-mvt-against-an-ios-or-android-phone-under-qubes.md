I had some time to experiment with the [Mobile Verification Toolkit](https://github.com/mvt-project/mvt) that was mentioned in an Amnesty International [forensic analysis](https://www.amnesty.org/en/latest/research/2021/07/forensic-methodology-report-how-to-catch-nso-groups-pegasus/) of phones that had been found to have spyware installed.

> Mobile Verification Toolkit (MVT) is a collection of utilities to simplify and automate the process of gathering forensic traces helpful to identify a potential compromise of Android and iOS devices.

On iOS, the process is to perform an iTunes backup of the phone, decrypt the backup, then analyze the data for indicators of compromise known to be in use. Since there is no iTunes for us, we use the open source imobiledevice utilities to create a backup off the iPhone. PIN code of the iPhone is required.

On Android, it uses adb to perform a backup of the SMS database. It also uses adb to download packages off the device and verify them against VirusTotal and Koodous online services to determine if they are known to be malware.


This is a guide on how I ran it under Qubes on an iOS and Android device. This is going to be long so bear with me...

**Warnings:**

- Performing a backup of a mobile device _will_ include sensitive data (such as photos). Don't leave the data sitting around after you're done. Forensic investigators love backups...
- This is why the instructions will use Disposable VMs
- USB redirection with sys-usb was not reliable for me. Therefore the qube running mvt had the USB controller attached to it.
  - If you use a USB keyboard, don't follow this verbatim.
  - If you have stuff connected via USB, don't follow this verbatim.
  - What you can do is make your sys-usb disposable, give it network, and just run all install commands within it, knowing everything will be lost after restarting your disposable sys-usb.
- This installs software outside of the package manager. This means package signing and integrity verification are not being performed for:
  - Python packages being installed with pip.
  - Code being downloaded from GitHub.
  - Java jars being built using online Maven repositories, which pulls other code in.
  - So, all of the above could be used to exploit your VM and/or your phone.
  
**Overall process:**

1. Create a template VM that contains package manager dependencies
2. Create a Disposable Template from the above template that installs the non-package-manager software into /usr/local
3. Create named Disposable VMs that use the Disposable Template to run the software.

This way, the named Disposable VMs will inherit package manager packages from the template, mvt and other stuff from the disposable template, and after shutting down the VM, no data will be retained.  

**Template Setup:**

1. Open Qube Manager
2. Select debian-10, right-click, Clone qube

   - A minimal Debian should work but probably needs extra packages; I haven't investigated which ones, but udev-related stuff might be missing.
3. Name it "mvt-template"
4. Open a terminal in mvt-template
5. Install software requirements:

       sudo apt install git python3 python3-pip libusb-1.0-0 sqlite3 \
                        libimobiledevice-utils \
                        adb openjdk-11-jre maven

6. Shutdown mvt-template


**Create Disposable Template:**

1. Create Qubes VM
2. Call it "mvt-dvm"
3. Template: mvt-template
4. Networking: sys-firewall or whatever you want, but this is only temporary
5. Click 'launch settings after creation'
6. Hit OK
7. In Settings:Advanced, check Disposable VM Template, Hit Apply
8. In Settings:Advanced: set Default DisposableVM Template to mvt-dvm

**Install mvt software** into /rw of mvt-dvm:

1. Qube Manager
2. Right-click mvt-dvm, Start/Resume qube
3. Open a terminal in mvt-dvm (Q icon, mvt-dvm, Run Terminal)
4. Install mvt. Note this is the most vulnerable part of the installation since we will be downloading stuff without any sort of signatures.

       mkdir ~/mvt-install
       cd ~/mvt-install

       # Get stuff
       git clone https://github.com/mvt-project/mvt
       git clone https://github.com/nelenkov/android-backup-extractor
       wget https://github.com/AmnestyTech/investigations/raw/master/2021-07-18_nso/pegasus.stix2

       # Install mvt to /usr/local
       cd ~/mvt-install/mvt
       sudo pip3 install .
       # Yes, no sudo is needed to install to ~/.local, but I want it at /usr/local

       # Install abe to /usr/local
       cd ~/mvt-install/android-backup-extractor
       mvn clean package
       sudo mv target/abe.jar /usr/local/bin/abe.jar

       # Install IOCs stix2 file to /usr/local
       cd ~/mvt-install
       sudo mkdir /usr/local/share/mvt-iocs
       sudo cp pegasus.stix2 /usr/local/share/mvt-iocs

5. At this point software is installed to:

   - /usr/local/bin/mvt-android
   - /usr/local/bin/mvt-ios
   - /usr/local/bin/abe.jar
   - /usr/local/share/mvt-iocs/pegasus.stix2

6. **Disable networking for mvt-dvm**

7. ~/mvt-install can be removed now.

8. Shutdown mvt-dvm

**Create App VMs for running mvt:**

1. Create non-networked mvt-device AppVM for device extraction. 

   This has to be done through the command line because we are creating a named disposable VM. This a VM that will derive initial data from mvt-dvm, but will lose everything in /home after shutdown.

       qvm-create --class DispVM --template mvt-dvm --label gray mvt-device

2. Edit settings of mvt-device
3. In Settings:Advanced, set Mode to HVM, hit Apply
4. In Settings:Devices, assign it your USB controller, hit Apply
5. In Applications, make sure Run Terminal is in the Selected column
6. Increase the Private volume size - this will need to be big enough to store 2 full device backups. If there are lots of pictures, files, and apps on the phone, you might need to increase this significantly. FWIW on a phone with only a handful of pictures and only WhatsApp installed, the backup was 500MB.

7. Create networked mvt-network AppVM for checking Android [optional]:

       qvm-create --class DispVM --template mvt-dvm --label blue mvt-network

8. Edit settings of mvt-network
9. Networking: sys-firewall, sys-whonix, sys-vpn, etc
10. Make sure Run Terminal is in the Selected column of Applications
11. This might need more Private Volume size as well - it will [temporarily] have copies of apps installed on the android device.


**Running mvt on an iOS device:**

0. Shutdown sys-usb if you have it running.
   - If you have a USB keyboard or other USB accessories connected, you will lose them, so _stop here if you're unsure how to handle this_.
1. Open a terminal in mvt-device. From dom0:

       qvm-run mvt-device qubes-run-terminal

2. Connect iPhone to the USB Port
3. Expect a Trust prompt on the iPhone; approve it with the PIN. If this step does not complete, try again with `idevicepair pair`
4. Enable backup encryption and enter a password used to encrypt the backup.

   It does not matter much as it will immediately be decrypted. This is needed because an encrypted backup contains more data than an unencrypted backup.

       idevicebackup2 -i backup encryption on

5. Perform the backup to directory "step1-encrypted"

       cd ~
       mkdir mvt-ios-data
       cd ~/mvt-ios-data

       mkdir step1-encrypted
       idevicebackup2 backup --full step1-encrypted

6. Decrypt the backup to directory "step2-decrypted"

       cd ~/mvt-ios-data
       mvt-ios decrypt-backup -d step2-decrypted step1-encrypted/*

7. Perform an analysis of the backup and get results to "step3-results"

       cd ~/mvt-ios-data
       mvt-ios check-backup --iocs /usr/local/share/mvt-iocs/pegasus.stix2 --output step3-results step2-decrypted

8. **Review any red WARNINGs here...these are possible indicators of compromise**

   Review other data in step3-results, for example timeline.csv shows a chronology of usage.

9. Clean up by unpairing the iPhone and mvt-device AppVM

       idevicepair unpair

10. Unplug the iPhone

11. Review any other data in the backup. When the VM is shutdown, this data will be lost.


**Running mvt on Android device** to check **SMS** links:

1. Enable developer options on the phone [Settings/About/tap build 7 times]
2. Go into developer options on the phone [Settings/System/Developer options]
3. Enable USB Debugging
4. Plug in the phone to the USB port
5. Open temrinal in mvt-device, from dom0:

       qvm-run mvt-device qubes-run-terminal

6. Make sure adb can see the device in mvt-device:

       # Confirm on the phone to accept the fingerprint and authorize your Qubes computer
       adb devices

7. Run a backup of SMS. This will ask for a password on the phone to encrypt the backup. Doesn't matter much because it'll be immediately decrypted.

       mkdir ~/mvt-android-data
       cd ~/mvt-android-data

       adb backup com.android.providers.telephony

       # should give a backup.ab file

8. Decrypt and extract the backup with android-backup-extractor

       cd ~/mvt-android-data
       java -jar /usr/local/bin/abe.jar unpack backup.ab backup.tar
       tar xvf backup.tar

9. Check the backup with mvt-android:

       mvt-android check-backup --iocs /usr/local/share/mvt-iocs/pegasus.stix2 --output . .

10. The above doesn't appear to check IOCs, but does give an sms.json file showing text messages that contained hyperlinks.

        grep body sms.json
        # investigate suspicious links

**Checking the APKs (packages)** of the android device

1. Retrieve APKs from the device

       cd ~/mvt-android-data

       adb kill-server
       
       # Make sure screen is unlocked and on to reauthorize USB debugging, keep trying if it doesn't make it past 1 line of output
       mvt-android download-apks -o android-apks

2. Copy APKs to mvt-network

       # select mvt-network as the target VM
       qvm-copy ~/mvt-android-data/android-apks

3. In mvt-network, check APKs against VirusTotal and Koodous

       cd ~/QubesIncoming/mvt-device/android-apks
       mvt-android download-apks -A -f packages.json

**Cleanup for android** in mvt-device:

1. In Developer options on the phone, tap Revoke USB debugging authorizations
2. Disable USB debugging
3. Unplug the phone

**Conclusion**:

When mvt-device or mvt-network are shutdown, the backup data in /home will be gone. Booting them up again should yield a fresh /home directory, but with mvt still installed at /usr/local.