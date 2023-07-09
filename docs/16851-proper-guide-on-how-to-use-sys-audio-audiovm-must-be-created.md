# Problem 

Currently no **proper guide** exists on how to create and use `sys-audio` (AudioVM) in R4.1/R4.2.

* Qubes OS Documentation **does not have a single article** about it.
* Qubes Community Documentations also has **nothing** at all about it.

# Consequences

So many people are trying to create `sys-audio` qube to listen to Bluetooth headphones and almost nothing helps or guides them except several forum topics which **are mess**: full of different information combined with useless, outdated or random messages on different topics. Almost nobody can set `sys-audio` to work properly in full.

# Solution proposal

So, I am asking people who is savvy enough or/and have a properly working sys-audio to:
1) Provide a detailed, up-to-date step-by-step guide how to create and set a sys-audio qube for having sound in it from the very beginning. Majority of steps should have an explanation of what (and why) is happening and how to test that the result of the step is right (check with aplay, reboot and check processes, look for something in pavucontrol and etc).
2) Explain how exactly the sound data should be moved by qubes tools by design for future Qubes OS versions that will include sys-audio be default similar to how sys-usb is used nowadays.
3) Provide a guide how to use Bluetooth headphones in this sys-audio qube to play sound in headphones.
4) Provide a guide how to make the sound work in Windows qubes too (currently this topic is even messier, some patches of qemu and etc).


Let's hope that someone (or multiple users) will try to do this important job for the greater good of others. It will be very appreciated.
I can make such guides myself but currently I am not able to set `sys-audio` for myself, facing multiple issues and lack of straight-forward information on the topic.

# Links to information on the topic that I think can be useful

* A short mention of sys-audio as a future for Qubes OS on official site:
https://www.qubes-os.org/news/2020/03/18/gui-domain/#audio-domain

* Current salt (automation script) for creating sys-audio (by far not enough to make anything work):
https://github.com/QubesOS/qubes-mgmt-salt-dom0-virtual-machines/blob/master/qvm/sys-audio.sls

* Other official audio salts that are not explained anywhere can be found here:
https://github.com/QubesOS/qubes-mgmt-salt-dom0-virtual-machines/tree/master/qvm

* The best guide that I could find at the moment by @hamenarin (but not full, not working for me and misses explanations)
https://forum.qubes-os.org/t/setting-up-an-audio-vm/5491/24

* User @SteveC follows the guide by @hamenarin adding useful information (but no success)
https://forum.qubes-os.org/t/setting-up-an-audio-vm/5491/31

* An outdated article about using "Bluetooth headset with Qubes" – Linux Administration
https://linuxadministration.us/bluetooth-headset-with-qubes/

* A guide of using debian-minimal modification for sys-audio by @dom0
https://forum.qubes-os.org/t/debian-minimal-template-for-sys-audio/11108/47

* Workaround with starting and stopping sys-audio 3 times in a row to make it work (devs should explain the reason!) by dom0:
https://forum.qubes-os.org/t/debian-minimal-template-for-sys-audio/11108/61

* Article by u/stroberrysugar about (outdated?) way making audiovm via pulseaudio sinks manually:
https://www.reddit.com/r/Qubes/comments/tnib7k/guide_on_using_a_usb_audio_device_with_qubes_41/

* The previous approach of stroberrysugar extended by @enmus (is it an outdated approach?):
https://forum.qubes-os.org/t/guide-on-using-an-usb-audio-device-with-qubes-4-1/10748/3

* Old and small instruction by @kef
https://forum.qubes-os.org/t/setting-up-an-audio-vm/5491/15

* Fix of scratchy sound by @alte (should be a part of guide if it's still working and needed):
https://forum.qubes-os.org/t/setting-up-an-audio-vm/5491/23

* Probably useful information by @logoerthiner
https://forum.qubes-os.org/t/r4-1-audio-does-not-go-from-appvm-to-dom0-in-default-installation/9532/15

* About using sys-audio for Windows audio
https://forum.qubes-os.org/t/using-sys-audio-for-windows-audio/10416

* Windows-releated issue ticket:
https://github.com/QubesOS/qubes-issues/issues/2624

* Official docs on audio virtualization:
https://www.qubes-os.org/doc/audio-virtualization/


# Uses, who supposingly has expertise or/and experience on the topic is bellow.
All these users are especially encouraged to participate within this topic.

https://forum.qubes-os.org/u/enmus
https://forum.qubes-os.org/u/dom0
https://forum.qubes-os.org/u/hamenarin
https://forum.qubes-os.org/u/marmarek
https://forum.qubes-os.org/u/fepitre
https://forum.qubes-os.org/u/kef
https://forum.qubes-os.org/u/dpr
https://forum.qubes-os.org/u/augsch
https://forum.qubes-os.org/u/disp584
https://forum.qubes-os.org/u/logoerthiner