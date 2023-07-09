Introduction
-

I have some applications, that run in the browser but I don't want Firefox to remember all my passwords and history. 
Some apps are in external repositories and installing them in Qubes OS needs special workaround but browser bars fills important space... 

Here's the solution, you'll tweak Firefox to looks like normal app  :slight_smile:

Requirements
-

So, let's say, you have separated appVM where is firefox, and you set you homepage to site which'll become your webapp.

Method 1 - Addons
-
*(Easiest, may not work for some sites)*

1. go to addons.mozilla.org and install [Popup window](https://addons.mozilla.org/en-US/firefox/addon/popup-window/) and [Web App mode](https://addons.mozilla.org/en-US/firefox/addon/web-app-mode/) 
 
2. Go to options ==> Extensions ==> Web App Mode settings ==> add your homepage site with wildcard to sites that will automatically start in this mode.

3. Test if it works by reopening Firefox (there is no need to restart appVM)

**Note:**
If something  crashes, then while firefox starts, quickly type CTRL+T to open new tab which will stay in default mode, where you have options

Method 2 - Firefox SSB
-
Read about this method [here](https://www.reddit.com/r/firefox/comments/f3ikwj/how_to_enable_web_apps_in_firefox_like_chrome/)

Method 3 - Firefox Profiles
-

Read about this method [here](https://www.reddit.com/r/firefox/comments/f3ikwj/how_to_enable_web_apps_in_firefox_like_chrome/)

*I tested only the first method but feel free to discuss about every you know/tested on Qubes* :slight_smile: