If anyone had been leveraging in-place `dist-upgrade`/`full-upgrade` of `debian-11-minimal` & inadvertently [borked](https://www.urbandictionary.com/define.php?term=borked) their `debian-12-minimal` aka `bookworm` templates (like me :roll_eyes:), here's what I find to be "working" (supporting `salt`/GUI Update) ...

---

Used to work a treat:
---
```sh
apt update && apt upgrade -y && apt autoremove -y
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/qubes-r4.list
apt update && apt upgrade -y && apt full-upgrade -y && apt autoremove -y
```
but, when updated via GUI removes `qubes-core-agent` & `qubes-core-qrexec`. :scream: :grimacing: :scream:

Try something like this instead:
---
```sh
echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
locale-gen en_US.UTF-8
apt update && apt upgrade -y && apt autoremove -y
sed -i 's/#deb \[arch=amd64\] https:\/\/deb.qubes-os.org\/r4.1\/vm bullseye-testing main/deb \[arch=amd64\] https:\/\/deb.qubes-os.org\/r4.1\/vm bullseye-testing main/g' /etc/apt/sources.list.d/qubes-r4.list
sed -i 's/#deb \[arch=amd64\] https:\/\/deb.qubes-os.org\/r4.1\/vm bullseye-securitytesting main/deb \[arch=amd64\] https:\/\/deb.qubes-os.org\/r4.1\/vm bullseye-securitytesting main/g' /etc/apt/sources.list.d/qubes-r4.list
apt update && apt upgrade -y && apt autoremove -y
sed -i 's/non-free/non-free non-free-firmware/g' /etc/apt/sources.list
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/qubes-r4.list
apt update && apt upgrade -y -o Dpkg::Options::=--force-confdef && apt full-upgrade -y && apt autoremove -y
```
---
It's not clear to me why the qubes packages from testing haven't been pushed to the main repo which, would allow the old standard in-place upgrade to work.

Hoping :pray: this helps someone!