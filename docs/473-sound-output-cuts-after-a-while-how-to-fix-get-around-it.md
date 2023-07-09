When I play anything sound plays for 5 seconds (sometimes a minute if I'm lucky) and then it cuts off making a "th" sound. I've had this issue with Arch and Solus too and can't seem to get around it. I tried:
*  I put the following in /etc/asound.conf
```
defaults.pcm.card 0
defaults.pcm.device 0
defaults.ctl.card 0
```
* I put the following in /etc/modprobe.d/alsa-base.conf
```
options snd-hda-intel model=auto
```
I don't think these are related though. I don't have a problem of not seeing the device. Someone told me that "cache is filled then not refilled when depleted" which I have no idea how to fix. It used to be that I would just use my headphones but now my audio jack is broken (quite literally).