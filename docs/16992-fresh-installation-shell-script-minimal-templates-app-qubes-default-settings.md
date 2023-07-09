# Qubes OS - Fresh Install - Minimal templates
---
> :warning: **Caution:**
> Minimal templates are intended for advanced users.

[qubes-os.org/doc/templates/minimal/#important](https://qubes-os.org/doc/templates/minimal/#important)


## Introduction
---
> :warning: **Warning:**
> This script **IS NOT** made to be launch as it.
> You **must** configure it to your hardware and preferences.

As an advanced topic, some knowledge is assumed.

[details="e.g. usage of the manual pages."]
```bash
[user@dom0 ~]$ man man
[user@dom0 ~]$ man qvm-template
[user@dom0 ~]$ grep --help
[user@dom0 ~]$ qvm-clone -h
```
[/details]

[details="e.g. these bash concepts and commands."]
  - `for loop` and `if then`
  - function ( `$#`, `$1`, `$2`, `$@`, `${@:3}` )
  - recursive function  ( function that calls itself )
  - sed ( `'s/foo/bar/g'`, `'/^foo.*bar/ d'` )
[/details]

### description
A customizable shell script to automate your installation.

This is a recipe, not a tutorial / course.
Take some or all of it. Modify it to your needs.

This script is a one-file format (single `.sh` file).

### initial setup
[qubes-os.org/doc/installation-guide/#initial-setup](https://qubes-os.org/doc/installation-guide/#initial-setup)

[details="Select these checkboxes."]
  - Fedora XX
  - Create default system qubes (sys-net, sys-firewall, default DispVM)
  - Use a qube to hold all USB controllers (create a new qube called sys-usb by default)
[/details]

[details="Do not select these checkboxes."]
  - Make sys-firewall and sys-usb disposable
  - Make sys-net disposable
  - Create default application qubes (personal, work, untrusted, vault)
[/details]

### usage
  - disable hibernate and suspend during the script execution.
    `apps menu > system tools > power manager`

  - in `dom0` terminal.
    - enable unlimited scrollback (to check if an error occured after the installation).
    `menu > edit > preferences > general > unlimited scrollback`

    - copy the script to `dom0`, make it executable, then launch it.
    [qubes-os.org/doc/how-to-copy-from-dom0/#copying-to-dom0](https://qubes-os.org/doc/how-to-copy-from-dom0/#copying-to-dom0)
      > :warning: **Caution**:
      > The code you run in dom0 **MUST** be understood.

      ``` bash
      file_name=qubes_fresh_install.sh
      qvm-run --pass-io sys-usb "
          cat /home/user/$file_name" > $HOME/$file_name
      chmod +x $HOME/$file_name
      $HOME/$file_name
      ```

  - after reboot and working internet.
    > :bulb: Keeping the full template can be useful in many situations.
    [details="Remove the default qubes."]
    ```bash
    qvm-remove --force \
        default-mgmt-dvm \
        sys-usb \
        sys-firewall \
        sys-net
    ```
    [/details]
    [details="Remove the full template."]
     ```bash
    qvm-remove --force \
        fedora-XX-dvm \
        fedora-XX
    ```
    [/details]


## Update
---
[qubes-os.org/doc/how-to-update/#command-line-interface](https://qubes-os.org/doc/how-to-update/#command-line-interface)

```bash
#!/usr/bin/bash

if true; then ## update
echo 'updating templates ...'
sudo qubesctl --skip-dom0 --templates state.sls update.qubes-vm

qvm-shutdown --all --wait
qvm-start sys-net sys-firewall
qvm-start sys-usb

echo 'updating dom0 ...'
sudo qubesctl --show-output state.sls update.qubes-dom0
fi ## end: update
```


## Configuration
---
```bash
os_name=fedora
os_release=$(qvm-template list --available \
    | grep -Eo "$os_name.*minimal" \
    | tail -n 1 \
    | grep -Eo '[0-9]+')

install_cmd='dnf -y --setopt=install_weak_deps=false install'
```


## Packages
---
> :warning: **Caution:**
Before adding a third-party repository, make sure it is a known and trusted source.

[details="System"]
Use `lspci` and `dnf search` to find your wifi driver.
e.g. `dnf search wireless` or `dnf search CARD_MANUFACTURER`
```bash
wifi_driver='
    iwl7260-firmware
    iwlax2xx-firmware'

passwordless_root='
    qubes-core-agent-passwordless-root'
networking='
    qubes-core-agent-networking'
usb_proxy='
    qubes-usb-proxy'

default_mgmt="
    $passwordless_root
    qubes-mgmt-salt-vm-connector"
sys_network="
    $networking
    qubes-core-agent-network-manager
    network-manager-applet
    $wifi_driver
    NetworkManager-wifi"
sys_firewall="
    $networking
    qubes-core-agent-dom0-updates"
sys_usb="
    $usb_proxy
    qubes-input-proxy-sender"
```
[/details]

[details="Common"]
```bash
audio='
    pulseaudio-qubes'
file_manager='
    qubes-core-agent-thunar'
password_manager='
    keepassxc'
text_editor='
    mousepad'
image_viewer='
    eog'
pdf_viewer='
    qpdfview-qt5'
email_client='
    thunderbird'
office_suite='
    libreoffice-calc
    libreoffice-draw
    libreoffice-writer
    libreoffice-gtk3'
```
[videolan.org/vlc/download-fedora.html](https://videolan.org/vlc/download-fedora.html)
Do not use the `$(rpm -E %fedora)` command, it will return the `dom0` fedora version.
```bash
fedora_rpm_free=rpmfusion-free-release-$os_release.noarch.rpm
media_player="\
    https://download1.rpmfusion.org/free/fedora/$fedora_rpm_free \
    && $install_cmd vlc"
```
[brave.com/linux/#fedora-centos-streamrhel](https://brave.com/linux/#fedora-centos-streamrhel)
Add `--httpproxy 127.0.0.1 --httpport 8082` to the `rpm` command.
[qubes-os.org/doc/how-to-install-software/#updates-proxy](https://qubes-os.org/doc/how-to-install-software/#updates-proxy)
```bash
brave_rpm_www=https://brave-browser-rpm-release.s3.brave.com
web_browser="\
    dnf-plugins-core \
    && dnf config-manager \
        --add-repo $brave_rpm_www/brave-browser.repo \
    && rpm --httpproxy 127.0.0.1 --httpport 8082 \
        --import $brave_rpm_www/brave-core.asc \
    && $install_cmd brave-browser"
```
[/details]

[details="Work"]
[vscodium.com](https://vscodium.com) - Free/Libre Open Source distribution of VSCode.
[github.com/VSCodium/vscodium#install-with-package-manager-gnulinux](https://github.com/VSCodium/vscodium#install-with-package-manager-gnulinux)
```bash
vscodium_repo='
[gitlab.com_paulcarroty_vscodium_repo]
name=...
baseurl=...
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=...
metadata_expire=1h'
# --version is used to skip $install_cmd
code_editor="--version > /dev/null \
    && echo \"$vscodium_repo\" > /etc/yum.repos.d/vscodium.repo \
    && $install_cmd codium"
dev_tools='
    git
    vim
    zsh'
```
[/details]

[details="Misc"]
```bash
printer='
    system-config-printer
    gutenprint-cups'
qt_theme='
    adwaita-qt5'
qubes_converter_tools='
    qubes-pdf-converter
    qubes-img-converter'
```
[/details]


##  Templates
---
```bash
echo 'creating templates ...'
```
[details="run_cmd ()"]
```bash
run_cmd ()
{
    qvm-run --pass-io --nogui --user $1 $2 "$3"
}
```
[/details]

### 1. base
Install the minimal template, clone it to a custom name and update it.
```bash
base_tpl=$os_name-$os_release-min
min_tpl=$os_name-$os_release-minimal

qvm-template install $min_tpl
qvm-clone $min_tpl $base_tpl
qvm-remove --force $min_tpl

sudo qubesctl --skip-dom0 --targets=$base_tpl state.sls update.qubes-vm
```
[details="theme & icons"]
Copy your favorite theme & icons from `dom0` to the base template.
All folders of a theme must be copied (there are symbolic links between them).
```bash
themes_dir=/usr/share/themes/
icons_dir=/usr/share/icons/
qvm-copy-to-vm $base_tpl \
    $themes_dir/Arc* \
    $icons_dir/gnome

qubes_incoming=/home/user/QubesIncoming/
run_cmd root $base_tpl "
    mv $qubes_incoming/dom0/Arc* $themes_dir
    mv $qubes_incoming/dom0/gnome $icons_dir
    rm -r $qubes_incoming"
```
[/details]
[details="filetype association"]
Disable the mimetype for `qvm-open-in-dvm` (comment the mimetype line).
Disable the default `mimeapps.list` (rename the file).
```bash
system_apps_dir=/usr/share/applications/
open_in_dvm_entry=$system_apps_dir/qvm-open-in-dvm.desktop
default_mimeapps=$system_apps_dir/mimeapps.list
run_cmd root $base_tpl "
    sed -i 's/^MimeType=/#&/' $open_in_dvm_entry
    mv $default_mimeapps $default_mimeapps.bak"
```
[/details]
Clone the base template as a clean base for future use.
```bash
qvm-shutdown --wait $base_tpl
qvm-clone $base_tpl $base_tpl-bak
```

### 2. creation
[details="install_packages ()"]
```bash
install_packages ()
{
    for pkg in "${@:2}"
    do
        echo "$1: $install_cmd $pkg"
        run_cmd root $1 "$install_cmd $pkg"
    done
}
```
[/details]
[details="install_base_tpl_pkgs ()"]
```bash
install_base_tpl_pkgs ()
{
    install_packages $base_tpl "$@"
    qvm-shutdown --wait $base_tpl
}
```
[/details]
[details="create_template ()"]
```bash
create_template ()
{
    qvm-clone $base_tpl $1
    install_packages "$@"
    qvm-shutdown --wait $1
}
```
[/details]
```bash
system_tpl=$base_tpl-sys
apps_tpl=$base_tpl-apps
print_tpl=$base_tpl-print
vault_tpl=$base_tpl-vault
web_tpl=$base_tpl-web
work_tpl=$base_tpl-work
```

Adapt the order and creation to your needs.
i.e.
`$passwordless_root` is in all templates.
`$file_manager` is not in `$system_tpl`, but is in all others.
```bash
install_base_tpl_pkgs \
    $passwordless_root

create_template $system_tpl \
    $default_mgmt \
    $sys_network \
    $sys_firewall \
    $sys_usb

install_base_tpl_pkgs \
    $file_manager

create_template $vault_tpl \
    $password_manager

install_base_tpl_pkgs \
    $networking \
    $usb_proxy \
    $text_editor \
    $qubes_converter_tools

create_template $web_tpl \
    $audio \
    "$web_browser"

install_base_tpl_pkgs \
    $image_viewer \
    $pdf_viewer \
    $qt_theme

create_template $apps_tpl \
    $audio \
    "$media_player" \
    $office_suite \
    $email_client

create_template $print_tpl \
    $printer

create_template $work_tpl \
    "$code_editor" \
    $dev_tools
```

Rename the base template backup and set the "default template".
```bash
qvm-remove --force $base_tpl
qvm-clone $base_tpl-bak $base_tpl
qvm-remove --force $base_tpl-bak

qubes-prefs default_template $apps_tpl
```


## Template settings
---
```bash
echo 'setting templates ...'
```
> :information_source: **Note:**
> All these settings, despite belonging to a fresh install script, **are not Qubes OS specific**.
> There are already many resources about all of them across the web.

### 1. settings
[details="gnome mimeapps"]
```bash
set_disable_gnome_mimeapps ()
{
    gnome_mimeapps=/usr/share/applications/gnome-mimeapps.list
    mv $gnome_mimeapps $gnome_mimeapps.bak
}
```
[/details]
[details="filetype association"]
```bash
set_default_mimetype ()
{
    echo '
    [Default Applications]
    text/plain=org.xfce.mousepad.desktop
    application/pdf=qpdfview-qt5.desktop' | cut -c 5- \
        >> /etc/skel/.config/mimeapps.list
}
```
[/details]
[details="dnf"]
```bash
set_dnf ()
{
    echo 'install_weak_deps=false' >> /etc/dnf/dnf.conf
}
```
[/details]
[details="qt theme"]
```bash
set_qt_theme ()
{
    echo 'QT_STYLE_OVERRIDE=adwaita-dark' >> /etc/environment
}
```
[/details]
[details="gtk"]
```bash
set_gtk ()
{
    local gtk3_dir=/etc/skel/.config/gtk-3.0/

    mkdir -p $gtk3_dir
    echo '
    [Settings]
    gtk-theme-name=Arc-Dark
    gtk-icon-theme-name=gnome
    gtk-decoration-layout=menu:
    gtk-titlebar-right-click=none' | cut -c 5- > $gtk3_dir/settings.ini

    # darker inactive tabs
    echo '
    .chromium menubar {
        background-color: #252A32
    }

    notebook header {
        background-color: #2F343F
    }' | cut -c 5- > $gtk3_dir/gtk.css

    # GTK4 dark mode
    # needed for zenity progress dialog used by qvm-copy/move
    # (dom0 Arc theme doesn't have GTK4 variant)
    local dconf_local_dir=/etc/dconf/db/local.d/

    mkdir -p $dconf_local_dir
    echo "
    [org/gnome/desktop/interface]
    color-scheme='prefer-dark'" | cut -c 5- > $dconf_local_dir/gnome-interface
    dconf update
}
```
[/details]
[details="default terminal"]
```bash
set_default_terminal ()
{
    local xfce_dir=/etc/skel/.config/xfce4/

    mkdir -p $xfce_dir
    echo 'TerminalEmulator=xterm' > $xfce_dir/helpers.rc
}
```
[/details]
[details="xterm"]
```bash
set_xterm ()
{
    echo '
    xterm*background: black
    xterm*foreground: white
    xterm*faceName: monospace
    xterm*faceSize: 12
    xterm*geometry: 80x40
    xterm*saveLines: 100000
    xterm*selectToClipboard: true' | cut -c 5- \
        | tee -a /etc/skel/.Xresources /home/user/.Xresources > /dev/null
}
```
[/details]
[details="bash"]
```bash
set_bash ()
{
    echo '
    export PS1="\[\e[1;31m\]$PS1\[\e[m\]"

    alias ls="ls --color=auto -F"
    alias ll="ls -lh"
    alias la="ls -lah"
    alias sudo="sudo "' | cut -c 5- \
        | tee -a /etc/skel/.bashrc /home/user/.bashrc /root/.bashrc > /dev/null
}
```
[/details]
<br>

[details="file chooser"]
```bash
set_file_chooser ()
{
    local dconf_local_dir=/etc/dconf/db/local.d/

    mkdir -p $dconf_local_dir
    echo '
    [org/gtk/settings/file-chooser]
    sort-directories-first=true
    window-position=(0, 0)
    window-size=(850, 550)' | cut -c 5- > $dconf_local_dir/file-chooser
    dconf update
}
```
[/details]
[details="file manager"]
```bash
set_file_manager ()
{
    local xfce_cfg_dir=/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/

    mkdir -p $xfce_cfg_dir
    echo '<?xml version="1.0" encoding="UTF-8"?>
    <channel name="thunar" version="1.0">
      <property name="last-location-bar"       type="string" value="ThunarLocationButtons"/>
      <property name="last-window-width"       type="int"    value="900"/>
      <property name="last-window-height"      type="int"    value="600"/>
      <property name="misc-show-delete-action" type="bool"   value="true"/>
    </channel>' > $xfce_cfg_dir/thunar.xml
}
```
[/details]
[details="password manager"]
```bash
set_password_manager ()
{
    local keepassxc_dir=/etc/skel/.config/keepassxc/

    mkdir -p $keepassxc_dir
    echo '
    [GUI]
    ApplicationTheme=dark' | cut -c 5- > $keepassxc_dir/keepassxc.ini
}
```
[/details]
[details="text editor"]
```bash
set_text_editor ()
{
    local dconf_local_dir=/etc/dconf/db/local.d/

    mkdir -p $dconf_local_dir
    echo "
    [org/xfce/mousepad/preferences/view]
    auto-indent=true
    color-scheme='cobalt'
    insert-spaces=true
    match-braces=true
    smart-backspace=true
    tab-width=uint32 4

    [org/xfce/mousepad/preferences/window]
    statusbar-visible=true

    [org/xfce/mousepad/state/window]
    height=uint32 900
    width=uint32 800" | cut -c 5- > $dconf_local_dir/mousepad
    dconf update
}
```
[/details]
[details="image viewer"]
```bash
set_image_viewer ()
{
    local dconf_local_dir=/etc/dconf/db/local.d/

    mkdir -p $dconf_local_dir
    echo "
    [org/gnome/eog/plugins]
    active-plugins=['statusbar-date', 'fullscreen']

    [org/gnome/eog/ui]
    image-gallery=true
    sidebar=false
    statusbar=true" | cut -c 5- > $dconf_local_dir/eog
    dconf update
}
```
[/details]
[details="pdf viewer"]
```bash
set_pdf_viewer ()
{
    local qpdfview_dir=/etc/skel/.config/qpdfview/

    mkdir -p $qpdfview_dir
    # background color: #383C4A
    # paper color : #999999
    echo '
    [documentView]
    highlightCurrentThumbnail=true
    prefetch=true
    prefetchDistance=2
    scaleMode=1

    [pageItem]
    backgroundColor=@Variant(\0\0\0\x43\x1\xff\xff\x38\x38<<JJ\0\0)
    paperColor=@Variant(\0\0\0\x43\x1\xff\xff\x99\x99\x99\x99\x99\x99\0\0)' \
        | cut -c 5- > $qpdfview_dir/qpdfview.conf
}
```
[/details]
[details="media player"]
```bash
set_media_player ()
{
    local vlc_dir=/etc/skel/.config/vlc/

    mkdir -p $vlc_dir
    echo '
    [qt]
    qt-privacy-ask=0
    qt-recentplay=0
    qt-system-tray=0
    qt-video-autorezise=0

    [core]
    metadata-network-access=0' | cut -c 5- > $vlc_dir/vlcrc
}
```
[/details]
[details="office suite"]
```bash
set_office_suite ()
{
    local lo_org=org.openoffice
    local lo_dir=/etc/skel/.config/libreoffice/4/user/
    local lo_cfg=$lo_dir/registrymodifications.xcu

    mkdir -p $lo_dir
    add_key_value ()
    {
        echo '<item oor:path="'$1'">' \
                 '<prop oor:name="'$2'" oor:op="fuse">' \
                     '<value>'$3'</value>' \
                 '</prop>' \
             '</item>' >> $lo_cfg
    }
    enable_ribbon_toolbar ()
    {
        for app in $@
        do
            local tb_mode=$lo_org.Office.UI.ToolbarMode
            local tb_app="/$tb_mode/Applications/$tb_mode:Application['$app']"
            local tabbed_mode="/Modes/$tb_mode:ModeEntry['Tabbed']"
            add_key_value $tb_app Active notebookbar.ui
            add_key_value $tb_app$tabbed_mode HasMenubar false
        done
    }
    set_default_window_size ()
    {
        if [[ $# -ne 0 ]]
        then
            local setup=$lo_org.Setup
            local app=com.sun.star.$1
            local app_cfg="/$setup/Office/Factories/$setup:Factory['$app']"
            local window_opt=ooSetupFactoryWindowAttributes
            local window_size="0,0,$2,$3;5;0,0,$2,$3;"
            add_key_value $app_cfg $window_opt $window_size
            set_default_window_size ${@:4}
        fi
    }

    echo '<?xml version="1.0" encoding="UTF-8"?>
    <oor:items
        xmlns:oor="http://openoffice.org/2001/registry"
        xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' > $lo_cfg

    local lo_help=/$lo_org.Office.Common/Help
    add_key_value $lo_help BuiltInHelpNotInstalledPopUp false

    local lo_misc=/$lo_org.Office.Common/Misc
    add_key_value $lo_misc FirstRun false
    add_key_value $lo_misc ShowTipOfTheDay false
    add_key_value $lo_misc SymbolStyle colibre_dark_svg

    local lo_ui=$lo_org.Office.UI
    local lo_color=/$lo_ui/ColorScheme/ColorSchemes/$lo_ui
    local lo_doc_bg="$lo_color:ColorScheme['LibreOffice']/DocColor"
    add_key_value $lo_doc_bg Color 10066329 # light gray 1 (#999999)

    enable_ribbon_toolbar Calc Draw Writer

    set_default_window_size \
        frame.StartModule          1400 900 \
        sheet.SpreadsheetDocument  1400 900 \
        drawing.DrawingDocument    1400 900 \
        text.TextDocument          1400 900

    local lo_product=/$lo_org.Setup/Product
    add_key_value $lo_product ooSetupLastVersion 42.0
    add_key_value $lo_product LastTimeDonateShown 4200000000
    add_key_value $lo_product LastTimeGetInvolvedShown 4200000000

    echo '</oor:items>' >> $lo_cfg
}
```
[/details]
[details="email client"]
```bash
set_email_client ()
{
    local default_prefs_dir=/usr/lib64/thunderbird/defaults/pref/
    local prefs_cfg=$default_prefs_dir/user.js

    echo '
    /* menu > edit > settings */
    /* ********************** */

    /* # General */
    pref("mailnews.start_page.enabled", false);

    /* # Language & Appearance */
    /* ## font & colors */
    pref("browser.display.use_system_colors", true);
    pref("browser.display.document_color_use", 2); // override: always
    /* ## plain text messages */
    pref("mail.display_glyph", false); // emoticons as graphics

    /* # Incoming Mails */
    pref("mail.biff.alert.show_preview", false);
    pref("mail.biff.play_sound", false);

    /* # Files & Attachments */
    pref("pdfjs.disabled", true);
    pref("browser.download.useDownloadDir", true);
    pref("browser.download.dir", "/home/user");
    pref("browser.download.downloadDir", "/home/user");

    /* # Reading & Display */
    pref("mail.showCondensedAddresses", false);

    /* # Network & Disk Space */
    /* ## offline */
    pref("offline.download.download_messages", 2); // disable

    /* # Composition */
    /* ## spelling */
    pref("mail.SpellCheckBeforeSend", false);
    pref("mail.spellcheck.inline", false); // when typing
    /* ## html style */
    pref("msgcompose.default_colors", true);
    /* ## sending format */
    pref("mail.default_send_format", 1); // only plain text

    /* # Attachments */
    pref("mail.compose.attachment_reminder", false);
    pref("mail.compose.big_attachments.notify", false);

    /* # Privacy */
    /* ## mail content */
    pref("mailnews.message_display.disable_remote_image", true);
    /* ## web content */
    pref("network.cookie.cookieBehavior", 2); // disable
    pref("places.history.enabled", false);

    /* # Thunderbird Data Collection */
    pref("datareporting.healthreport.uploadEnabled", false);

    /* # Security */
    pref("mail.phishing.detection.enabled", false);

    /* # Chat */
    pref("messenger.startup.action", 0); // offline


    /* menu > view */
    /* *********** */

    /* menu > view > message body as > plain text */
    pref("mailnews.display.disallow_mime_handlers", 1);
    pref("mailnews.display.html_as", 1);
    pref("mailnews.display.prefer_plaintext", true);

    /* menu > view > headers > all */
    pref("mail.show_headers", 2);


    /* config editor */
    /* ************* */

    pref("network.protocol-handler.external-default", false) # disable links

    pref("mail.chat.enabled", false);
    pref("geo.enabled", false);
    pref("browser.region.update.enabled", false);

    pref("toolkit.telemetry.unified", false);
    pref("toolkit.telemetry.server", "");
    pref("toolkit.telemetry.newProfilePing.enabled", false);
    pref("toolkit.telemetry.updatePing.enabled", false);
    pref("toolkit.telemetry.shutdownPingSender.enabled", false);
    pref("toolkit.telemetry.bhrPing.enabled", false);
    pref("toolkit.telemetry.firstShutdownPing.enabled", false);
    pref("toolkit.coverage.opt-out", true);

    pref("breakpad.reportURL", ""); // crash report
    pref("captivedetect.canonicalURL", ""); // captive portal
    pref("network.connectivity-service.enabled", false); // network check
    pref("mail.rights.version", 1); // disable "know rights" notif' \
        | cut -c 5- > $prefs_cfg
}
```
[/details]
[details="web browser"]
```bash
set_web_browser ()
{
    local brave_dir=/etc/skel/.config/BraveSoftware/Brave-Browser/
    local brave_state_cfg="$brave_dir/Local State"
    local brave_prefs_cfg=$brave_dir/Default/Preferences

    mkdir -p $brave_dir/Default/
    state_add_value_to_brave_key ()
    {
        sed -i '/"brave": {/ r'<(echo "$1") "$brave_state_cfg"
    }
    prefs_add_value_to_key ()
    {
        sed -i "/$1/ r"<(echo "$2") $brave_prefs_cfg
    }

    echo '{' | tee "$brave_state_cfg" $brave_prefs_cfg > /dev/null

    ## brave://flags
    #---------------
    echo '
        "browser": {
            "enabled_labs_experiments": [
                "enable-force-dark@1", # web content night mode
                "translate@2" # disable
            ]
        },' >> "$brave_state_cfg"

    ## Get started
    #-------------
    echo '
        "session": {
            "restore_on_startup": 5 # open new tab page
        },' >> $brave_prefs_cfg

    ## Appearance
    #------------
    echo '
        "brave": {
            "dark_mode": 1 # enable
        },' >> "$brave_state_cfg"
    echo '
        "extensions": {
            "theme": {
                "system_theme": 1 # GTK
            }
        },
        "bookmark_bar": {
            "show_on_all_tabs": true
        },
        "brave": {
            "show_side_panel_button": false,
            "today": {
                "should_show_toolbar_button": false # brave news button
            },
            "location_bar_is_wide": false,
            "omnibox": {
                "prevent_url_elisions": false, # show full URL
                "bookmark_suggestions_enabled": true,
                "history_suggestions_enabled": true
            },
            "sidebar": {
                "sidebar_show_option": 3 # never
            },
            "show_side_panel_button": false,
            "autocomplete_enabled": true,
            "top_site_suggestions_enabled": true,
            "tabs_search_show": true,
            "tabs": {
                "mute_indicator_not_clickable": false,
                "vertical_tabs_enabled": false,
                "hover_mode": 1 # card
            },
            "speedreader": {
                "enabled": false
            },
            "mru_cycling_enabled": false # cycle most recently tabs
        },
        "browser": {
            "show_home_button": false,
            "custom_chrome_frame": false # use system frame (enable)
        },' >> $brave_prefs_cfg

    ## New Tab Page
    #--------------
    prefs_add_value_to_key '"brave": {' '
            "new_tab_page": {
                "hide_all_widgets": true, # cards
                "show_background_image": true,
                "show_branded_background_image": false,
                "show_clock": false,
                "show_stats": false,
                "show_together": false, # news
                "shows_options": 0 # new tab page: dashboard
            },'
    echo '
        "ntp": {
            "shortcust_visible": false # top sites
        },' >> $brave_prefs_cfg

    ## Shields
    #---------
    prefs_add_value_to_key '"brave": {' '
            "shields": {
                "stats_badge_visible": false # number on icon
            },
            "de_amp": {
                "enabled": true # auto-redirect AMP
            },
            "debounce": {
                "enabled": true # auto redirect tracking urls
            },
            "reduce_language": true, # prevent fingerprinting
            "no_script_default": false,'
    echo '
        "profile": {
            "content_settings": { # agressive / strict
                "exceptions": {
                    "fingerprintingV2": {
                        "*,*": {
                            "setting": 2
                        }
                    },
                    "cosmeticFiltering": { # tackers & ads
                        "*,*": {
                            "setting": 2
                        },
                        "*,https://firstparty": {
                            "setting": 2
                        }
                    },
                    "shieldsAds": { # tackers & ads
                        "*,*": {
                            "setting": 2
                        }
                    },
                    "trackers": { # tackers & ads
                        "*,*": {
                            "setting": 2
                        }
                    }
                }
            },
            "cookie_controls_mode": 1, # block cross-site
            "default_content_setting_values": {
                "httpsUpgrades": 2 # strict
            }
        },' >> $brave_prefs_cfg
    ### Content Filtering:
    state_add_value_to_brave_key '
            "ad_block": {
                "cookie_list_opt_in_shown": true,
                "regional_filters": {
                    "319A754E-065A-465F-B09D-3F2C7BF1E67B": {
                        "enabled": true # ublock annoyances list
                    },
                    "67E792D4-AE03-4D1A-9EDE-80E01C81F9B8": {
                        "enabled": true # fanboy annoyances list
                    }
                }
            },'

    ## Brave Rewards
    #---------------
    prefs_add_value_to_key '"brave": {' '
            "rewards": {
                "inline_tip_buttons_enabled": false,
                "show_brave_rewards_button_in_location_bar": false
            },'

    ## Social media blocking
    #-----------------------
    prefs_add_value_to_key '"brave": {' '
            "google_login_default": false,
            "fb_embed_default": false,
            "twitter_embed_default": false,
            "linkedin_embed_default": false,'

    ## Privacy and security
    #----------------------
    echo '
        "search": {
            "suggest_enabled": false # improve search
        },
        "webrtc": {
            "ip_handling_policy": "disable_non_proxied_udp"
        },' >> $brave_prefs_cfg
    prefs_add_value_to_key '"brave": {' '
            "gcm": { # google for push messaging
                "channel_status": false
            },'
    state_add_value_to_brave_key '
            "p3a": {
                "enabled": false # product analytics
            },
            "stats": {
                "reporting_enabled": false # daily ping
            },'
    echo '
        "user_experience_metrics": {
            "reporting_enabled": false # diagnostic reports
        },' >> "$brave_state_cfg"
    ### Clear Browsing data
    prefs_add_value_to_key '"browser": {' '
            "clear_data": {
                "browsing_history_on_exit": true,
                "cache_on_exit": true,
                "cookies_on_exit": true,
                "download_history_on_exit": true,
                "form_data_on_exit": true,
                "hosted_apps_data_on_exit": true,
                "passwords_on_exit": true,
                "site_settings_on_exit": false
            },'
    ### Cookies and other site data
    prefs_add_value_to_key '"default_content_setting_values": {' '
                "cookies": 4,' # clear cookies/site data, block third-party
    echo '
        "enable_do_not_track": false,' >> $brave_prefs_cfg
    ### Security
    echo '
        "safebrowsing": {
            "enabled": false
        },
        "https_only_mode_enabled": true,' >> $brave_prefs_cfg
    echo '
        "dns_over_https": {
            "mode": "secure",
            "templates": "https://dns.adguard-dns.com/dns-query"
        },' >> "$brave_state_cfg"
    ### Site and Shields Settings
    prefs_add_value_to_key '"default_content_setting_values": {' '
                "ar": 2,
                "automatic_downloads": 1,
                "autoplay": 1,
                "brave_ethereum": 2,
                "brave_google_sign_in": 2,
                "brave_solana": 2,
                "clipboard": 2,
                "file_system_write_guard": 2,
                "geolocation": 2,
                "hid_guard": 2,
                "images": 1,
                "local_fonts": 2,
                "media_stream_camera": 2,
                "media_stream_mic": 2,
                "midi_sysex": 2,
                "notifications": 2,
                "payment_handler": 2,
                "popups": 2,
                "sensors": 2,
                "serial_guard": 2,
                "sound": 1,
                "usb_guard": 2,
                "vr": 2,
                "window_placement": 2,'
    echo '
        "custom_handlers": {
            "enabled": false # protocol handlers
        },
        "plugins": {
            "always_open_pdf_externally": true # download pdf
        },
        "webkit": {
            "webprefs": {
                "encrypted_media_enabled": false # protected content
            }
        },' >> $brave_prefs_cfg
    ### Tor windows
    echo '
        "tor": {
            "tor_disabled": true
        },' >> "$brave_state_cfg"

    ## Search engine
    #---------------
    echo '
        "default_search_provider": {
            "synced_guid": "485bf7d3-0215-45af-87dc-538868000510"
        },
        "default_search_provider_data": {
            "template_url_data": {
                "keyword": ":sp",
                "prepopulate_id": 510,
                "short_name": "Startpage",
                "synced_guid": "485bf7d3-0215-45af-87dc-538868000510",
                "url": ""
            }
        },' >> $brave_prefs_cfg
    prefs_add_value_to_key '"brave": {' '
            "other_search_engines_enabled": false,
            "web_discovery_enabled": false,'

    ## Extensions
    #------------
    prefs_add_value_to_key '"brave": {' '
            "hangouts_enabled": false,
            "webtorrent_enabled": false,'
    echo '
        "signin": {
            "allowed": false # google login
        },
        "media_router": {
            "enable_media_router": false
        },' >> $brave_prefs_cfg
    state_add_value_to_brave_key '
            "widevine_opted_in": false,'

    ## Web3
    #------
    ### Wallet
    prefs_add_value_to_key '"brave": {' '
            "wallet": {
                "default_solana_wallet": 1, # no fallback
                "default_wallet2": 1, # eth: no fallback
                "show_wallet_icon_on_toolbar": false,
                "nft_discovery_enabled": false,
                "auto_pin_enabled": false
            },'
    ### IPFS
    prefs_add_value_to_key '"brave": {' '
            "ipfs": {
                "resolve_method": 3 # disabled
            },'
    ### Web3 domains
    state_add_value_to_brave_key '
            "ens": {
                "resolve_method": 1 # disabled
            },
            "sns": {
                "resolve_method": 1 # disabled
            },
            "unstoppable_domains": {
                "resolve_method": 1 # disabled
            },'

    ## Autofill
    #----------
    echo '
        "autofill": {
            "credit_card_enabled": false, # save payment
            "profile_enabled": false # addresses
        },
        "credentials_enable_autosignin": false,
        "credentials_enable_service": false, # save password
        "payments": {
            "can_make_payment_enabled": false # allow sites to check
        },' >> $brave_prefs_cfg

    ## Languages
    #-----------
    echo '
        "translate": {
            "enabled": false
        },' >> $brave_prefs_cfg
    prefs_add_value_to_key '"browser": {' '
            "enable_spellchecking": false,'

    ## Download
    #----------
    echo '
        "download": {
            "prompt_for_download": false
        },
        "download_bubble": {
            "partial_view_enabled": true # show when done
        }' >> $brave_prefs_cfg

    ## Help tips
    #-----------
    prefs_add_value_to_key '"brave": {' '
            "wayback_machine_enabled": false,
            "enable_window_closing_confirm": true,'

    ## System
    #--------
    echo '
        "background_mode": {
            "enabled": false
        },
        "hardware_acceleration_mode": {
            "enabled": false
        },' >> "$brave_state_cfg"
    prefs_add_value_to_key '"brave": {' '
            "enable_closing_last_tab": true,'
    echo '
        "performance_tuning": {
            "high_efficiency_mode": {
                "enabled": false # memory saver
            }
        }' >> "$brave_state_cfg"

    ## Misc
    #------
    state_add_value_to_brave_key '
            "dont_ask_for_crash_reporting": true,'
    prefs_add_value_to_key '"shields": {' '
                "advanced_view_enabled": true,'

    echo '}' | tee -a "$brave_state_cfg" $brave_prefs_cfg > /dev/null
    sed -i 's/ #.*//' "$brave_state_cfg" $brave_prefs_cfg
}
```
[/details]
<br>

[details="code editor"]
```bash
set_code_editor ()
{
    local codium_dir=/etc/skel/.config/VSCodium/User/

    mkdir -p $codium_dir
    echo '
    {
    }' | cut -c 5- > $codium_dir/settings.json
}
```
[/details]
[details="git"]
```bash
set_git ()
{
    echo '
    [user]
        name   "John Doe"
        email  johndoe@example.com
    [core]
        editor vim' | cut -c 5- > /etc/skel/.gitconfig
}
```
[/details]
[details="vim"]
```bash
set_vim ()
{
    echo '
    source $VIMRUNTIME/defaults.vim
    set expandtab
    set smarttab
    set shiftwidth=4
    set tabstop=4' | cut -c 5- > /etc/skel/.vimrc
}
```
[/details]
[details="zsh"]
```bash
set_zsh ()
{
    sed -i 's/bash/zsh/' /etc/passwd
    echo '
    git_branch ()
    {
        git branch 2> /dev/null \
            | sed -e "/^[^*]/ d" \
                  -e "s/* \(.*\)/(\1)/"
    }

    setopt PROMPT_SUBST
    autoload colors
    colors
    export PS1="%B%{$fg[black]%}$(git_branch)%{$fg[red]%}$PS1%b%{$reset_color%}"

    autoload -U compinit
    compinit
    zstyle ":completion:*" matcher-list "m:{a-z}={A-Z}"

    alias ls="ls --color=auto -F"
    alias ll="ls -lh"
    alias la="ls -lah"
    alias sudo="sudo "' | cut -c 5- > /etc/skel/.zshrc
}
```
[/details]

### 2. customization
[details="handle_custom_settings ()"]
```bash
handle_custom_settings ()
{
    for qube in $2
    do
        echo "    $qube ..."
        run_cmd $1 $qube "
            $(declare -f ${@:3})
            $(echo ${@:3} | sed 's/ set_/;&/g')"
        qvm-shutdown --wait $qube
    done
}
```
[/details]
[details="custom_settings ()"]
```bash
custom_settings ()
{
    handle_custom_settings root "$@"
}
```
[/details]
[details="custom_settings_user ()"]
```bash
custom_settings_user ()
{
    handle_custom_settings user "$@"
}
```
[/details]
<br>

[details="set_common"]
```bash
set_common='
    set_dnf
    set_gtk
    set_default_terminal
    set_xterm
    set_bash'
```
[/details]
[details="set_file_management"]
```bash
set_file_management='
    set_file_chooser
    set_file_manager'
```
[/details]
[details="set_text_img_pdf"]
```bash
set_text_img_pdf='
    set_text_editor
    set_image_viewer
    set_pdf_viewer'
```
[/details]
[details="set_dev_tools"]
```bash
set_dev_tools='
    set_git
    set_vim
    set_zsh'
```
[/details]

Set the settings in their corresponding templates.
```bash
custom_settings $base_tpl \
    $set_common

custom_settings $system_tpl \
    $set_common

custom_settings $apps_tpl \
    $set_common \
    $set_file_management \
    $set_text_img_pdf \
    set_disable_gnome_mimeapps \
    set_qt_theme \
    set_media_player \
    set_office_suite \
    set_default_mimetype \
    set_email_client

custom_settings $print_tpl \
    $set_common \
    $set_file_management \
    $set_text_img_pdf \
    set_disable_gnome_mimeapps \
    set_qt_theme

custom_settings $vault_tpl \
    $set_common \
    $set_file_management \
    set_password_manager

custom_settings $web_tpl \
    $set_common \
    $set_file_management \
    set_text_editor \
    set_web_browser

custom_settings $work_tpl \
    $set_common \
    $set_file_management \
    $set_text_img_pdf \
    set_disable_gnome_mimeapps \
    set_qt_theme \
    set_code_editor \
    $set_dev_tools
```


## Template management
---
[qubes-os.org/doc/templates/#switching](https://qubes-os.org/doc/templates/#switching)

> :information_source: **Note:**
> Do not enable for a fresh installation.
> Only for new template release (e.g. fedora XX -> fedora XX + 1).

```bash
if false; then ## new tpl release
echo 'switching old templates with new ones ...'
```

### 1. switch templates
```bash
qvm-shutdown --all --wait
```
[details="Change the templates."]
If you only have a USB keyboard/mouse, you may want to switch the `sys-dvm`
after confirming that the new `sys-usb-dvm` works as expected.
```bash
change_template ()
{
    if [[ $# -ne 0 ]]
    then
        qvm-prefs $1 template $2
        change_template ${@:3}
    fi
}
change_template $(qvm-ls --field class,name,template \
    | sed -e '/^AppVM/ !d' \
          -e "/$os_name/ !d" \
          -e 's/^AppVM//' \
          -Ee "s/$os_name-[0-9]+/$os_name-$os_release/")
```
[/details]
[details="Remove the old templates."]
Keep the old system template until confirming working internet.
```bash
remove_old_template ()
{
    if [[ $# -ne 0 ]]
    then
        qvm-remove --force $1
        remove_old_template ${@:2}
    fi
}
remove_old_template $(qvm-ls --field class,name \
    | sed -e '/^TemplateVM/ !d' \
          -e "/$os_name/ !d" \
          -e "/$os_name-$os_release/ d" \
          -e '/min-sys/ d' \
          -e 's/^TemplateVM//')
```
[/details]
```bash
qvm-start \
    sys-usb-dvm \
    sys-net-dvm \
    sys-firewall-dvm
```

### 2. update settings
Update the settings where needed.
[details="set_new_web_browser_settings"]
```bash
set_new_web_browser_settings ()
{
    local brave_dir=.config/BraveSoftware/Brave-Browser/
    local brave_state_cfg="$brave_dir/Local State"
    local brave_prefs_cfg=$brave_dir/Default/Preferences

    cp /etc/skel/$brave_state_cfg /home/user/$brave_state_cfg
    cp /etc/skel/$brave_prefs_cfg /home/user/$brave_prefs_cfg
}
```
[/details]

```bash
custom_settings_user web-dvm \
    set_new_web_browser_settings

fi ## end: new tpl release
```


## Disposable templates
---
[qubes-os.org/doc/disposable-customization/](https://qubes-os.org/doc/disposable-customization/)
```bash
if true; then ## fresh install
echo 'creating disposable templates ...'
```
[details="create_dvm_template ()"]
```bash
create_dvm_template ()
{
    if [[ $# -ne 0 ]]
    then
        echo "    $1 ..."
        qvm-create $1 --template $2 --label $3 \
            --property maxmem=4096 \
            --property memory=512 \
            --property netvm='' \
            --property template_for_dispvms=true
        qvm-features $1 appmenus-dispvm $4
        create_dvm_template "${@:5}"
    fi
}
```
[/details]
```bash
mgmt_dvm=mgmt-dvm
sys_dvm=sys-dvm
apps_dvm=apps-dvm
print_dvm=print-dvm
web_dvm=web-dvm
```
```bash
create_dvm_template \
    $mgmt_dvm  $system_tpl black '' \
    $sys_dvm   $system_tpl red   '' \
    $apps_dvm  $apps_tpl   red   1  \
    $print_dvm $print_tpl  red   '' \
    $web_dvm   $web_tpl    red   1
```
[details="Set the "default management" and "default disposable" qubes."]
```bash
qvm-features $mgmt_dvm internal 1
qubes-prefs management_dispvm $mgmt_dvm

qubes-prefs default_dispvm $apps_dvm
```
[/details]


## Named disposables
---
[qubes-os.org/doc/disposable-customization/#using-named-disposables-for-sys-](https://qubes-os.org/doc/disposable-customization/#using-named-disposables-for-sys-)
```bash
echo 'creating named disposables ...'
```
[details="create_named_dvm ()"]
```bash
create_named_dvm ()
{
    if [[ $# -ne 0 ]]
    then
        local vmode=pvh
        if [[ $5 -eq 0 ]]; then vmode=hvm; fi
        echo "    $1 ..."
        qvm-create $1 --template $2 --class DispVM --label $3 \
            --property autostart=$4 \
            --property maxmem=$5 \
            --property memory=$6 \
            --property netvm=$7 \
            --property provides_network=$8 \
            --property vcpus=1 \
            --property virt_mode=$vmode
        qvm-features $1 appmenus-dispvm ''
        create_named_dvm "${@:9}"
    fi
}
```
[/details]
```bash
net_dvm=sys-net-dvm
fw_dvm=sys-firewall-dvm
usb_dvm=sys-usb-dvm
printer_dvm=printer-dvm
```
```bash
create_named_dvm \
    $net_dvm      $sys_dvm   red    'true'  0    448 ''       'true'  \
    $fw_dvm       $sys_dvm   green  'true'  2048 512 $net_dvm 'true'  \
    $usb_dvm      $sys_dvm   red    'true'  0    320 ''       'false' \
    banking-dvm   $web_dvm   gray   'false' 2048 512 $fw_dvm  'false' \
    mail-web-dvm  $web_dvm   purple 'false' 2048 512 $fw_dvm  'false' \
    $printer_dvm  $print_dvm red    'false' 2048 512 $fw_dvm  'false'
```
[details="Set the "default clock" and "default update" qubes."]
```bash
qubes-prefs clockvm  $net_dvm
qubes-prefs updatevm $fw_dvm
```
[/details]
[details="Set the "default net" qube."]
It cannot be changed to a domain that is not running.
```bash
qvm-start $net_dvm $fw_dvm
qubes-prefs default_netvm $fw_dvm
qvm-shutdown --wait $fw_dvm $net_dvm
```
[/details]
Set the "qubes.UpdatesProxy" policy to use `$net_dvm`.
[qubes-os.org/doc/rpc-policy/](https://qubes-os.org/doc/rpc-policy/)
```bash
echo "qubes.UpdatesProxy * @type:TemplateVM  @default  allow target=$net_dvm" \
    | sudo tee -a /etc/qubes/policy.d/30-user.policy > /dev/null
```
[details="Disable the non-disposable system qubes."]
```bash
qvm-prefs sys-usb      autostart false
qvm-prefs sys-net      autostart false
qvm-prefs sys-firewall autostart false
```
[/details]


## Regular app qubes
---
[qubes-os.org/doc/how-to-organize-your-qubes/#conclusion](https://qubes-os.org/doc/how-to-organize-your-qubes/#conclusion)
```bash
echo 'creating regular appvms ...'
```
[details="create_regular_appvm ()"]
```bash
create_regular_appvm ()
{
    if [[ $# -ne 0 ]]
    then
        echo "    $1 ..."
        qvm-create $1 --template $2 --label $3 \
            --property autostart=$4 \
            --property maxmem=$5 \
            --property memory=$6 \
            --property netvm=$7 \
            --property vcpus=$8
        qvm-features $1 appmenus-dispvm ''
        create_regular_appvm "${@:9}"
    fi
}
```
[/details]
```bash
create_regular_appvm \
    daily-web $web_tpl   orange 'true'  4096 512 $fw_dvm 2 \
    mail      $apps_tpl  purple 'false' 2048 512 $fw_dvm 1 \
    media     $apps_tpl  yellow 'false' 4096 512 ''      2 \
    personal  $apps_tpl  yellow 'false' 4096 512 ''      2 \
    vault     $vault_tpl black  'false' 2048 512 ''      1 \
    work      $work_tpl  blue   'false' 4096 512 ''      2 \
    work-web  $web_tpl   blue   'false' 2048 512 $fw_dvm 1
```
[details="Set the fullscreen mode."]
[qubes-os.org/doc/how-to-enter-fullscreen-mode/](https://qubes-os.org/doc/how-to-enter-fullscreen-mode/)
```bash
qvm-features daily-web gui-allow-fullscreen 1
qvm-features media     gui-allow-fullscreen 1
```
[/details]
[details="Resize the private storage."]
[qubes-os.org/doc/resize-disk-image/](https://qubes-os.org/doc/resize-disk-image/)
```bash
qvm-volume resize daily-web:private 10737418240 # 10GiB (2^30 * 10)
```
[/details]


## Network
---
[dev.qubes-os.org/projects/core-admin-client/en/latest/manpages/qvm-firewall.html](https://dev.qubes-os.org/projects/core-admin-client/en/latest/manpages/qvm-firewall.html)

Default Firewall rules:
[details="Allow all outgoing connections"]
```bash
qvm-firewall [VMNAME] reset
```
[/details]
[details="Limit outgoing connections to ..."]
```bash
qvm-firewall [VMNAME] reset
qvm-firewall [VMNAME] del accept
qvm-firewall [VMNAME] add accept specialtarget=dns 
qvm-firewall [VMNAME] add accept proto=icmp
qvm-firewall [VMNAME] add drop
```
[/details]
```bash
echo 'setting network ...'

qvm-prefs $web_dvm netvm $fw_dvm
```
Set the printer qube to your printer IP only.
```bash
qvm-firewall $printer_dvm del accept
qvm-firewall $printer_dvm add accept dsthost=192.168.1.42
qvm-firewall $printer_dvm add accept specialtarget=dns 
qvm-firewall $printer_dvm add accept proto=icmp
qvm-firewall $printer_dvm add drop
```


## USB devices
---
```bash
echo 'setting usb devices ...'
```
Automatically accept USB mice (not recommended).
[qubes-os.org/doc/usb-qubes/#usb-mice](https://qubes-os.org/doc/usb-qubes/#usb-mice)
```bash
echo "
qubes.InputMouse * $usb_dvm  dom0  allow
qubes.InputMouse * @anyvm  @anyvm  deny" \
    | sudo tee -a /etc/qubes/policy.d/30-user.policy > /dev/null
```

Setup for USB keyboards depends on your hardware.
[qubes-os.org/doc/usb-qubes/#manual-setup-for-usb-keyboards](https://qubes-os.org/doc/usb-qubes/#manual-setup-for-usb-keyboards)

[details="e.g. only 1 usb controller, only usb keyboard, EFI boot, LUKS."]
```bash
echo "
qubes.InputKeyboard * $usb_dvm  dom0  allow
qubes.InputKeyboard * @anyvm  @anyvm  deny" \
    | sudo tee -a /etc/qubes/policy.d/30-user.policy > /dev/null
```
> :warning: **Caution:**
> Hiding your USB controllers from dom0 could lock you out of your system.

```bash
# rd.qubes.hide_all_usb
# rd.qubes.dom0_usb=XX:XX.X
echo 'GRUB_CMDLINE_LINUX="$GRUB_CMDLINE_LINUX usbcore.authorized_default=0"' \
    | sudo tee -a /etc/default/grub > /dev/null

# sudo grub2-mkconfig -o /boot/grub2/grub.cfg (legacy boot)
sudo grub2-mkconfig -o /boot/efi/EFI/qubes/grub.cfg
```
[/details]


## PCI devices
---
[qubes-os.org/doc/how-to-use-pci-devices/#qvm-pci-usage](https://qubes-os.org/doc/how-to-use-pci-devices/#qvm-pci-usage)
```bash
echo 'setting pci devices ...'
```
[details="get_pci_id ()"]
```bash
get_pci_id ()
{
    qvm-pci | grep "$1" | cut -d ' ' -f 1
}
```
[/details]
[details="pci_attach ()"]
```bash
pci_attach ()
{
    for device in $2
    do
        qvm-pci attach $1 $device ${@:3}
    done
}
```
[/details]
```bash
ethernet_devid=$(get_pci_id 'Ethernet')
wifi_devid=$(get_pci_id 'Network')
usb_devid=$(get_pci_id 'USB')
```

Attach all pci devices (ethernet, wireless, usb controllers) to the `sys-*` qubes.
```bash
pci_attach $net_dvm "$ethernet_devid" --persistent
pci_attach $net_dvm "$wifi_devid" --persistent
pci_attach $usb_dvm "$usb_devid" --persistent --option no-strict-reset=True
```


## App qube settings
---
```bash
echo 'setting app qubes ...'
```
[details="Desktop files entries"]
```bash
xterm_entry='
    xterm.desktop'
file_manager_entry='
    thunar.desktop'
text_editor_entry='
    org.xfce.mousepad.desktop'
image_viewer_entry='
    org.gnome.eog.desktop'
pdf_viewer_entry='
    qpdfview-qt5.desktop'
password_manager_entry='
    org.keepassxc.KeePassXC.desktop'
office_suite_entry0='
    libreoffice-startcenter.desktop'
office_suite_entry1='
    libreoffice-calc.desktop
    libreoffice-draw.desktop
    libreoffice-writer.desktop'
email_client_entry='
    mozilla-thunderbird.desktop'
media_player_entry='
    vlc.desktop'
web_browser_entry='
    brave-browser.desktop'
printer_entry='
    system-config-printer.desktop'
code_editor_entry='
    codium.desktop'
```
[/details]

### 1. settings
[details="filetype association"]
```bash
set_disable_mimetype ()
{
    local user_apps_dir=/home/user/.local/share/applications/

    mkdir -p $user_apps_dir
    for file in $@
    do
        touch $user_apps_dir/$file
    done
}
```
[/details]
[details="file persistent (bind-dirs)"]
[qubes-os.org/doc/bind-dirs/](https://qubes-os.org/doc/bind-dirs/)
```bash
set_file_persistent ()
{
    local qubes_bind_dirs=/rw/config/qubes-bind-dirs.d/

    mkdir -p $qubes_bind_dirs
    for file in $@
    do
        echo "binds+=( '$file' )" >> $qubes_bind_dirs/50_user.conf
    done
}
```
[/details]
[details="wifi connection"]
Automatically connect the wifi connection.
```bash
set_wifi_connection ()
{
    local wifi_dir=/rw/config/NM-system-connections/
    local wifi_cfg=$wifi_dir/home.nmconnection

    mkdir -p $wifi_dir
    echo '
    [wifi]
    ssid=MY_SSID_NAME

    [wifi-security]
    key-mgmt=wpa-psk
    psk=MY_PASSWORD' | cut -c 5- > $wifi_cfg
    chmod 600 $wifi_cfg
}
```
[/details]

### 2. customization
```bash
custom_settings $sys_dvm \
    set_wifi_connection

custom_settings_user mail \
    set_disable_mimetype \
        $text_editor_entry \
        $image_viewer_entry \
        $pdf_viewer_entry \
        $office_suite_entry0 \
        $office_suite_entry1 \
        $media_player_entry

custom_settings_user media \
    set_disable_mimetype \
        $text_editor_entry \
        $image_viewer_entry \
        $pdf_viewer_entry \
        $office_suite_entry0 \
        $office_suite_entry1 \
        $email_client_entry

custom_settings_user personal \
    set_disable_mimetype \
        $email_client_entry

custom_settings $print_dvm \
    set_file_persistent \
        /etc/cups/
```
[details="Add your printer (not Qubes OS specific)."]
[www.cups.org/doc/admin.html](https://www.cups.org/doc/admin.html)
```bash
run_cmd root $print_dvm '
    driver_model=$(lpinfo -m \
        | grep "MY_PRINTER_NAME" \
        | grep simple \
        | cut -d " " -f 1)

    lpadmin -p "MY_CUSTOM_PRINTER_NAME" -E \
        -v lpd://192.168.1.42/PASSTHRU \
        -m $driver_model \
        -o printer-error-policy=retry-current-job \
        -o printer-is-shared=false \
        -o Resolution=301x300dpi \
        -o ColorModel=Gray \
        -o print-quality-default=3'
qvm-shutdown --wait $print_dvm
```
[/details]


## Menu entries
---
```bash
echo 'setting menu entries ...'
```
The "Qube Settings" entry is included in all qubes menus by default.
[details="set_appmenus ()"]
```bash
set_appmenus ()
{
    for appvm in $1
    do
        echo "    $appvm ..."
        echo ${@:2} | qvm-appmenus --set-whitelist - $appvm
        qvm-appmenus --update $appvm
    done
}
```
[/details]
```bash
set_appmenus $apps_dvm \
    $file_manager_entry \
    $xterm_entry

set_appmenus mail \
    $file_manager_entry \
    $email_client_entry

set_appmenus media \
    $file_manager_entry \
    $media_player_entry

set_appmenus personal \
    $file_manager_entry \
    $text_editor_entry \
    $office_suite_entry1

set_appmenus $print_dvm \
    $file_manager_entry \
    $printer_entry

set_appmenus vault \
    $password_manager_entry \
    $file_manager_entry \
    $xterm_entry

set_appmenus "$web_dvm daily-web work-web" \
    $file_manager_entry \
    $web_browser_entry

set_appmenus work \
    $file_manager_entry \
    $text_editor_entry \
    $code_editor_entry \
    $xterm_entry
```


## Dom0 settings
---
```bash
echo 'setting dom0 ...'
```
> :information_source: **Note:**
> All these settings, except Qube Manager, **are not Qubes OS specific**.

```bash
cfg_dir=$HOME/.config/
xfce_cfg_dir=$cfg_dir/xfce4/xfconf/xfce-perchannel-xml/
```

[details="auto-login (not recommended)"]
```bash
sudo sed -i -Ee "s/^#(autologin-user=)/\1$USER/" \
            -Ee 's/^#(autologin-user-timeout=0)/\1/' \
         /etc/lightdm/lightdm.conf
```
[/details]
[details="intel screen tearing (if needed)"]
```bash
echo '
Section "Device"
    Identifier "Intel Graphics"
    Driver "Intel"
EndSection' | sudo tee /etc/X11/xorg.conf.d/20-intel.conf
```
[/details]
<br>

[details="qube manager"]
[qube-manager dark mode (built-in method)](https://forum.qubes-os.org/t/qube-manager-dark-mode-built-in-method/15241)
```bash
echo '[General]
window_size=@Size(755 800)

[columns]
Backup=false
Default DispVM=false
Internal=false
IP=false
Is DVM Template=false
Last backup=false
Virt Mode=false' > "$cfg_dir/The Qubes Project/qubes-qube-manager.conf"
```
[/details]
[details="gtk"]
```bash
gtk3_dir=$cfg_dir/gtk-3.0/

mkdir -p $gtk3_dir
echo '[Settings]
gtk-theme-name=Arc-Dark
gtk-icon-theme-name=gnome' > $gtk3_dir/settings.ini

echo 'notebook header {
    background-color: #2F343F
}' > $gtk3_dir/gtk.css
```
[/details]
[details="bash"]
```bash
echo '
export PS1="\[\e[1;31m\]$PS1\[\e[m\]"

alias ls="ls --color=auto -F"
alias ll="ls -lh"
alias la="ls -lah"
alias sudo="sudo "' >> $HOME/.bashrc
```
[/details]
[details="vim"]
```bash
echo 'source $VIMRUNTIME/defaults.vim
set expandtab
set smarttab
set shiftwidth=4
set tabstop=4' > $HOME/.vimrc
```
[/details]
[details="file chooser"]
```bash
gsettings set org.gtk.Settings.FileChooser sort-directories-first true
gsettings set org.gtk.Settings.FileChooser window-position '(0, 0)'
gsettings set org.gtk.Settings.FileChooser window-size '(800, 500)'
```
[/details]
<br>

[details="appearance"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="xsettings" version="1.0">
  <property name="Net" type="empty">
    <property name="ThemeName"     type="string" value="Arc-Dark"/>
    <property name="IconThemeName" type="string" value="gnome"/>
  </property>
</channel>' > $xfce_cfg_dir/xsettings.xml
```
[/details]
[details="file manager"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="thunar" version="1.0">
  <property name="last-location-bar"  type="string" value="ThunarLocationButtons"/>
  <property name="last-show-hidden"   type="bool"   value="true"/>
  <property name="last-view"          type="string" value="ThunarCompactView"/>
  <property name="last-window-height" type="int"    value="550"/>
  <property name="last-window-width"  type="int"    value="850"/>
</channel>' > $xfce_cfg_dir/thunar.xml
```
[/details]
[details="mouse and touchpad"]
```bash
touchpad_name=$(xinput list --name-only \
    | grep -i touchpad \
    | sed -e '/Synaptics/ d' \
          -e 's/://g' \
          -e 's/ /_/g')

echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="pointers" version="1.0">
  <property name="'$touchpad_name'" type="empty">
    <property name="Properties" type="empty">
      <property name="libinput_Tapping_Enabled" type="int" value="1"/>
    </property>
  </property>
</channel>' > $xfce_cfg_dir/pointers.xml
```
[/details]
[details="notifications"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-notifyd" version="1.0">
  <property name="expire-timeout" type="int" value="5"/>
</channel>' > $xfce_cfg_dir/xfce4-notifyd.xml
```
[/details]
[details="panel"]
```bash
panel_cfg=$xfce_cfg_dir/xfce4-panel.xml

add_panel_launcher ()
{
    if [[ $# -ne 0 ]]
    then
        local launcher_dir=$HOME/.local/share/applications/
        local launcher_file=org.qubes-os.vm.$1.$2
        xfce4-panel --add=launcher $launcher_dir/$launcher_file
        add_panel_launcher ${@:3}
    fi
}
add_panel_launcher \
    vault     $password_manager_entry \
    personal  $file_manager_entry \
    daily-web $web_browser_entry \
    daily-web $file_manager_entry \
    work      $code_editor_entry \
    work      $file_manager_entry

sleep 7
# move new launchers to the left
ids_begin=$(($(sed -n '/plugin-ids/ =' $panel_cfg) + 1))
ids_count=$(($(sed -n '/plugin-ids/,/property/ p' $panel_cfg | wc -l) - 2))
launcher_end=$(($ids_begin + $ids_count - 1))
launcher_begin=$(($launcher_end - 5))

launcher_saved=$(sed -n "$launcher_begin,$launcher_end p" $panel_cfg)
sed -i -e "$launcher_begin,$launcher_end d" \
       -e "$ids_begin r"<(echo "$launcher_saved") \
    $panel_cfg

# remove workspace switcher
sed -i '/value="pager"/ d' $panel_cfg
```
[/details]
[details="power manager"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-power-manager" version="1.0">
  <property name="xfce4-power-manager" type="empty">
    <property name="inactivity-on-ac" type="uint" value="90"/>
  </property>
</channel>' > $xfce_cfg_dir/xfce4-power-manager.xml
```
[/details]
[details="pulseaudio volume control"]
```bash
# switch off microphone
amixer set Capture nocap
```
[/details]
[details="screensaver"]
```bash
echo 'mode: off' > $HOME/.xscreensaver

echo '
[Desktop Entry]
Hidden=true' > $HOME/.config/autostart/xscreensaver.desktop
```
[/details]
[details="session and startup"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-session" version="1.0">
  <property name="general" type="empty">
    <property name="AutoSave"   type="bool" value="false"/>
    <property name="SaveOnExit" type="bool" value="false"/>
  </property>
</channel>' > $xfce_cfg_dir/xfce4-session.xml
```
[/details]
[details="window manager"]
```bash
echo '<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="theme"             type="string" value="Arc-Dark"/>
    <property name="button_layout"     type="string" value="O|HMC"/>
    <property name="mousewheel_rollup" type="bool"   value="false"/>
    <property name="workspace_count"   type="int"    value="1"/>
  </property>
</channel>' > $xfce_cfg_dir/xfwm4.xml
```
[/details]
[details="xfce terminal"]
```bash
echo '[Configuration]
MiscDefaultGeometry=80x50
ScrollingUnlimited=TRUE
MiscShowUnsafePasteDialog=FALSE' > $cfg_dir/xfce4/terminal/terminalrc
```
[/details]
[details="xterm"]
```bash
echo 'xterm*background: black
xterm*foreground: white
xterm*faceName: monospace
xterm*faceSize: 12
xterm*geometry: 80x40
xterm*saveLines: 100000
xterm*selectToClipboard: true' > $HOME/.Xresources
```
[/details]

```bash
fi ## end: fresh install
```


## Remarks
---
Please, use your search engine for Qubes OS unspecific questions.
All the answers you are looking for can be found on many websites, really.

This complete example should help you to start your own script.
The Qubes way is to use Salt. [qubes-os.org/doc/salt/](https://qubes-os.org/doc/salt/)

Don't hesitate to ask if something is not clear.
Good luck.


[details="latest edit"]
- fix typo in switch templates (excepted -> expected)
- change libreoffice icon theme to colibre_dark_svg
- set gnome interface color-scheme to prefer-dark
[/details]

<div data-theme-toc="true"> </div>