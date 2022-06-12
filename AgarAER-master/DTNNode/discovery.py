import ipaddress
import socket
import struct
import threading
import time
from random import uniform

import dill
import netifaces as ni
import logging


class Discovery:

    def __init__(self,interface, newPeerListener):
        self.interface = interface
        self.UDP_IP = str(ni.ifaddresses(interface)[socket.AF_INET6][0]['addr'])
        logging.debug(f'discovery ip : {self.UDP_IP}')
        self.discoveryPort = 19230
        self.group_addr = 'ff0e::3'
        self.sock = socket.socket(socket.AF_INET6,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 5)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 5)
        self.sock.bind(("::", self.discoveryPort))
        self.config_socketMTC()
        threading.Thread(target=self.discoverPeers).start()
        self.newPeerListener = newPeerListener

    def config_socketMTC(self):
        # Getting interfaces
        interface_index = socket.if_nametoindex(self.interface)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 10)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 10)
        mc_addr = ipaddress.IPv6Address(self.group_addr)
        join_data = struct.pack('16sI', mc_addr.packed, interface_index)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, join_data)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_TCLASS, 0)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVTCLASS, 1)

    def announcePeer(self,msg):
        msgpickled = dill.dumps(msg)
        threading.Thread(target=self.startThreadToAnnouncePeer,args=(msgpickled,)).start()

    def startThreadToAnnouncePeer(self,msgpickled):
        timeToSleep = uniform(0.47, 0.53)
        while True:
            self.sock.sendto(msgpickled, (self.group_addr, self.discoveryPort))
            time.sleep(timeToSleep)

    def discoverPeers(self):
        while True:
            data, addr = self.sock.recvfrom(1400)
            self.newPeerListener(data,addr)




