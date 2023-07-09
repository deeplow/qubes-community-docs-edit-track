Now I managed to make the whole thing together.
If you "keep all your passwords strictly offline", just stop reading. For the rest of us.

First, I divided the passwords to 3 categories:
1. "**high security**". The security requirement is defining, so we need to sacrifice some availability here.
2. "**domain-specific**". These passwords are needed within a specific context and typically may reside there.
3. "**accessible**". For these passwords, accessibility requirements are more important than security.  JFYI, I see almost everything that is properly (properly means excluding SMS) protected by a second factor may fall into this category unless it is already classified as 1 or 2.

For **high security** passwords (and this may include not just passwords, but TOTP keys as well) I do not think KeepassXC is a good fit at all. Most of its features will remain unused, including GUI, and I would consider some of it even dangerous. [**pass + pass-otp**](https://www.passwordstore.org/) looks like a better fit.

For **domain-specific** passwords again, there is no need in advanced solutions. The most obvious way to manage is to keep them in the browser keychain of the according Qube. Even it gets compromised, the impact is going to be limited.

Now, the interesting part. How to set up single KeepassXC backend to make "**accessible**" passwords available from any Qube (maybe not *any* any, but most of general purpose ones which are not strictly domain-specific or compartmentalized due to elevated threat).

1. "**vault**" setup. It is not exactly vault, because most likely you want it to be accessible not just from your Qubes system, but from your other devices as well, so it is going to be networked and synced (or not if you do not wish to, I do not insist). This is mostly typical passwdXC installation within a Qube, with one extra thing: we want to make the keepassXC socket available to remote clients. To get this, we need to make it sure that keepassXC set to autostart in desltop environment, and a service is created as /etc/qubes-rpc/qubes.keepassXC:

```
#!/bin/sh
notify-send "[`qubesdb-read /name`] KeepassXC access from: $QREXEC_REMOTE_DOMAIN"
ncat -U /run/user/1000/org.keepassxc.KeePassXC.BrowserServer

```

Please note that in template-based installation the file does not presist over Qube restarts. You need to either put it on the template or re-create it every time with rc.local. Don't forget to make it executable.

2. **dom0** setup. That's easy, all you need is a regular polcy in /etc/qubes/policy.d/30-user.policy (whatever your vaultvm is, or you may replace "ask" with "allow" if you are confident enough):

```
qubes.keepassXC   *   @anyvm vaultvm  ask target=vaultvm
```

3. **client** setup. First, you need keepassxc to be installed in all that templates as well, because you need a binary component named keepassxc-proxy. Then you need to define a few things: first. the **extension itself**. You may install it manually to each user, or just place the **keepassxc-browser@keepassxc.org.xpi** file to **/usr/share/mozilla/firefox/extensions**. Second, the **messaging host** reference to let the browser communicate to the proxy, the ```org.keepassxc.keepassxc_browser.json``` file. 
```
{
    "allowed_extensions": [
        "keepassxc-browser@keepassxc.org"
    ],
    "description": "KeePassXC integration with native messaging support",
    "name": "org.keepassxc.keepassxc_browser",
    "path": "/usr/bin/keepassxc-proxy",
    "type": "stdio"
}
```

Put it either to .mozilla/native-messaging-hosts per user, or to /usr/lib64/mozilla template-wide. Third, the **forwarder service**. You need to run
```
/usr/bin/ncat -k -l -U /run/user/1000/org.keepassxc.KeePassXC.BrowserServer -c "qrexec-client-vm vaultvm qubes.keepassXC"
```

in every client Qube, under user privileges. You may define a user systemd service, or a desktop entry.

Did not test with Chromium but should work in a similar fashion.