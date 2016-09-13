#!/usr/bin/env python
# encoding: utf-8

"""
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
networksetup -setsecurewebproxy Wi-Fi 127.0.0.1 8888

"""

