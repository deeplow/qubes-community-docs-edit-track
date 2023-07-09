***NOTE: While this guide is still a work in progress, it is now useful enough that many people should be able to use it to get logging working locally on their system***



After a 7 year discussion on logging, a Qubes [pull request](https://github.com/QubesOS/qubes-core-agent-linux/pull/321) was recently created for new patches to allow the creation of a logging qube.  

Both DisposableVM's *and* AppVM's currently discard all their logs when they are shut down, so this was desperately needed.  (note: verify that that situation hasn't changed for AppVM's)

This thread is the start of a guide for how to set up a logging qube that uses those new patches.  We can use this thread to collect all the logging qube related information with the hope of having a complete guide by the time the patches are integrated into upstream.


Remember, it is still a work in progress, still with many open questions to get feedback on.  Please shout out if you have a answer, see a potential security issue that isn't addressed, or have other input.


**First: Know your goal**
Before setting up a logging qube, you should determine your goal.  While logs can be great, if your goal is maximum privacy, and your never going to look at the logs anyway, then you might be best off having no logs at all.

However, many people will want logs for one of the following reasons:

1. Debugging.  Using logs to figure out why things aren't working so they can fix it.
2. Forensic analysis.  Trying to figuring out if a qube was comprimised whenever they suspect it has been.  This adds the additional potential complication of trying to figure out if the logging qube itself has been comprimised letting a attacker alter the logs that you are using to try to determine if there was a comprimise.

Now that you know why you want logs, you are ready to make decisions relating to them and we can move on to how to set up a logging qube


**Install qubes.Syslog file**
*(Note: You only need to do this if the patch has not been integrated upstream and distributed out through the normal update mechanisms yet.)*
* Start the template that the qube that will collect the logs will use as its template.
* Copy the file to https://github.com/QubesOS/qubes-core-agent-linux/blob/009e973b1eb3bbb14df59a25bf52a31d5f5f5043/qubes-rpc/qubes.Syslog to be /etc/qubes-rpc/qubes.Syslog in the template.
* Turn off that template

As stated before, if it has been integrated upstream and you are up to date, then the file wil already be there, and this step is unnecicary.

**Setting up your templateVMs to log to the sys-log logVM**
You need to do this for each template that you want all the appVMs that use that template to send logs to sys-log:
1. Make sure rsyslog is installed in the template.
    - it should already be installed in debian based distributions, but if you want to check, you can with: `apt-cache policy rsyslog`.  If it's not there, you can install it in debian with: `apt-get install rsyslog`
    - You can install it in fedora based distributions with:  `dnf install rsyslog`
    - Windows:  one option is: `choco install nxlog`
2. Configure rsyslog by modifying your rsyslog configuration file at  /etc/rsyslog.d/qubes_syslog.conf as described at [https://github.com/QubesOS/qubes-core-agent-linux/blob/009e973b1eb3bbb14df59a25bf52a31d5f5f5043/qubes-rpc/qubes.Syslog#L50-L67 ](https://github.com/QubesOS/qubes-core-agent-linux/blob/009e973b1eb3bbb14df59a25bf52a31d5f5f5043/qubes-rpc/qubes.Syslog#L50-L67)
except in the line, ```binary="/usr/sbin/runuser -u user -- /usr/bin/qrexec-client-vm work qubes.Syslog"``` ,
 change `work` to `sys-log` so it looks like: 
```binary="/usr/sbin/runuser -u user -- /usr/bin/qrexec-client-vm work qubes.Syslog"```
(side note: it should be possible to add a copy of this section pointed to sys-log-local to allow 2 seperate logging systems)
3. Then shut the template down and reboot any qubes you want to be using it.

4. TODO: Add instructions specific windows instructions for configuring nxlog?

5. TODO: We haven't mentioned getting logs from dom0 yet, which would be a important one.

**WARNING: Make sure your system will still be able to boot!**

If you have added logging to the templates for the sys-net and sys-firewall qubes, then when you boot up, they will generate a significant amount of traffic which will get logged (more then 10000 lines each).  
The system will automatically try to boot sys-log, so all sounds fine.  
However during boot time, many other things are going on (for example the sys-net and sys-firewall qubes starting).  This can slow down the system.  
If it slows it down enough so that it takes longer then 60 seconds to boot the sys-log qube, qrexec will kill the sys-log qube, and immediately try launching a new bootup of the sys-log qube, which causes new system load, and starts a infinte loop.

Depending on the speed of your system, and how many things you configure in your auto-boot sequence(including possibly more the one sys-log qube), this may be a problem or not.

There are 2 precautions to take:
1. Make backups of everything before you complete your logging configurations
2. Change the timeout for all qubes with:
```qubes-prefs default_qrexec_timeout 600```
or change the timeout for individual qubes with `qvm-prefs`


**Setting up a sys-log qube to collect all the logs**
1. Create a sys-log qube with networking: Example (typed from dom0): 
   ```
   qvm-create --template debian-10 --label-purple --property netvm=sys-firewall --property provides_network=True sys-log
   qvm-tags sys-log add collects-logs
   ```
   Or Create a sys-log-local qube with no networking:  Example (typed from dom0):
   ```
   qvm-create --template debian-10 --label-purple --property netvm=none --property provides_network=True sys-log-local
   qvm-tags sys-log-local add collects-logs
   ```
(Note: you could do both.  A thread has been made for discussing [if there is a benefit to doing both](https://forum.qubes-os.org/t/what-risks-do-we-add-to-a-qube-by-enabling-sys-firewall-networking-instead-of-none/6649https://forum.qubes-os.org/t/what-risks-do-we-add-to-a-qube-by-enabling-sys-firewall-networking-instead-of-none/6649)  )
Alternatives:  
    * you could create it as a standalone qube instead of a AppVM that uses a template

   Notes: 
   * We are basically checking the "provides network" box for the new qube, even though the qube does not provide networking, (or if creating sys-log-local does not even *have* networking. That checkbox is what determines if the qube is classified as a "service" qube in the menu or not.)
Note: While rsyslog is not strictly necessary for the logVM, you probably will want to use it.

2. If sys-log is using a template you just added the rsyslog configuration to, then you probably need to disable the /etc/rsyslog.d/qubes_syslog.conf file or it could create a feedback loop. :)   (we could put here a explanation on how to disable it via /rw bind)
2. Set the qubes policy in dom0 by creating a file at `/etc/qubes-rpc/policy/qubes.Syslog` containing:

    ```
    sendingVM receivingVM allow
    ```
   (Other options:  If your planning to log all qubes, you could do: 
   ```
   sys-log sys-log deny
   @tag:collects-logs sys-log deny
   @anyvm sys-log allow
   ```
or  if your just testing, you could do: `@anyvm @anyvm ask`)


4. Test it!  Generate some logs in the sending VM by typing `logger "hello world"` in a appVM that has been rebooted and is using your new modified template.  Then notice that the message can be observed in the `journalctl -b0` of the sys-log qube!
5. The logs in sys-log will still disappear after it reboots, so now we make the configuration and logs persistent
   - do: `sudo mkdir -p /rw/config/qubes-bind-dirs.d`
   - do:  `sudo nano /rw/config/qubes-bind-dirs.d/50_user.conf`
   - add this line: 
       ```
       binds+=( '/var/log' )
       binds+=( '/run/log/journal' )
       ```
6. Networking options:
* If you are not going to forward the logs to a external logging system, then instead of a sys-log qube, you could make a sys-log-local qube that has no networking.
* If you are going to forward the logs but are concerned about the logging qube being attacked *from* the network, then you could create both sys-log with networking, and sys-log-local that has no networking.


**OPTIONAL: Configuring a secondary external log outside of dom0**
If dom0 is ever compromised, then we should expect sys-log to be compromised.
If sys-log is ever compromised, weather via dom0, or via another method, then the attacker can go back in time in the logs to the old logs that showed the compromise when it happened, and change them to cover up the compromise.
Having a logging system outside of dom0 gives us a opportunity to have a copy of the logs that have the potential to keep a untained copy of a dom0 compromise.
Note that sys-log reads data from every qube.  This seems like a possible attack vector.  While they try to mitigate that potential in the patches, it seems like a possible attack vector that can't be eliminated while still being functional.  Also note that this same data will get forwarded to the external log.

A completely separate reason for having a external log is that if you have more then one qubes system, you can have that one external log aggregating all the logs from all the qubes systems in one place.

*Sending the logging traffic from sys-log:*
Sending the logging traffic from sys-log can be as easy as editing the /etc/rsyslog.conf file on sys-log and adding 
```*.*      @{ip address of your external log collector}```
This is the simplest configuration that will copy all logs from sys-log to that remote system.  They will be forwarded unencrypted.
(TODO: talk about setting up encryption)

*Set up a external computer to recieving the logging traffic coming from sys-log:*
1. Options:
1.a Set up a normal computer with a linux distribution other then Qubes (actually Qubes is more of a xen distribution, but that's beside the point).  Recommended distributions.  Debian is normal.  Would we want to advise a security oriented distribution?  Also mention that BSD is fine to install, but most people are probably not familiar with it.
1.b Set up another computer with Qubes on it.  (would require pointing to a guide for opening up listening ports to the outside world for a qubes qube)  (hardware that can run Qubes 4.0 is valuable enough to a Qubes user that it'd probably be getting used for Qubes.   possibly discuss potential issues with using that qubes system for logging *and* for other things?)
1.c Set up a raspberry pi.  (Depending on the traffic generated (which depends on *how many* qubes computers you have pointed at it), it's possible that not all raspberry pi models can handle the traffic, so maybe some kind of guidance on that?).  Guidance on operating systems?  Recommended distributions?  Standard is raspbian (now renamed to something else), which is a mangled version of debian. Recommend a distribution more security oriented?  (Also, if you don't feel Qubesy enough running a raspberry pi note that xen supposedly works fine on raspberry pi nowdays)
2. install rsyslog on it
3. TODO: explain how to set up rsyslog to allow receiving from the IP address of the qubes system
4. TODO: add SSL to explanation


**Configuring a queryable database**
* Depending on if more then one qube can receive a copy of the logs, address if this should be yet another separate logging qube?  
* TODO: explain how to set up rsyslog to save the logs in a database
* possibly recommend querying interfaces?
* address the database both as being a qube, and as the possibility of being a external copy



**OTHER:**
* Maybe mention setting up retention policies of the logs?  Maybe just find a external document for that and point to it?
* Find guides about how to do debugging under qubes, and point those documents to this?
* Find guides about doing forensic analysis when you suspect one or more qubes may have been compromised (I.E. some kind of "what to do if you suspect you may have been hacked" type article), and point those documents to this (with the caution that you need to set up the logging *before* the incident happens)



**Significant open questions:**
 - Should we recommend some specific security oriented operating systems for external logging (either amd64 or raspberry pi operating) instead of a normal one?