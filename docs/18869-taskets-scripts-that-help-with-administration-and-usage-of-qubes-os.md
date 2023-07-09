https://github.com/tasket/Qubes-scripts

(non-exhaustive list)

- `qubes4-multi-update`: Updates multiple template and standalone VMs

- `configure-sudo-prompt`: Restores internal VM security so that authorization is required to gain root access

- `findpref`: Dom0: Find all VMs that match a pref value, optionally set new values for them. For example, its a handy way to switch all VMs that are using a particular netvm to a different netvm.

- `halt-vm-by-window`: A simple way to shutdown a Qubes VM associated with the currently active window. Before shutdown, any running instances of Firefox or Thunderbird in that VM will be told to quit; this allows the apps to save their open-tabs state.