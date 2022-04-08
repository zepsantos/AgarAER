import socket
import struct
import ipaddress
class Watcher:
    def __init__(self, ip, port, group_addr):
        self.ip = ip
        self.port = port
        self.group_addr = group_addr
        self.mtcsock = socket.socket(socket.AF_INET6, # Internet
						socket.SOCK_DGRAM) # UDP
        self.mtcsock.setblocking(False)
        self.mtcsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mtcsock.bind((self.ip, self.port))
        self.config_socketMTC()

    def config_socketMTC(self):
        interface_index = socket.if_nametoindex("eth0")

        #self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)
        #self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 1)
        mc_addr = ipaddress.IPv6Address(self.group_addr)
        join_data = struct.pack('16sI', mc_addr.packed, interface_index)
        self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, join_data)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_TCLASS, 0)
        # self.mtcsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVTCLASS, 1)

    def retrieveMessage(self):
        data, addr = self.mtcsock.recvfrom(1400)
        return data,addr


    # TODO: Dar timeout a este request
    def listenWhile(self, fnbool):
        self.mtcsock.setblocking(True)
        while True:
            data, addr = self.mtcsock.recvfrom(1400)
            if fnbool(data,addr):
                return data,addr




    def close(self):
        self.mtcsock.close()


    def get_watch(self):
        return self.mtcsock.fileno()

