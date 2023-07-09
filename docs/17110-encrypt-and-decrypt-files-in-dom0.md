Since tar does not support any encryption capabilities I was looking for a solution to encrypt and decrypt files directly within dom0. I found ccrypt as the most simple and secure solution. But this would also require a dom0 installation...

Option B, make a no network minimal template based appVM and install ccrypt and pilot all via dom0: sending files to appVM -> make a qvm-run --pass-io ... to do the encryption remotely and pass it back to dom0 but this also sounds like a complex workaround.

Any suggestions?