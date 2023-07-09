Currently Qubes DispVM's are not fully ephemeral; by default data written to xvda and xvdb is written to the disk in plaintext. When the user sets ephemeral=True data written to xvdc is encrypted with an ephemeral encryption key placed in RAM. If in addition the user sets rw:root rw 0 then writes to xvda are routed to xvdc and thus encrypted. However xvdb is at present always written to the disk in plaintext. 

I recently wrote a patch for initramfs that resolves this issue; after application of the patch all data written by a PVH DispVM (including to swap) is encrypted by an ephemeral key. The code and a guide is available at 

https://github.com/anywaydense/QubesEphemerize

Hopefully this will find its way to R4.2. The patch has been tested only on the most recent stable R4.1.