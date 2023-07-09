Hey everyone this isn't necessarily a guide, more of a little solution I discovered yesterday night after a couple glasses of donjulio and thought it might help out some people who are looking to run i2p on qubes/whonix like the good old days.

Just install one of the i2pd packages from their github repo, I installed it using 'dpkg --install'

then instead of running 
```
sudo dpkg-reconfigure i2pd
```
to make it run automatically at boot just use
```
sudo systemctl enable i2pd
```
Now that's done I made it run for 2 mins in case it needed to create the necessary config files like the java version.
```
sudo systemctl start i2pd
```
```
sudo systemctl stop i2pd
```
after that I edited the config file i2pd.config that can be found in the `/etc/i2pd` (or something like that, should be there somewhere in /etc/)
the only thing I edited was the max bandwidth and the address of the http webconsole to 127.0.0.2:7070 (basically just changed its IP to 127.0.0.2).

I then just followed the [whonix wiki to setup tor for I2P](https://www.whonix.org/wiki/I2P), currently there is one adjustment to be made different from the wiki: instead of putting `127.0.0.2` under `network.proxy.http` you should put `127.0.0.1` 
And put `127.0.0.2` under `network.proxy.no_proxies_on` so that the browser lets you connect to the webconsole without trying to route the connection through I2P. 

And that's done! Just tweak the other settings of torbrowser just as in the [wiki](https://www.whonix.org/wiki/I2P) and you should be good to go.

P.S.
This guide is really generic since I've done this thing on a standaloneVM just to make things quicker, I'll try and adapt everything to the qubes environment whenever the lazyness goes away.
Also please let me know all the things that are wrong with this setup! I've been using qubes for a long while but I'm not really knowledgeable about anything regarding linux or networks so please let me know!
Bye Bye