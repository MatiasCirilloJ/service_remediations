#!/usr/bin/python
# -*- encoding: iso-8859-1 -*-

"""
Python syslog client.
This code is placed in the public domain by the author.
Written by Christian Stigen Larsen.
This is especially neat for Windows users, who (I think) don't
get any syslog module in the default python installation.
See RFC3164 for more info -- http://tools.ietf.org/html/rfc3164
Note that if you intend to send messages to remote servers, their
syslogd must be started with -r to allow to receive UDP from
the network.
---------------------------------------------------------------------
"""

import socket

LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

def syslog(message, level=LEVEL['notice'],
    host='10.54.158.25', port=5000):
    """
    Send syslog TCP packet to given host and port.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port));
    data = '<%d> %s' % (level, message)
    sock.send(data.encode())
    sock.close()

#syslog(message=data, level=0, host='10.54.158.25', port=udp5000)