# wyproxy
Proxying And Recording HTTP/HTTPs and Socks5, Save To Mysql Database.   
HTTP/HTTPS, Socks5代理服务器, 并可以将请求记录保存到后台数据库。   

记录字段如下:   
- host 
- port
- url
- path
- extension
- headers
- content
- request_headers
- request_content
- method
- scheme
- status_code
- date_start
- date_end

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

### 配置和启动开发环境
```bash
$ virtualenv --no-site-packages wyproxy
$ cd wyproxy
$ source bin/activate
```

### 获取代码
```bash
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
### 启动wyproxy

普通方式启动   

```bash
$ python wyproxy.py -p 8080 -m socks5
```   

守护进程方式启动

```bash
$ python wyproxy.py -p 8080 -m socks5 -d
```