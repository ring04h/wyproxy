#!/usr/bin/env python
# encoding: utf-8

"""
sudo networksetup -setautoproxystate Wi-Fi on
sudo networksetup -setautoproxyurl Wi-Fi http://s5.wuyun.org/s5.pac

disable_proxy()
{
    networksetup -setsocksfirewallproxystate Wi-Fi off
    networksetup -setsocksfirewallproxystate Ethernet off
    echo "SOCKS proxy disabled."
}
trap disable_proxy INT
 
networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9999
networksetup -setsocksfirewallproxy Ethernet 127.0.0.1 9999
networksetup -setsocksfirewallproxystate Wi-Fi on
networksetup -setsocksfirewallproxystate Ethernet on
echo "SOCKS proxy enabled."
echo "Tunneling..."


networksetup -setwebproxystate Wi-Fi on
networksetup -setsecurewebproxystate Wi-Fi on

networksetup -setwebproxy Wi-Fi 127.0.0.1 8888
networksetup -setwebproxy Ethernet 127.0.0.1 8888
networksetup -setsecurewebproxy Wi-Fi 127.0.0.1 8888

"""

import re
import argparse
import subprocess

black_device = [
    'Bluetooth PAN',
    'Thunderbolt 1',
    'Thunderbolt Bridge',
    'Thunderbolt Ethernet']

class Warpper(object):
    """docstring for Warpper"""
    def __init__(self, service, ipaddr, port):
        super(Warpper, self).__init__()
        self.service = service
        self.ipaddr = ipaddr
        self.port = port
        self.devices = self.get_all_service()

    def run_setup_command(self, *arguments):
        # print ['networksetup'] + list(arguments)
        return subprocess.check_output(['networksetup'] + list(arguments))

    def enable_proxy_for_device(self):
        print('Enabling proxy on {} {} {}...'.format(self.service, self.ipaddr, self.port))

        if self.service == 'http':
            for device in self.devices:
                for subcommand in ['-setwebproxy', '-setsecurewebproxy']:
                    self.run_setup_command(
                        subcommand, device, self.ipaddr, str(self.port))

        elif self.service == 'socks5':
            for device in self.devices:
                self.run_setup_command(
                    '-setsocksfirewallproxy', device, self.ipaddr, str(self.port))

    def disable_proxy_for_device(self):
        for device in self.devices:
            print('Disabling proxy on {}...'.format(device))
            for subcommand in ['-setwebproxystate', '-setsecurewebproxystate', '-setsocksfirewallproxystate']:
                self.run_setup_command(subcommand, device, 'Off')

    def get_all_service(self):
        all_service = []
        for device in self.get_service_name_map().values():
            if device not in black_device:
                all_service.append(device)
        return all_service

    def get_service_name_map(self):
        order = self.run_setup_command('-listnetworkserviceorder')
        mapping = re.findall(
            r'\(\d+\)\s(.*)$\n\(.*Device: (.+)\)$',
            order,
            re.MULTILINE)
        return dict([(b, a) for (a, b) in mapping])

def main():

    parser = argparse.ArgumentParser(
        description="Enable/Disable OS X network device proxy and wrap wyproxy")

    parser.add_argument(
        "-d","--disable",
        action="store_true",
        help="Disable wyproxy OS X device")

    parser.add_argument(
        "-ip","--ipaddr",
        metavar="",default="127.0.0.1",
        help="override the default ipaddr of 127.0.0.1")

    parser.add_argument(
        "-p","--port",
        metavar="",default="8080",
        help="override the default port of 8080")

    parser.add_argument(
        "-m","--mode",
        metavar="",choices=['http','socks5'], default="http",
        help="wyproxy mode (http, socks5)")

    args = parser.parse_args()

    osx_warpper = Warpper(
        service = args.mode,
        ipaddr = args.ipaddr, 
        port = args.port)

    if args.disable:
        osx_warpper.disable_proxy_for_device()
        print('Disable all proxy successfully...')
    else:
        osx_warpper.enable_proxy_for_device()
        print('Enable proxy successfully...')

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print('error: {}'.format(e))



