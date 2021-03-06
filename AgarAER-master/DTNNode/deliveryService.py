import logging
import socket
from sqlite3 import Timestamp


class DeliveryService:
    """NOT SURE Apenas uma ideia"""

    def __init__(self, storeService):
        self.storeService = storeService
        self.deliveryHelper = {}
        # self.socketPort = {}
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def deliverOnNode(self, packet_report):
        packet = self.storeService.requestPacket(packet_report.get_digest())
        if self.recentPacketSent(packet_report):
            return

        if packet is None:
            return
        # sock = self.get_socket(packet_report.port)

        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 0)

        self.sock.sendto(packet, (packet_report.packet_dst, packet_report.port))
        self.packetSent(packet_report)

    """def get_socket(self,port):
        sock = self.socketPort.get(port,None)
        if sock is None:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            sock.bind(('::', port))
            self.socketPort[port] = sock
        return sock """

    def recentPacketSent(self,packet_report):
        timestamp = self.deliveryHelper.get(packet_report.port, None)
        if timestamp is None:
            return False
        elif timestamp-packet_report.timestamp < 0:
            return False
        return True

    def packetSent(self,packet_report):
        self.deliveryHelper[packet_report.port] = packet_report.timestamp

    def deliverToOverlay(self, packet_report):
       # logging.debug(f'delivering packet {packet_report.packet_dst}  {packet_report.port} {packet_report.get_digest()}')
       # logging.debug(f'packet : {self.storeService}  {self.storeService.requestPackets}')
        packet = self.storeService.requestPacket(packet_report.get_digest())

        if packet is None:
            return
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 64)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 0)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 64)

        self.sock.sendto(packet, (packet_report.packet_dst, packet_report.port))

        def close():
            pass
