## Mac OS X 系统代理设置器
通过修改[系统网卡设备]的代理配置项, 实现[系统数据]都通过发送。
Enable/Disable OS X network device proxy and wrap wyproxy

## 使用帮助

```bash
usage: warpper.py [-h] [-d] [-ip] [-p] [-m]

Enable/Disable OS X network device proxy and wrap wyproxy

optional arguments:
  -h, --help       show this help message and exit
  -d, --disable    Disable wyproxy OS X device
  -ip , --ipaddr   override the default ipaddr of 127.0.0.1
  -p , --port      override the default port of 8080
  -m , --mode      wyproxy mode (http, socks5)
```

### 配置代理

wyproxy服务器
IP地址: proxy.wuyun.org
代理端口: 19191
代理类型: socks5

```bash
$ sudo python warpper.py -ip proxy.wuyun.org -p 19191 -m socks5
Enabling proxy on socks5 proxy.wuyun.org 19191...
Enable proxy successfully...
```

IP地址: proxy.wuyun.org
代理端口: 19191
代理类型: http/https

```bash
$ sudo python warpper.py -ip proxy.wuyun.org -p 19191 -m http
Enabling proxy on http proxy.wuyun.org 19191...
Enable proxy successfully...
```

### 禁用代理功能
```bash
$ sudo python warpper.py -d
Disabling proxy on Wi-Fi...
Disable all proxy successfully...
```

