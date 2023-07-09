As a reference from this [topic](https://forum.qubes-os.org/t/error-126-while-updating-the-os-from-terminal/10597), there is only one solution.

In order to fix error 126, the first thing is to edit /etc/qubes-rpc/policy/qubes.ConnectTCP as this following for one line only:
> $anyvm $anyvm allow

This way you don't have any errors. 


Another thing that in order to update is this following command in dom0 terminal:
> sudo qubes-dom0-update --action=reinstall binutils

This will update your commands because you are adding something to your machines.

Vola! you are done there, but don't add anything to qubes.ConnectTCP file otherwise all vms cannot update.