(Yeah, that's a geeky physics reference)

**Introduction/Rationale**

From what I've seen, there are two major enhancements to firefox or tor that get referenced a lot here (presumably that means they get used a lot, too).

My experience has been entirely with Firefox.  (I wish I could like tor, but it takes so ridiculously long to start it over my network...)  I hope this carries over to tor, for those who do use it.

[Edit to add:  Apparently, you don't want to combine Tor in any form with Arkenfox.  My source on this is unclear as to whether Tor+split browser is a bad idea.  However, RusyBird (the originator of split browser) does support both Tor and Firefox.]

**Hardening Based on Arkenfox**

The first is basically an elaboration of Arkenfox's work that is elaborated in https://forum.qubes-os.org/t/guide-automatically-install-extensions-and-configure-new-dispvm-firefox-profiles-with-arkenfox-user-js-and-policies/11786/60 .  

Arkenfox, as originally conceived (and I may be misreading this), sets up a preference file that is persistent between firefox runs...it gets copied into the runtime preferences when you start Firefox, and any settings you change during a session won't "stick" and be around the next time you run Firefox.  Arkenfox, however, wasn't thinking in Qubes, and given that we have disposable virtual machines it's possible to go one better on him.  That is what @BEBF738VD did.

In essence, the Arkenfox user.js preference settings are added to a template with a fresh install of firefox in such a way that when you start an appvm (or disposable) based on that template, it's as if you were running firefox for the first time...but the default settings are now what you want.  BEBF738VD's work also includes instructions on how to add a policy to the installation.  (You need a policy to actually set the default browser; it cannot be done through prefs.  A deliberate design decision by Firefox.)  

[Incidentally, when you run Firefox for the very first time, it creates a "profile" with a random, gobbledygook name, which becomes your profile in subsequent runs...and it's distinguishable.  By doing things this way a different profile name is generated every time you run the browser because on a DVM every run is the *first* run.]

The BEBF738VD thread gives directions on how to do all this, and you have opportunities to set things up to use a subset of Arkenfox's settings or to add more to them.  (I did the latter, to configure the Firefox UI in a way more to my liking.)  The Arkenfox file itself is well commented and organized topically, so it's fairly easy to find settings you don't care about (or which break something online) and remove them.  After doing that they are translated into a different format and placed in an area Arkenfox himself didn't envision, so that they become the default prefs when you start firefox for the first time (well, the first and last time in the life of that particular DVM).  In fact I have three distinct copies of the original Arkenfox user.js file, one with basically everything in it, the other two with fewer and fewer Arkenfox settings actually enabled.

Some argue that this treatment is pointless, at least for Firefox, because Arkenfox emphasizes fingerprinting resistance and really the best way to accomplish that is through Tor.  But there is a lot more to Arkenfox's settings than just fingerprint resistance (though I kept that part in all three versions), so even if you think the fingerprinting is pointless, it's still worth checking out.

The big disadvantage of this is, you have no bookmarks.  You could import them, of course, but that involves copying files, doing the actual import...and a hacker could conceivably capture your bookmarks...all of them...unless you go to the trouble of maintaining separate sets of bookmarks, which multiplies the pain-in-the-hindquarters factor greatly.

**Bookmarks from Split Browser**

The *other* popular enhancement to browsers is split-browser,   There are a number of threads on this topic, but the best starting place is here: [GitHub - rustybird/qubes-app-split-browser: Tor Browser (or Firefox) in a Qubes DisposableVM, with persistent bookmarks and login credentials](https://github.com/rustybird/qubes-app-split-browser) as @RustyBird has written good instructions.  (NB:  there seems to be an issue with this on Fedora so you may want to consider the "or install manually" directions if that gets in your way.)

The idea here is to create an AppVM where your bookmarks are stored, and use that AppVM to launch disposable browsers (the default-dispvm for that AppVM should point to the VM with the browser installed).   Installation happens on both the bookmark-holding AppVM and the browser DVM template.  Once installed the only thing you actually do on the bookmark AppVM is use it to launch browsers.  You go to the browser and look up bookmarks with Alt-B (which tells the bookmark AppVM to pop up a window to let you select a bookmark, then the AppVM sends the bookmark to the browser, which opens in a new tab).  Also the browser lets you save bookmarks, these are sent to the bookmark AppVM which puts them in the bookmarks file for future use.  (There is a capability to manage passwords, too, but I haven't tried it yet so I can't summarize it.)

So this has the bookmarks, *and* those bookmarks are controlled elsewhere so someone who hacks your browser qube can't steal them all.  And the fact that the browser runs in a disposable means bookmarks you used previously aren't there any more.

The problem with this is you get a bonestock Firefox install, complete with obnoxious "welcome to Firefox" page and Firefox's default home page and the url bar sending your typos to google and...you name it.  In other words, this brings with it a lot of the problems you can solve with the Arkenfox+ described previously.

Wouldn't it be nice to combine these?  Hardening and customization of your Firefox browser *and* bookmarks which persist and are kept elsewhere?

Well, when I first installed split browser, I did it in a half-assed "Arkenfoxed" VM (I think I just put a user.js in the profile area).  And it did NOT work.  The prior quasi-arkenfoxing I had done prevented the keyboard shortcuts in split browser (which are vital) from working.  So basically it looked like the two couldn't be combined.

**The Grand Unified Browser (Best of Both Worlds)**

However, It turns out they **can** be combined.  And it's fairly easy!

Step One:  Install split browser as described in the github link above.  Do this with the browser side being a template with a fresh, never-used Firefox installation.  Verify it works by running the bookmark VM, using it to start a browser, and then, in that browser, saving a bookmark or two with ctrl-d, and getting the bookmark with alt-B.  (NB: split browser checks your new bookmark to ensure it's not a duplicate, so any additional bookmarks in your test must be distinct.)

Step Two:  Create your user.js file as given in the instructions I linked above.  I personally downloaded the latest version from Arkenfox's github, modified it, then added some more settings.  I then translated this (as described in BEBF738VD's instructions, into a firefox.cfg file.

Do NOT put this where described in those instructions.  Instead, append it to the file `/usr/share/split-browser-disp/firefox/sb.js` in your split-browser's browser template.  Please note I said "append."  *Don't replace, add to the end of the existing file.*  The existing file defines, among other things, the keyboard shortcuts that underpin split browser; if you destroy those, you don't really have a split browser any more.

[Alternative:  instead of appending to sb.js in the split browser's browser template, place this file in the *bookmarks* AppVM in `/etc/split-browser/prefs`.  But name it `50-user.js`.  This method allows you to alter the preferences without having multiple templates for the browser since this file gets copied over to the browser VM when it starts up.  You can swap different versions of this file depending on how much (or how little) Arkenfox+ you want in the browser, right before starting the browser.  This can be automated by writing scripts to copy a specific version of 50-user.js to that location and then run browser-start; each of these scripts can be referenced by a different .desktop file if you like calling things up from desktop shortcuts or the main Qubes menu.]

Step Three:  Copy your policies.json file (if you have one) from your "Arkenfox+" setup, to `/usr/lib/firefox-esr/distribution`.

That's it...the next time you run the split-browser browser, it should look exactly like your arkenfox+ browser...because it essentially *is*.  But you have access to your bookmarks that are kept on your bookmarks AppVM.

OK, so there's still some stuff missing...there's no pre-canned solution for importing bookmarks into split-browser from one of those .html bookmark export files.  But that was true before, too.  Also it'd be nice if the bookmarks could be subdivided into folders...well, I think it would be nice, perhaps most people don't care about that.  But these are both characteristic of what's already there; they are not *new* limitations of the Grand Unified Browser.  (And as it happens, I am working on both of them.)

I hope that both @RustyBird and @BEBF738VD see this and read it and tell me if there are any gaping holes--especially with respect to security--with this concept.