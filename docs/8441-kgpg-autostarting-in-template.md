I am running the KDE desktop manager and recently installed Kgpg in a Debian template.  To my surprise, after installing the package and later starting the template to update, a Kgpg window popped up.   Kgpg autostarted in the template.  :/  It seems that this is caused by a Kgpg default to autostart in Gnome.  To stop this from happening I modified:
```
/etc/xdg/autostart/org.kde.kgpg.desktop
```
I added the following line:
```
OnlyShowIn=KDE
```

Not sure if this option is available for those who have not installed KDE or how they might stop Kgpg from autostarting but you might try the above.

If Kgpg already autostarted in your template and you are especially paranoid, scrap the template, reinstall Kgpg and modify the above file before restarting the template to make sure nothing runs in the template.   I tend to clone my templates at various stages of modification to make "do-overs" a bit easier.  YMMV.