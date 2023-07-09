For the best practice of anonymity, it's good to sync AppVM's system time zone to wherever the timezone of the VPN server is connected to. During Qubes 3.0 days, I remember Fedora VM used to sync its timezone automatically by simply turning on the Automatic Time Zone in the Settings but that perk was long gone after I believe some kind of new rpc policy on clocksync was introduced. Ever since then, I've been changing the sys timezone manually from the Settings. 

I have basically two questions.

1. Is there a way to automatically sync VPN server's time zone in an AppVM?

2. When an AppVM turns on, is there a way to start off with random time zone?