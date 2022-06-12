import ipaddress
import socket
import struct
import logging
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip6


class MulticastWatcher:
    ETH_FRAME_LEN = 1514  # Max. octets in frame sans FCS
    ETH_P_ALL = 3

    def __init__(self, interface):
        self.interface = interface
        self.groupSocket = {}

    def joinGroup(self, group_addr):
        if self.groupJoined(group_addr):
            return
        rawsocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        rawsocket.bind(('::', 0))
        interface_index = socket.if_nametoindex(
            self.interface)  # loop over interfaces to get the desired interface instead of hardcoded

        mc_addr = ipaddress.IPv6Address(group_addr)
        join_data = struct.pack('16sI', mc_addr.packed, interface_index)
        rawsocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, join_data)
        self.groupSocket[group_addr] = rawsocket


    def checkPacketAddr(self, packet):
        eth = ethernet.Ethernet(packet)
        ip1 = eth[ip6.IP6]
        if ip1.dst_s in self.groupSocket.keys():  # Pode não ser o ip1.src_s
            logging.debug(f'packet sniffing {ip1.dst_s}')
            return True
        else:
            return False

    def groupJoined(self, group_addr):
        return group_addr in self.groupSocket.keys()


    def groupQuit(self,group_addr):
        pass

    def groupsJoined(self):
        return list(self.groupSocket.keys())
