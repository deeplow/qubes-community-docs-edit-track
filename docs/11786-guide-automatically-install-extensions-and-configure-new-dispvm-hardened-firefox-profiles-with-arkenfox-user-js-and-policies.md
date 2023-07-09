This was inspired by a number of posts that sometimes pop up on the forum.

**Section 1** explains how to use arkenfox's (but you can use any other) `user.js` file (https://github.com/arkenfox/user.js) and make it compatible with Firefox autoconfig, in order to automatically configure new dispvm (or appvm) profiles without first creating one (so no profile-name fingerprinting).

For more information, see https://support.mozilla.org/en-US/kb/customizing-firefox-using-autoconfig.

It may help to know that this works well with Firefox policies.
Policies can complement what is defined by the `autoconfig.js` file. You can easily install (and remove) extensions, as well as toggle other parameters. The how-to can be found in **Section 2**, but for all the available parameters you are encouraged to read the official page: https://github.com/mozilla/policy-templates. 

# Section 1: Autoconfig

### 1. Download arkenfox's user.js:
```
[user@disp1234 ~]$ curl --tlsv1.2 -L https://raw.githubusercontent.com/arkenfox/user.js/master/user.js -o /home/user/user.js
[user@disp1234 ~]$ qvm-copy /home/user/user.js
```
In the prompt, select your Firefox's **TemplateVM** (in this example `deb-11-firefox`)


#### Notes: 
1. run all of the following commands in Firefox's **TemplateVM**.
2. take note of the dispvm name, you will need to change it in the following section (in this example `disp1234`).

### 2. Adapt user.js into firefox.cfg
user.js files don't work by default because they have some slight differences. We will solve that in this step:
```
[root@deb-11-firefox ~] export firefox_cfg="/usr/lib/firefox-esr/firefox.cfg"
[root@deb-11-firefox ~] export user_js="/home/user/QubesIncoming/disp1234/user.js"
[root@deb-11-firefox ~] echo "// IMPORTANT: Start your code on the 2nd line" > $firefox_cfg
[root@deb-11-firefox ~] cat $user_js | grep "user_pref" | grep -v "// user_pref" >> $firefox_cfg
[root@deb-11-firefox ~] sed -i 's/user_pref/pref/g' $firefox_cfg
```
Note: if you have a `user-overrides.js` that you'd like to use, simply re-run the last `cat` command (**before** running `sed`), but instead of `$user_js` include the path to your `user-overrides.js` file.

### 3. Create autoconfig.js
```
[root@deb-11-firefox ~] export autoconfig_js="/usr/share/firefox-esr/browser/defaults/preferences/autoconfig.js"
[root@deb-11-firefox ~] mkdir -p /usr/share/firefox-esr/browser/defaults/preferences
[root@deb-11-firefox ~] echo 'pref("general.config.filename", "firefox.cfg");' > $autoconfig_js
[root@deb-11-firefox ~] echo 'pref("general.config.obscure_value", 0);' >> $autoconfig_js
```

### 4. Clean up and shut down the template
If you have anything else other than `user.js` in QubesIncoming, don't run the first command (or do, if you want to remove it).
```
[root@deb-11-firefox ~] rm -r /home/user/QubesIncoming
[root@deb-11-firefox ~] unset autoconfig_js firefox_cfg user_js
[root@deb-11-firefox ~] shutdown -h now
```

# Section 2: Policies

### 1. Define your policies:
This part is very subjective so you should consider what you personally need. If you want to start from scratch, you should open a text editor in a vm and begin writing a `policies.json` file structured as follows:
```
{
    "policies": {
        <your policies go here>
    }
}
```
Then head over to https://github.com/mozilla/policy-templates and find what's important to you. You will see that for each policy, implementations for different OSs are provided: you need to scroll to the end of each policy until you find the `policies.json` section, then copy the key-value pair and insert it in the template shown above.
If you don't know what you're doing, you can paste your code in one of many json validators, such as https://jsonlint.com/, in order to see if you've made any mistakes.

Below, I provide a **very minimal** `policies.json` file which will disable a few things (telemetry, studies, Pocket), reject cookies, enable fingerprinting protection, install two extenstions (NoScript, Ublock origin), add Startpage engine, uninstall non-privacy friendly search engines, block access to location data, and replace the welcome screen (usually shown for new profiles) with a plain homepage with a search-bar:

```
{
    "policies": {
        "Cookies": {
            "Behavior": "reject-tracker-and-partition-foreign",
            "ExpireAtSessionEnd": true,
            "Locked": false
        },
        "DisableFirefoxStudies": true,
        "DisablePocket": true,
        "DisableTelemetry": true,
        "EnableTrackingProtection": {
            "Value": true,
            "Locked": true,
            "Cryptomining": true,
            "Fingerprinting": true
        },
        "ExtensionSettings": {
            "*": {
                "installation_mode": "blocked"
            },
            "{73a6fe31-595d-460b-a920-fcc0f8843232}": {
                "installation_mode": "normal_installed",
                "install_url": "https://addons.mozilla.org/firefox/downloads/latest/noscript/latest.xpi"
            },
            "uBlock0@raymondhill.net": {
                "installation_mode": "normal_installed",
                "install_url": "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
            }
        },
        "FirefoxHome": {
            "Search": true,
            "TopSites": false,
            "SponsoredTopSites": false,
            "Highlights": false,
            "Pocket": false,
            "SponsoredPocket": false,
            "Snippets": false,
            "Locked": false
        },
        "HardwareAcceleration": false,
        "Homepage": {
            "URL": "about:home",
            "Locked": false,
            "StartPage": "homepage"
        },
        "OverrideFirstRunPage": "about:home",
        "Permissions": {
            "Location": {
                "BlockNewRequests": true,
                "Locked": true
            }
        },
        "SearchEngines": {
            "Add": [
                {
                    "Name": "Startpage",
                    "URLTemplate": "https://www.startpage.com/sp/search?query={searchTerms}",
                    "Method": "GET",
                    "IconURL": "https://www.startpage.com/sp/cdn/favicons/favicon--dark.ico",
                    "Alias": "@startpage",
                    "Description": "Startpage",
                    "SuggestURLTemplate": "https://www.startpage.com/sp/search?query={searchTerms}"
                }
            ],
            "Remove": [
                "Amazon",
                "Bing",
                "Google",
                "Twitter",
                "Wikipedia",
                "Yahoo"
            ]
        }
    }
}
```


Also note that the following policy will block the installation of additional addons:

```
"*": {
    "installation_mode": "blocked"
}
```
If you want to install addons after the browser profile has been created, you need to remove that policy. Otherwise you can enable additional addons like I did with ublock and noscript, by setting `installation_mode` to `allowed`.

### 2. Enable your policies:
Start your firefox template (for example `deb-11-firefox`) and place the json file in `/usr/lib/firefox-esr/distribution/policies.json` (make sure to replace `/PATH/TO/SAVED/policies.json` with the actual location of the file you made):
```
[root@deb-11-firefox ~] mkdir -p /usr/lib/firefox-esr/distribution
[root@deb-11-firefox ~] cat /PATH/TO/SAVED/policies.json > /usr/lib/firefox-esr/distribution/policies.json
[root@deb-11-firefox ~] shutdown -h now
```

### 3. Remove existing profiles from the dvm-template:

To avoid profile fingerprinting, make sure there are no profiles in your dvm-template. To remove them, run the following:
```
[user@deb-11-firefox-dvm ~] rm -r /home/user/.mozilla
[root@deb-11-firefox-dvm ~] shutdown -h now
```

All done!