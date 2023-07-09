Hey everyone,

i am trying to get my second storage device permanently mounted to a specific AppVM.
The problem with persistently attaching a block device like this

qvm-block attach -p ...

is that qubes asigns a new name to the device on every restart. 
How can i remedy that?

Is their a better way to add a big storage pool that is flexible and can be shared with multiple AppVMs?