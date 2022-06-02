from pypacker.layer3 import ip6, icmp6
from pypacker.layer12 import ethernet
from pypacker.layer4 import udp

class StoreService:
    """
        Esta classe tem como função controlar o nosso repositorio de shelves
    """
    def __init__(self):
        self.shelveRepository = {}
        self.requestingData = set()


    def receivePacket(self,packet):
        self.parsePacket(packet)

    def handleICMP(self,icmp1):
        pass

    def handleMCPacket(self,udp2):
        pass

    def parsePacket(self, packet):
        eth = ethernet.Ethernet(packet)
        ip1 = eth[ip6.IP6]
        icmp1 = ip1[icmp6.ICMP6]
        udp2 = ip1[udp.UDP]
        if icmp1:
            self.handleICMP(icmp1)
            return

        if udp2:
            self.handleMCPacket(udp2)
            return