This is a followup to [this question](https://forum.qubes-os.org/t/qubes-users-howto-grab-capture-sound-of-one-vm/2804). Since I'm not on the mailing list, maybe someone else can reply to that question with a link to this description.

=====

What we want to achieve: record audio output of qube A in qube B.

All instructions should be executed in dom0.

1. Run `sudo modprobe snd_aloop`

2. In `pavucontrol`, in the "Playback" tab, change the output for A to `Loopback Analog Stereo`.

3. In `pavucontrol`, in the "Recording" tab, change the source for B to `Monitor of Loopback Analog Stereo`.

4. Attach the microphone to qube B via either the applet in the system tray or using `qvm-device mic` in the command line.

The audio output of A should now appear as the microphone input in B.