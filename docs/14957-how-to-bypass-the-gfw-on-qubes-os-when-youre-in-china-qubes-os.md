很多中国人在刚使用Qubes OS的时候都会被翻墙的问题难住，但Qubes OS的官方文档和官方社区却缺少使用clash等软件的教程。本文旨在提供多个可行的翻墙方法供各位选择。

> Many Chinese people are stumped by the problem of bypassing the GFW when they first use Qubes OS, but the official documentation and official community of Qubes OS lacks tutorials for using clash and other software. The purpose of this article is to provide several feasible ways to bypass the GFW for you to choose.

因为Qubes OS实际上是一个虚拟机平台，所以我们实际上是在设置一系列虚拟机，让某些虚拟机成为其他虚拟机的网关，从而达到全局翻墙的目的。

> Because Qubes OS is actually a virtual machine platform, we are actually setting up a series of virtual machines so that certain virtual machines become gateways for other virtual machines to bypass the GFW.

这里的翻墙方案默认提供的是对国内分流的方案，分流方案默认在访问国内网站的时候不使用代理服务器且拦截广告流量，如果你需要隐藏你的真实IP的话你可能需要修改相应的配置来实现强制全局代理和使用国外DNS服务器

> The default wall solution here will split the traffic, it won't use a proxy when visiting Chinese websites server and it will block ads, if you need to hide your real IP then you may need to modify the corresponding configuration to achieve a mandatory global proxy and use non-Chinese DNS servers.

> For non-Chinese: the Great Firewall(the GFW) is a complex mechanism that filter every request between China and the internet outside China. It would try to block Youtube, Telegram, Tor, Duckduckgo and any other things that is considered "harmful" with technology like DNS pollution, SNI sniffing and more. The debate on whether it is good is controversial in China, lots of people says it keep those people, who is too stupid to recognize lies, safe from being infected by western media like BBC, but some other Chinese thinks it limits the freedom of speech. There's lots of open source softwares like shadowsocks, v2ray, trojan and clash targets at bypassing it. Most of the softwares can connect to the proxy server outside China using some kind of encrypted proxy protocol and provide a SOCKS5 inbound for the user to use. Some of them (like Clash.Meta and sing-box) can take over the whole system with TPROXY/REDIRECT/TUN. OpenVPN is not popular in China because it works poorly against the GFW.

# 方法一：在TemplateVM上安装翻墙软件

> Method 1: Installing GFW-bypassing software on TemplateVM

这个方法是所有方案中最简单，但也最危险的方法，建议在无法使用其他方案的情况下再使用本方法

> This method is the simplest of all options, but also the most **dangerous**, it is recommended to use this method when other options are not available

在这个方案中，如果你的某个Qube遭受入侵，那你的代理配置(连接密码，入口IP等等)也会随之暴露

> In this method, if one of your Qubes is compromised, your proxy configuration (connection password, entry IP, etc.) will be leaked as well.

很遗憾的是v2raya在没有网络的情况下无法正常进行配置，v2raya在第一次打开的时候需要同步geoip等文件，导致第一次打开v2raya时**必须**为其设置一个netvm, 否则v2raya无法加载webui

> Unfortunately, v2raya cannot be configured properly without a network. v2raya needs to synchronize geoip and other files when it is opened for the first time, so when opened it for the first time, you **must** set a netvm for it, otherwise v2raya cannot load webui.

其他软件，比如说clashy，可以正常运行，但是其同样需要网络更新订阅文件。

> Other software, such as clashy, works fine, but its also requires the network to update the subscription file.

你只需要在你的TemplateVM上像操作普通Linux发行版一样配置你想要的软件即可，关闭TemplateVM并重启对应的AppVM后即可正常使用。

> You just need to configure the software you want on your TemplateVM as if it were a normal Linux distribution, close the TemplateVM and restart the corresponding AppVM and it will work fine.

注意：订阅等也需要在TemplateVM上设置，更新订阅的时候如果提示没网，你可能需要临时为你的TemplateVM设置一个netvm(这也正是为什么这个方法非常危险)

> Note: subscriptions, etc. also need to be set up on the TemplateVM, and you may need to temporarily set up a netvm for your TemplateVM if prompted for no network when updating subscriptions (which is exactly why this method is very dangerous)

# 方法二：使用任意代理加sing-box网关

> Method 2: Use any proxy software with sing-box gateway

这个方案分为两个qube

> This method includes two qubes.

代理 Qube：负责连接云服务器，提供稳定的翻墙方式，对sing-box网关提供一个socks5接口

> Proxy Qube: responsible for connecting to the cloud server, providing a stable way to bypass the GFW, providing a socks5 interface to the sing-box gateway

SingBox Qube：负责作为netvm处理并分流其他qube发出的流量，劫持DNS请求并发向对应的DoH/DoT服务器，提供一个tun接口，将所有发来的流量发向socks5接口

> SingBox Qube: responsible for processing and diverting traffic sent by other qube as netvm, hijacking DNS requests and sending them to the corresponding DNS servers with DoH/DoT, providing a TUN interface to send all traffic to the socks5 interface.

这个方案可以保护代理服务器的配置不会泄漏，也可以保证各类请求必然通过sing-box代理软件，提供更高的安全性(因为你可以控制所有流量)，同时本方案兼容其他机器的clash方案，你可以利用本方案在手机电脑上使用一样的clash配置，但本方案的网速较慢(主要是下载软件时需要几秒才能提升到最大网速)

> This method can protect the configuration of the proxy server from leaking, and also to ensure that all kinds of requests must pass through the sing-box proxy software, providing higher security(so that you can route everything), and this method allows you to use the same configuration as your phone when using clash, but the network speed of this program is a little bit slow (mainly when downloading software takes a few seconds to upgrade to the maximum network speed)

教程：

> tutorials:

- 首先新建上方的两个qube, 在代理Qube上按照各个软件的教程配置上你想要的软件(v2ray/clash/......)，配置完后需要在设置中打开允许LAN

- > First of all, create two new qube above, configure the software you want on the proxy Qube in accordance with the tutorials of the software you like (v2ray/clash/......) After the configuration, you need to turn on Allow LAN in the settings

- 设置完后，在设置中找到软件暴露在外的socks5端口(如果是clash的话也可以是mixed port)，按照[这个教程](https://www.qubes-os.org/doc/firewall/#enabling-networking-between-two-qubes)把这个端口暴露给另一个qube

- > After setting it up, find the socks5 port exposed by the software in the settings (or mixed port if it's clash) and follow [this tutorial](https://www.qubes-os.org/doc/firewall/#enabling-networking-between-two-qubes) to expose this port to another qube

- 打开SingBox Qube的终端，输入`ALL_PROXY=socks://代理Qube的IP:代理Qube的端口 curl ip.me`。如果以上步骤正确的话，你应该可以看到代理的出口IP
  
  - 假如说你的代理Qube的IP为`10.137.0.123`，暴露的端口为`7890`，那你应该输入`ALL_PROXY=socks://10.137.0.1234:7890 curl ip.me`

- > Open SingBox Qube's terminal and type `ALL_PROXY=socks://<ProxyQubeIP>:<ProxyQubePort> curl ip.me`. If the above steps are correct, you should see the proxy's exit IP
  
  - > Say your proxy Qube has an IP of `10.137.0.123` and an exposed port of `7890`, then you should enter `ALL_PROXY=socks://10.137.0.123:7890 curl ip.me`

- 在Singbox Qube上安装sing-box，然后在`/etc/sing-box/config.json`填入以下设置，并在设置中填入你的IP和端口：

- > Install sing-box on Singbox Qube, then fill in the following settings in `/etc/sing-box/config.json` and fill in your IP and port in the settings.

- 这个配置通过代理使用`tls://1.1.1.1`来解析国外的网站，使用`223.5.5.5`来解析国内的网站

- > This configuration uses `tls://1.1.1.1`  through proxy to resolve foreign sites and `223.5.5.5` to resolve Chinese sites.

```json
{
  "dns": {
    "servers": [
      {
        "tag": "cf",
        "address": "tls://1.1.1.1"
      },
      {
        "tag": "local",
        "address": "223.5.5.5",
        "detour": "direct"
      }
    ],
    "rules": [
      {
        "geosite": "cn",
        "server": "local"
      }
    ],
    "strategy": "ipv4_only"
  },
  "inbounds": [
    {
      "type": "tun",
      "inet4_address": "172.202.0.1/30",
      "auto_route": true,
      "strict_route": true,
      "sniff": true
    }
  ],
  "outbounds": [
    {
      "type": "socks",
      "tag": "proxy",
      "version": "5",
      "server": "代理Qube的IP",
      "server_port": 代理Qube的端口
    },
    {
      "type": "direct",
      "tag": "direct"
    },
    {
      "type": "block",
      "tag": "block"
    },
    {
      "type": "dns",
      "tag": "dns-out"
    }
  ],
  "route": {
    "rules": [
      {
        "protocol": "dns",
        "outbound": "dns-out"
      },
      {
        "geosite": "category-ads-all",
        "outbound": "block"
      },
      {
        "geosite": "cn",
        "geoip": "cn",
        "outbound": "direct"
      },
      {
        "geosite": "private",
        "geoip": "private",
        "outbound": "direct"
      }
    ],
    "auto_detect_interface": true
  }
}
```

- 在SingBox Qube中执行`sudo systemctl restart sing-box`重启sing-box，然后在设置中打开`provide network`将SingBox Qube变成netvm

- > Execute `sudo systemctl restart sing-box` in SingBox Qube to restart sing-box, then turn on `provide network` in the settings to turn SingBox Qube into netvm

- 最后将你想要翻墙的Qube的netvm设置为SingBox Qube

- > Finally, set the netvm of the Qube you want it to bypass GFW to SingBox Qube