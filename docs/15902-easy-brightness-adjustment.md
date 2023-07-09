Ive spent quite a while trying to figure this out and just wanted to pass it on.

Click Q in top left corner and open "Terminal Emulator" 

in Terminal type

xrandr -q

you will get a print out resembling this

Screen 0" minimum blah blah current blah blah 
**HDMI-1** connected primary blah blah
   numbers
   numbers
   more numbers
DP-1 disconnected blah blah
HDMI-2 disconected blah blah

What you want is the bold part. The connected primary.

you then type

xrandr --output **yourConnectedPrimary-whatever** --brightness desiredBrightnessIndecimalForm

For me I went with 50% brightness writen as 0.5. 0.8 would be 80%, 0.75 for 75% ect ect. My example looks like this

xrandr --output HDMI-1 --brightness 0.5

then hit enter

and you are done.

I assume, which I know is dangerous with Linux, that if you have multiple displays you can set them the same way just modify the connected primary for whatever secondary displays or ports you are working with. Good luck and best wishes!