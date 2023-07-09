Hello everyone, I've written up a tutorial on how to use pass with dmenu in Qubes OS via qrexec. You can check it out here:

https://kenogo.org/blog/20221201.html

I know about the existence of [qubes-pass](https://github.com/Rudd-O/qubes-pass). However, its approach, where the qube in need of a password requests it from the password vault, did not suit me.

For one, it does not allow me to simply set a global keybinding in dom0 for obtaining my passwords. Secondly, I don't like potentially malicious qubes to be able to request a password. I know that you can set your qubes-rpc policy so that the user is always asked for confirmation, so qubes-pass certainly has valid use cases. I just decided to go a different route. Maybe someone finds it interesting or helpful.