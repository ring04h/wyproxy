# wyproxy
Proxying And Recording HTTP/HTTPs and Socks5, Save To Mysql Database.   
HTTP/HTTPS, Socks5代理服务器, 并可以将请求记录保存到后台数据库。   

帮助说明   

```bash
$ python wyproxy.py -h
usage: wyproxy.py [-h] [-d] [-stop] [-restart] [-p] [-m]

wyproxy v 1.0 ( Proxying And Recording HTTP/HTTPs and Socks5)

optional arguments:
  -h, --help           show this help message and exit
  -d, --daemon         start wyproxy with daemond
  -stop, --stop        stop wyproxy daemond
  -restart, --restart  restart wyproxy daemond
  -p , --port          wyproxy bind port
  -m , --mode          wyproxy mode (HTTP/HTTPS, Socks5)
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
$ yum install python-devel libxml2-devel libxslt-devel libjpeg-turbo-devel libffi-devel
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
$ yum install mysql-server mysql-devel
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