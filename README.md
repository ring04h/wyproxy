# wyproxy
Proxying And Recording HTTP/HTTPs and Socks5 to Mysql Database.   

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
$ git clone http://github.com/ring04h/wyproxy.git
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

