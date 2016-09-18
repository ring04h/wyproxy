# PPTP VPN support
## 安装pptp服务器
安装PPP, PPTP   
```
# yum install -y ppp
# rpm -ivh http://static.ucloud.cn/pptpd-1.3.4-2.el6.x86_64.rpm
```
注：32位请安装i686版本，将上面链接中的“x86_64”改为“i686”即可，请根据自己的OS安装相应的版本。   

```shell   
# 编辑pptp.conf，在最后加入以下两行代码

$ vim /etc/pptpd.conf
localip 10.8.0.1   
remoteip 10.8.0.10-100   

# 编辑options.pptpd，在最后加入以下两行代码   
   
$ vim /etc/ppp/options.pptpd
ms-dns 8.8.8.8
ms-dns 8.8.4.4

# 编辑chap-secrets，account为pptp登录帐号，password为登录密码，其他默认
   
$ vim /etc/ppp/chap-secrets
# client        server      secret            IP addresses
  account       pptpd       password          *

# 编辑sysctl.conf，开启网络转发功能

$ vim /etc/sysctl.conf
net.ipv4.ip_forward = 1
# sysctl -p

# 配置NAT
$ iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE 
$ iptables-save > /etc/sysconfig/iptables

# 启动PPTP服务
$ service pptpd start

# 设置为开机启动

$ chkconfig pptpd on
$ chkconfig iptables on
```

## 设置iptables防火墙转发   
   
```bash
$ iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
$ iptables -t nat -A PREROUTING -s 10.8.0.0/24 -i ppp+ -p tcp -m multiport --dports 80,81,82,83,88,8000,8001,8002,8080,8081,8090 -j DNAT --to-destination 10.8.0.1:8080
$ iptables -t nat -A PREROUTING -s 10.8.0.0/24 -i ppp+ -p tcp -m multiport --dports 443,8443 -j DNAT --to-destination 10.8.0.1:8080
```

## 参考
* https://docs.ucloud.cn/software/vpn/pptp4centos