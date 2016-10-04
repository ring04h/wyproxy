# wyproxy
Proxying And Recording HTTP/HTTPs and Socks5, Save To Mysql Database.  

HTTP/HTTPS, Socks5代理服务器, 并可以将网络请求记录保存到后台数据库.   
     
帮助安全测试人员更加便捷的发现(客户端/APP/网页)中隐藏的接口或资源。     

同时支持流量handle回放数据功能,    
在HTTP Header中插入 移动/联通/电信 营业厅的免流量域名头, 实现免流量代理上网。   
   
演示服务器：http://s5.wuyun.org:5000   
代理服务器：s5.wuyun.org , socks5: 8080   
    
支持场景    
- iPhone App
- iPad App
- Mac OS X App
- Android APP

## 帮助说明    

```bash
$ python wyproxy.py -h
usage: wyproxy.py [-h] [-d] [-stop] [-restart] [-pid] [-p] [-m] [-us]

wyproxy v 1.0 ( Proxying And Recording HTTP/HTTPs and Socks5)

optional arguments:
  -h, --help           show this help message and exit
  -d, --daemon         start wyproxy with daemond
  -stop, --stop        stop wyproxy daemond
  -restart, --restart  restart wyproxy daemond
  -pid , --pidfile     wyproxy daemond pidfile name
  -p , --port          wyproxy bind port
  -m , --mode          wyproxy mode (HTTP/HTTPS, Socks5, Transparent)
  -us, --unsave        Do not save records to MySQL server

```

记录字段如下   

![github](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/captrue.png "github")   

- method    (HTTP/HTTPS/OPTIONS)
- scheme    (http/https/ftp)
- host      (www.wuyun.org)
- port      (80/8080)
- url       (https://www.wuyun.org/foo/bar.php?id=1)
- path      (/foo/bar.php)
- extension (php)
- query     (id=1)
- headers   (response headers)
- content   (response contnet)
- request_headers  (reqeust client headers)
- request_content  (request data: liked post data)
- status_code      (200/404/403)
- date_start       (unix timestamp)
- date_end         (unix timestamp)

## 环境要求
- CentOS 6.4
- Python 2.7
- Mysql Server

### 开发环境依赖
```bash
$ yum install python-devel libxml2-devel libxslt-devel libjpeg-turbo-devel libffi-devel mysql-devel
```

### 编译安装Python2.7环境
```
$ wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz
$ tar zvxf Python-2.7.8.tgz
$ cd Python-2.7.8
$ ./configure
$ make
$ make install
$ mv /usr/bin/python /usr/bin/python2.6.6  
$ ln -s /usr/local/bin/python2.7 /usr/bin/python
```
重启bash终端, 就拥有新的Python2.7环境了

### 安装新的Python2.7环境下的pip
https://pip.pypa.io/en/latest/installing/
```bash
$ wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
$ python get-pip.py
```

yum在Python2.7环境下无法使用，需要让它使用python2.6.6的环境
```bash
$ vim /usr/bin/yum # 修改第一行的程序执行环境
#!/usr/bin/python   ->    #!/usr/bin/python2.6.6
```

### 获取代码
```bash
$ yum install git
$ mkdir src
$ cd ./src
$ git clone https://github.com/ring04h/wyproxy.git
```

### 安装python依赖库
```
$ pip install -r requirements.txt
```

### 安装MYSQL数据库
```bash
$ yum install mysql-server
$ service mysqld start
$ mysql -uroot -p < wyproxy.sql
```

### 性能优化
MYSQL配置调优, 有时候网页的content内容size大于1M,    
需要修改MYSQL配置调优的全局配置文件max_allowed_packet, 允许插入的数据大小为64M.   
   
```bash
$ vim /etc/my.cnf
[mysqld] # 位置
max_allowed_packet = 64M
```
   
Open Max file option:    

```bash
$ echo ulimit -HSn 65536 >> /etc/rc.local
$ echo ulimit -HSn 65536 >> ~/.bash_profile
```

### 开发环境

或者你可以配置和启动一个virtualenv环境来独立运行wyproxy.   

```bash
$ virtualenv --no-site-packages wyproxy
$ cd wyproxy
$ source bin/activate
```

### 启动wyproxy
> 如果不想将代理记录保存到数据库, 必须指定 -us 或者 --unsave 参数
   
普通方式启动   

```bash
$ python wyproxy.py -p 8080 -m socks5 --unsave
```   

守护进程方式启动

```bash
$ python wyproxy.py -p 8080 -m socks5 --unsave -d
```

### 支持HTTPS, 需要配置客户端 SSL 证书
#### iPhone 移动端, 使用Safari浏览器打开
https://raw.githubusercontent.com/ring04h/wyproxy/master/ssl/mitmproxy-ca.pem    
会有如下图片提示, 点击右上角安装, 使证书状态变为绿色生效

安装界面    
    
![install_pem](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/install_pem.png)

成功后的界面   

![install_pem_succ](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/install_pem_succ.png)   

#### Mac OS X 安装配置 SSL 证书 并信任
```bash
$ wget https://raw.githubusercontent.com/ring04h/wyproxy/master/ssl/mitmproxy-ca.pem
```
在Finder中双击运行mitmproxy-ca.pem

进入钥匙串访问工具, 选择mitmproxy的证书
![key_manager](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/key_manager.png "key_manager")   
   
选择始终信任该证书, 即可生效, 便能成功捕捉所有HTTPS的流量
![key_trust](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/key_trust.png "key_trust")   

### iPhone配置全局Socks5代理支持   
用代理自动配置文件pac给iPhone和iPad设备添加socks代理    

首先启动wyproxy代理服务器, 设置代理类型为socks5    
    
```
$ python wyproxy.py -p 8080 -m socks5 -d
```
    
找一台开启了HTTPD服务的服务器, 新建一个.pac文件, 内容如下    
    
```pac
function FindProxyForURL(url, host)
{
    if (isInNet(host, "192.168.199.0", "255.255.255.0"))
        return "DIRECT";

    return "SOCKS 106.75.147.67:8080";
}
```
     
设置iPhone的无线配置, 代理处填上你的HTTPD服务器地址    
http://s5.wuyun.org/s5.pac   

![enable_s5](https://raw.githubusercontent.com/ring04h/wyproxy/master/screenshot/enable_s5.png "enable_s5")   
    
这样iPhone上面, 所有的流量，全都会经过wyproxy的socks5代理了

## 使用技巧
### 在单服务器运行多个代理服务
运行socks5服务, 监听1080端口   
   
```bash
$ python wyproxy.py -p 1080 -m socks5 -pid /tmp/1080.pid -d
wyproxy daemon starting...
wyProxy daemon started successfully 
2016-09-14 17:11:20,333 [INFO] wyproxy is starting...
2016-09-14 17:11:20,334 [INFO] Listening: 0.0.0.0:1080 socks5
2016-09-14 17:11:20,390 [INFO] wyproxy started successfully...
```

停止1080端口的服务   
   
```bash
$ python wyproxy.py -stop -pid /tmp/1080.pid
wyproxy daemon stopping...
wyproxy daemon stopped successfully
```
   
运行socks5服务, 监听1081端口   
   
```bash
$ python wyproxy.py -p 1081 -m socks5 -pid /tmp/1081.pid -d
wyproxy daemon starting...
wyProxy daemon started successfully 
2016-09-14 17:11:27,564 [INFO] wyproxy is starting...
2016-09-14 17:11:27,566 [INFO] Listening: 0.0.0.0:1081 socks5
2016-09-14 17:11:27,583 [INFO] wyproxy started successfully...
```

停止1081端口的服务   
   
```bash
$ python wyproxy.py -stop -pid /tmp/1081.pid
wyproxy daemon stopping...
wyproxy daemon stopped successfully
```
   
# PPTP VPN support
## wyproxy代理服务器设置
做NAT代理转发,必须启动代理服务器的模式为 transparent   
   
```shell
$ python wyproxy.py -p 8080 -m transparent -d
```
   
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

# 编辑chap-secrets，account为wyproxy登录帐号，1234qwer为登录密码，其他默认 
$ vim /etc/ppp/chap-secrets
# client      server    secret          IP addresses
wyproxy       pptpd       1234qwer          *

# 编辑sysctl.conf，开启网络转发功能
$ vim /etc/sysctl.conf
net.ipv4.ip_forward = 1
$ sysctl -p

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
$ iptables -t nat -A PREROUTING -s 10.8.0.0/24 -i ppp+ -p tcp -m multiport --dports 80,81,82,83,88,8000,8001,8002,8080,8081,8090 -j DNAT --to-destination 10.8.0.1:8080
$ iptables -t nat -A PREROUTING -s 10.8.0.0/24 -i ppp+ -p tcp -m multiport --dports 443,8443 -j DNAT --to-destination 10.8.0.1:8080
$ iptables-save > /etc/sysconfig/iptables
$ service iptables restart
```

## 参考
* https://docs.ucloud.cn/software/vpn/pptp4centos
