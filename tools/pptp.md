# PPTP VPN support
大于 CentOS 6.4   
yum install libevent2 libevent2-devel

小于 CentOS 6.4   
yum install libevent libevent-devel

CentOS 6.4 的内核版本不支持Tproxy, 需要更新到CentOS 7.0

-A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 12345
-A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 12345


iptables -t nat -N REDSOCKS
iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 106.75.147.67 -j RETURN
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345

iptables -t nat -A OUTPUT -p tcp -o eth0 -j REDSOCKS

iptables -t nat -D OUTPUT -p tcp -o eth0 -j REDSOCKS

iptables -t nat -D REDSOCKS -d 106.75.147.67 -j RETURN

// 新建路由转发表中的一个链 REDSOCKS
iptables -t nat -N REDSOCKS

// 设置不需要代理转发的网段
// 目的为墙外代理服务器的数据包一定不能转发
<!-- sudo iptables -t nat -A REDSOCKS -d $SS_SERVER_IP -j RETURN -->

// 目的为局域网和本地回环地址的数据包不用转发
sudo iptables -t nat -A REDSOCKS -d 172.0.0.0/24 -j RETURN
sudo iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN

// 将数据包转发到 redsocks
sudo iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345

// 将 REDSOCKS 链的规则应用到经过 eth0 网卡的数据包
sudo iptables -t nat -A OUTPUT -p tcp -o eth0 -j REDSOCKS
iptables -t nat -A OUTPUT -p tcp -o ppp0 -j REDSOCKS

## 参考
* http://blog.csdn.net/zdy0_2004/article/details/48474721
* http://www.jianshu.com/p/814d57d597aa

