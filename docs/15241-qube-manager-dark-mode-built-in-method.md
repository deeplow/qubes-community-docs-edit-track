# Qube Manager & Tools: Dark Mode
---
Add an option in the view menu to enable/disable dark mode.

The script must be launch in a dom0 terminal.

Make sure to have only `space` character for python part.
If you have `tab` character, qube manager will fail to start.

Dark mode can be set in the qube-manager config file:
 `$HOME/.config/The Qubes Project/qubes-qube-manager.conf`
```
[view]
darkmode=true
```

## Stylesheet
Colors are based on Arc-Dark theme.
You can extract the css file from your theme with `gresource`.
```bash
qubes_cfg_dir="$HOME/.config//The Qubes Project/"
dark_stylesheet=dark-stylesheet.css
echo '
QMenu {
    border: 1px solid #252A32;
}

::separator {
    background-color: #475970;
    height: 1px;
    width: 1px;
}

:disabled {
    color: gray;
}

::tab:!selected {
    background-color: #2F343F;
}

::tab:!selected:hover {
    background-color: #505666;
}

* {
    color: #D3DAE3;
    background-color: #383C4A;
    alternate-background-color: #404552;
    selection-background-color: #5294E2;
}' > "$qubes_cfg_dir/$dark_stylesheet"
```

## Function
Terms to feed to your favorite search engine:
  - bash sed
  - bash <()
  - bash function $#
  - bash function $@
  - bash if [[ ]]
  - bash recursive function

Bash command `<()` doesn't handle sudo.
Just like file redirection (`text > file`) doesn't.

A backup file is made for each file!
```bash
python_version=$(python3 --version | grep -Eo '[0-9]+\.[0-9]+')
qm_dir=/usr/lib/python$python_version/site-packages/qubesmanager/
add_data_after_pattern ()
{
    handle_data ()
    {
        if [[ $# -ne 1 ]]
        then
            sed -i -E "/$2/ r"<(echo "$3") $1
            handle_data $1 "${@:4}"
        fi
    }
    local qtool=$qm_dir/$1
    local qtmp=$HOME/$1

    if [ ! -f $qtool.bak ]; then
        sudo cp $qtool $qtool.bak
    fi
    sudo cp $qtool $qtmp
    sudo chown user:user $qtmp

    handle_data $qtmp "${@:2}"

    sudo mv $qtmp $qtool
    sudo chown root:root $qtool
}
```

## Qubes tools
If setting is set to dark mode, use our css stylesheet.
```bash
add_dark_mode ()
{
    local qm_darkmode="
        if not parent:
            manager_settings = QtCore.QSettings(
                'The Qubes Project', 'qubes-qube-manager')
        else:
            manager_settings = QtCore.QSettings(self)
        if manager_settings.value('view/darkmode',
                                  defaultValue='false') != 'false':
            qubes_cfg_dir = '$qubes_cfg_dir'
            stylesheet = open(qubes_cfg_dir + '$dark_stylesheet', 'r')
            self.setStyleSheet(stylesheet.read())
            stylesheet.close()"
    for qtool_file in $@
    do
        add_data_after_pattern $qtool_file 'setupUi' "$qm_darkmode"
    done
}
add_dark_mode \
    global_settings.py \
    settings.py \
    template_manager.py \
    create_new_vm.py \
    clone_vm.py \
    backup.py \
    restore.py \
    log_dialog.py

sudo sed -i 's/^from PyQt5 import /&QtCore, /' $qm_dir/log_dialog.py
```

## Qube manager
Add a toggle option in the view menu.
```bash
qm_set_darkmode="
    @pyqtSlot(bool)
    def on_action_dark_mode_toggled(self, checked):
        if checked:
            qubes_cfg_dir = '$qubes_cfg_dir'
            stylesheet = open(qubes_cfg_dir + '$dark_stylesheet', 'r')
            self.setStyleSheet(stylesheet.read())
            stylesheet.close()
        else:
            self.setStyleSheet('')
        if self.settings_loaded:
            self.manager_settings.setValue('view/darkmode', checked)"

qm_menu () {
    echo "        self.menu_view.addAction(self.$1)"
}
qm_darkmode_menu=$(qm_menu action_dark_mode)

qm_restore () {
    echo "
        if self.manager_settings.value('$1',
                                       defaultValue='false') != 'false':
            self.action_dark_mode.setChecked(True)"
}
qm_darkmode_restore=$(qm_restore 'view/darkmode')

add_data_after_pattern qube_manager.py \
    'self\.close' "$qm_set_darkmode" \
    'compact_view\.setChecked' "$qm_darkmode_restore" \
    'Action\(self\.action_compact_view' "$qm_darkmode_menu"
```

Create the Qt widget to handle dark mode. (Qt is the gui framework)
```bash
qm_widget () {
    echo "
        self.$1 = QtWidgets.QAction(VmManagerWindow)
        self.$1.setCheckable(True)
        self.$1.setChecked($2)
        self.$1.setObjectName('$1')"
}
qm_darkmode_widget=$(qm_widget action_dark_mode 'False')

qm_text () {
    echo "        self.$1.$2(_translate('VmManagerWindow', '$3'))"
}
qm_darkmode_text=$(qm_text action_dark_mode setText 'Dark mode')

add_data_after_pattern ui_qubemanager.py \
    '"action_compact_view"' "$qm_darkmode_widget" \
    'Compact view' "$qm_darkmode_text"
```

## Note
qube manager version: 4.1.25-1
Dark mode will be erase if qube manager get updated.