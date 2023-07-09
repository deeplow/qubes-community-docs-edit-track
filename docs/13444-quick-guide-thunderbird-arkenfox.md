Hello all,
There is a great guide on using the arkenfox user.js within a disp on [this forum.](https://forum.qubes-os.org/t/guide-automatically-install-extensions-and-configure-new-dispvm-firefox-profiles-with-arkenfox-user-js-and-policies/11786) I now do all my daily browsing in a disp thanks to this. However, I haven't seen anything for mail. Here is a modified user.js you can use with Thunderbird to improve your security/privacy. It's based on arkenfox.

https://github.com/HorlogeSkynet/thunderbird-user.js/wiki/1.3-Implementation
Just  copy the user.js to your ~/.thunderbird/<user.account.folder-default> 
replace <user.account.folder-default> with your subfolder for your account.
Make any changes to the user.js to suit your needs.

If you are using R.1 you could use it along side the open-with-dvm service to open all your attachments in a disp.