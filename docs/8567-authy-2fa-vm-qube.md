Im sure most of you use 2FA, the more savy would already be using [Authy](https://authy.com/) over google authenticator. I thought of the idea of making a dedicated Authy qube that once setup has no network access, creating a secure, isolated way for me to generate 2FA codes, and act as a backup if ever i lose my phone.

[Setup](https://snapcraft.io/install/authy/fedora):
im using a fedora minimal template

```
sudo dnf install snapd
sudo ln -s /var/lib/snapd/snap /snap
```
restart to update pathways
```
sudo snap install authy
```
refresh applications & add to shortcuts.
launch app.
enter password for decryption.
shutdown VM.
set network VM to none.
Done.

i allocated only 600mb ram, & 1CPU, a little slow to boot, but find once running operates fine. If you do add more accounts to Authy on your phone, i guess you would just enable network temporarily sync them to your Authy VM qube.

Im sure the even more security minded of you probably rock Yubikeys, and i think the same will be possible using the [Desktop Yubico Authenticator](https://www.yubico.com/products/yubico-authenticator/) which also installs via snap. I havent tried this yet though as all my keys are in authy and im too lazy to change atm.