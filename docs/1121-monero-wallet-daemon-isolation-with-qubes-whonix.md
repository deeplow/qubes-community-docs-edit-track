Just a heads-up for anyone who is new to setting this up .... Just don't even bother going to the [Official Monero Guide](https://www.getmonero.org/resources/user-guides/cli_wallet_daemon_isolation_qubes_whonix.html). Don't worry, you're not going mad, it's just hopelessly out of date.

I eventually came across [this github guide](https://github.com/0xB44EFD8751077F97/monero-site/blob/6c25a8714b5f7c3863e91dac3fe48472c6b4b253/_i18n/ar/resources/user-guides/wallet_daemon_isolation_qubes_whonix.md#walletdaemon-isolation-with-qubes--whonix) that took all the pain away. Highly recommended.

A few pointers I found as I went:

1.2. Create daemon's AppVM: monerod-ws
	Increased size to 100G

2.2. Create systemd unit
	`sudo kwrite /lib/systemd/system/monerod-mainnet.service`
	Replaced kwrite with nano

3.1.1 Install command-line only tools
	`sudo install -g staff -m 0755 -o root ~/monero-<VERSION NUMBER>/monero-blockchain-* ~/monero-<VERSION NUMBER>/monerod -t /usr/local/bin/`
	For the correct VERSION NUMBER look at /home/user for name of the directory (`monero-x86_64-linux-gnu.v0.17.1.0`). That'll save you a few guesses lol.

4.2 Create communication channel with daemon on boot
	Replace kwrite with nano


There. Now there's my good deed for the day.