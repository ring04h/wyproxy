# wyproxy
Proxying And Recording HTTP/HTTPs and Socks5, Save To Mysql Database.  

HTTP/HTTPS, Socks5代理服务器, 并可以将网络请求记录保存到后台数据库，   
帮助安全测试人员更加便捷的发现(客户端/APP/网页)中隐藏的接口或资源。     

同时支持流量handle回放数据功能,    
在HTTP Header中插入 移动/联通/电信 营业厅的免流量域名头, 实现免流量代理上网。   
    
支持场景    
- iPhone App
- iPad App
- Mac OS X App
- Android APP

## 帮助说明    

```bash
$ python wyproxy.py -h
usage: wyproxy.py [-h] [-d] [-stop] [-restart] [-pid] [-p] [-m]

wyproxy v 1.0 ( Proxying And Recording HTTP/HTTPs and Socks5)

optional arguments:
  -h, --help           show this help message and exit
  -d, --daemon         start wyproxy with daemond
  -stop, --stop        stop wyproxy daemond
  -restart, --restart  restart wyproxy daemond
  -pid , --pidfile     wyproxy daemond pidfile name
  -p , --port          wyproxy bind port
  -m , --mode          wyproxy mode (HTTP/HTTPS, Socks5, Transparent)

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

### 开发环境

或者你可以配置和启动一个virtualenv环境来独立运行wyproxy.   

```bash
$ virtualenv --no-site-packages wyproxy
$ cd wyproxy
$ source bin/activate
```

### 启动wyproxy

普通方式启动   

```bash
$ python wyproxy.py -p 8080 -m socks5
```   

守护进程方式启动

```bash
$ python wyproxy.py -p 8080 -m socks5 -d
```

### 性能优化
Open Max file option:    

```bash
$ echo ulimit -HSn 65536 >> /etc/rc.local
$ echo ulimit -HSn 65536 >> ~/.bash_profile
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