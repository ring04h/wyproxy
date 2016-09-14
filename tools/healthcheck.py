#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, print_function, division)

import sys
sys.path.append("../")

import json
import subprocess
from daemon import Daemon

"""
health check tool, 
if wyproxy is error, then restart the proxy server.
$ python wyproxy.py -restart
: wyporyx.py need add -conf options
"""

def main():
    args = json.load(open('../.proxy.cnf', 'r'))
    print(args)

if __name__ == '__main__':
    main()
