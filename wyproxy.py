#!/usr/bin/env python
# encoding: utf-8

import sys
import argparse
import logging

from daemon import Daemon
from mitmproxy import flow, proxy
from mitmproxy.proxy.server import ProxyServer
from untils import ResponseParser, save_cnf, read_cnf
from plugins import MysqlInterface

logging.basicConfig(
    level=logging.INFO,
    # filename='/tmp/wyproxy.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
)

class WYProxy(flow.FlowMaster):

    def __init__(self, server, state):
        super(WYProxy, self).__init__(server, state)
        self.connection = MysqlInterface.init()

    def run(self):
        try:
            logging.info("wyproxy started successfully...")
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()
            logging.info("Ctrl C - stopping wyproxy server")
        finally:
            self.connection.close()

    def handle_request(self, f):
        f = flow.FlowMaster.handle_request(self, f)
        if f:
            f.request.anticache() # disable cache
            # f.request.anticomp()  # disable gzip compress
            f.reply()
        return f

    def handle_response(self, f):
        f = flow.FlowMaster.handle_response(self, f)
        if f:
            parser = ResponseParser(f)
            result = parser.parser_data()
            mysqldb_io = MysqlInterface(self.connection)
            mysqldb_io.insert_result(result)
            f.reply()
        return f

    # def handle_error(self, f):
    #     f = flow.FlowMaster.handle_error(self, f)
    #     if f:
    #         logging.info(f.error)
    #         f.reply()
    #     return f

def start_server(proxy_port, proxy_mode):
    port = int(proxy_port) if proxy_port else 8080
    mode = proxy_mode if proxy_mode else 'regular'

    if proxy_mode == 'http':
        mode = 'regular'

    config = proxy.ProxyConfig(
        port=port,
        mode=mode,
        cadir="./ssl/",
    )

    state = flow.State()
    server = ProxyServer(config)
    m = WYProxy(server, state)
    m.run()

class wyDaemon(Daemon):

    def __init__(self, pidfile, proxy_port=8080, proxy_mode='regular'):
        super(wyDaemon, self).__init__(pidfile)
        self.proxy_port = proxy_port
        self.proxy_mode = proxy_mode

    def run(self):
        logging.info("wyproxy is starting...")
        logging.info("Listening: 0.0.0.0:{} {}".format(
            self.proxy_port, self.proxy_mode))
        start_server(self.proxy_port, self.proxy_mode)

def run(args):

    if args.restart:
        args.port = read_cnf().get('port')
        args.mode = read_cnf().get('mode')

    wyproxy = wyDaemon(
        pidfile = '/tmp/wyproxy.pid',
        proxy_port = args.port,
        proxy_mode = args.mode)

    if args.daemon:
        save_cnf(args)
        wyproxy.start()
    elif args.stop:
        wyproxy.stop()
    elif args.restart:
        wyproxy.restart()
    else:
        wyproxy.run()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="wyproxy v 1.0 ( Proxying And Recording HTTP/HTTPs and Socks5)")
    parser.add_argument("-d","--daemon",action="store_true",
        help="start wyproxy with daemond")
    parser.add_argument("-stop","--stop",action="store_true",required=False,
        help="stop wyproxy daemond")
    parser.add_argument("-restart","--restart",action="store_true",required=False,
        help="restart wyproxy daemond")
    parser.add_argument("-p","--port",metavar="",default="8080",
        help="wyproxy bind port")
    parser.add_argument("-m","--mode",metavar="",choices=['http','socks5','transparent'],default="http",
        help="wyproxy mode (HTTP/HTTPS, Socks5)")
    args = parser.parse_args()

    try:
        run(args)
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping Client")
        sys.exit(1)

