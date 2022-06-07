from pypacker.layer3 import ip6, icmp6
from pypacker.layer12 import ethernet
from pypacker.layer4 import udp


class StoreService:
    """
        Esta classe tem como função controlar o nosso repositorio de shelves
    """

    def __init__(self):
        self.shelveRepository = {} # (AX(BXC)) (IPS(PORTA??) ( GROUPADDR (Shelve))
        self.requestingData = set()

    def receivePacket(self, packet):
        self.parsePacket(packet)

    def handleICMP(self, ip1, icmp1):
        print('icmp1 type:',icmp1.type)
        if icmp1.type == icmp6.MLD_LISTENER_QUERY:
            return
        elif icmp1.type == icmp6.MLD_LISTENER_REPORT:
            self.requestingData.add(ip1)
            return
        elif icmp1.type == icmp6.MLD_LISTENER_DONE:
            self.requestingData.remove(ip1)
            return


    #https://kbandla.github.io/dpkt/creating_parsers.html
    def handleMCPacket(self, ip1, udp2):
        print(udp2.dport)

    def parsePacket(self, packet):
        eth = ethernet.Ethernet(packet)
        ip1 = eth[ip6.IP6]
        icmp1 = ip1[icmp6.ICMP6]
        udp2 = ip1[udp.UDP]
        if icmp1:
            self.handleICMP(ip1, icmp1)
            return

        if udp2:
            self.handleMCPacket(ip1, udp2)
            return

    def requestPacket(self,addr):
        pass
