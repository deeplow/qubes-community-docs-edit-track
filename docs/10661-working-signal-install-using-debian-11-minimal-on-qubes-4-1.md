1.copy the following code to a script.sh file 
2. move to dom0
3. execute
This assumes you have debian 11-minimal installed

> #!/bin/bash                                                                                                                                                                                                        
> qvm-clone debian-11-minimal t-social-deb-11-min
> qvm-run --pass-io -u root t-social-deb-11-min 'sudo apt install --no-install-recommends  qubes-core-agent-networking qubes-core-agent-nautilus dunst curl -y'
> qvm-run --pass-io -u root t-social-deb-11-min 'sudo apt upgdate'
> qvm-run --pass-io -u root t-social-deb-11-min 'sudo apt upgrade'
> qvm-run --pass-io -u root t-social-deb-11-min 'curl --proxy http://127.0.0.1:8082/ https://updates.signal.org/desktop/apt/keys.asc  | apt-key add -'
> qvm-run --pass-io -u root t-social-deb-11-min 'echo "deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main" | tee -a /etc/apt/sources.list.d/signal-xenial.list'
> qvm-run --pass-io -u root t-social-deb-11-min 'apt update '
> qvm-run --pass-io -u root t-social-deb-11-min 'apt full-upgrade'
> qvm-run --pass-io -u root t-social-deb-11-min 'apt install --no-install-recommends signal-desktop'