#!/usr/bin/env python
# encoding: utf-8

'''代理服务器健康监控工具
health check tool, 
if wyproxy is error, then restart the proxy server.
$ python wyproxy.py -restart
: wyporyx.py need add -conf options
'''

from __future__ import (absolute_import, print_function, division)

import os
import json
import subprocess

"""health check conf"""
bind_addr = '106.75.199.107'
url = 'http://www.baidu.com/wy'

def read_cnf():
    args = json.load(open('../.proxy.cnf', 'r'))
    return args

def run_command(*arguments):
    return subprocess.check_output(['curl']+ list(arguments))

def check_live():
    # curl --proxy 106.75.199.107:8080 http://www.baidu.com/wyproxy
    # curl --socks5-hostname 106.75.199.107:8080 http://www.baidu.com/wyproxy
    try:
        args = read_cnf()
        if args.get('mode') == 'socks5':
            opt = '--socks5-hostname'
        elif args.get('mode') == 'http':
            opt = '--proxy'
        server = '{}:{}'.format(bind_addr, args.get('port'))
        result = run_command('-q', opt, server, url, '--connect-timeout', '5')
        return False if 'Failed to connect' in result else True
    except Exception as e:
        return False

def restart_wyproxy(pidfile):
    return subprocess.check_output('python','wyproxy.py','--restart','--pid', pidfile)

def main():
    print(check_live())
    # print(result)
    # print(check_live())
    # print(__file__)
    # print(os.path.realpath(__file__))
    # print(os.path.dirname(os.path.realpath(__file__)))
    # pwd = os.environ['PWD']
    # print(pwd)
    # print(os.getcwd())

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print('error: {}'.format(e))