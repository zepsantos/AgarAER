import socket
from sqlite3 import Timestamp

class DeliveryService:
    """NOT SURE Apenas uma ideia"""
    def __init__(self, storeService):
        self.storeService = storeService
        self.socketPort = {}
        
    def deliverOnNode(self,packet_report):
        packet = self.storeService.requestPacket(packet_report.packet_digest)
        if packet is None:
            return
        sock = get_socket(packet_report.port)

        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 0)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 0)

        
        sock.sendto(packet,packet_report.packet_dst)


    def get_socket(self,port):
        sock = self.socketPort.get(port,None)
        if sock is None:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            sock.bind(('::', port))
            self.socketPort[port] = sock
        return sock
        
    def deliverToOverlay(self,packet_report):
        packet = self.storeService.requestPacket(packet_report.packet_digest)
        if packet is None:
            return
        
        sock = socket.socket(socket.AF_INET6,  # Internet
                                  socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 20)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, 1)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL, 20)
        sock.bind(('::',packet_report.port))
        
        sock.sendto(packet,packet_report.packet_dst)
        
        
        def close():
            pass