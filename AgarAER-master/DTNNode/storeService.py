import xxhash
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip6, icmp6
from pypacker.layer4 import udp
import logging
from packetReport import PacketReport
from shelve import Shelve
from deadCertificate import DeadCertificate


class StoreService:
    """
        Esta classe tem como função controlar o nosso repositorio de shelves
    """

    def __init__(self):
        self.shelveRepository = {} # GRUPO_ADDR X PORT X QUEUE
        self.requestingData = set()
        self.deadCertificatesHistory = {}
        self.packetsCache = {}
        self.dtnMessagesCache = {}

    def receivePacket(self, packet):        
        self.parsePacket(packet)

    def handleICMP(self, ip1, icmp1):
        print('icmp1 type:',icmp1.type)
        if icmp1.type == icmp6.MLD_LISTENER_QUERY:
            return
        elif icmp1.type == icmp6.MLD_LISTENER_REPORT:
            self.requestingData.add(ip1.src_s)
            print('icmp1 body_bytes: ' ,str(icmp1.body_bytes))
            return
        elif icmp1.type == icmp6.MLD_LISTENER_DONE:
            self.requestingData.remove(ip1.src_s)
            return


    def getShelve(self,group_addr):
        shelve = self.shelveRepository.get(group_addr,None)
        if shelve is None:
            shelve = Shelve(group_addr)
            self.shelveRepository[group_addr] = shelve
        return shelve

    #https://kbandla.github.io/dpkt/creating_parsers.html
    def handleMCPacket(self, ip1, udp2):
        if udp2.dport == 19230 or udp2.dport == 10000: ## PORTA DO SERVIÇO DE DISCOVERY
            return
        digest = xxhash.xxh64()
        digest.update(udp2.body_bytes)
        packet_digest = digest.hexdigest()
        self.packetsCache[packet_digest] = udp2.body_bytes
        packet_report = PacketReport(packet_digest,udp2.dport,ip1.src_s,ip1.dst_s,False)
        
        shelve = self.getShelve(ip1.dst_s)
        
        shelve.addPacket(packet_report)
        logging.debug(f'packet_report : {shelve.listPortQueueSortedByTimestamp()}')

        



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

    def requestPackets(self,packet_digest):
        return self.packetsCache.get(packet_digest,None)


    def deadPacketReceived(self,deadCertificate):
        packet_digest = deadCertificate.message_hash
        if packet_digest in deadCertificate:
            return
        self.deadCertificatesHistory[packet_digest] = deadCertificate
        self.packetsCache.pop(packet_digest)


    def dtnPacketReceived(self,dtnPacket):
        if dtnPacket.digest in self.packetsCache:
            logging.debug(f'packet already in cache')
            return
        packet_report = self.convertDTNPacketToPacketReport(dtnPacket)
        self.packetsCache[dtnPacket.digest] = dtnPacket.packet
        shelve = self.getShelve(dtnPacket.dest_addr)
        shelve.addPacket(packet_report)
        return packet_report

    def convertDTNPacketToPacketReport(self, dtnpacket):
        return PacketReport(dtnpacket.digest,dtnpacket.port,dtnpacket.src_addr,dtnpacket.dest_addr,dtnpacket.fromOverlay)


    def getShelves(self):
        return self.shelveRepository.values()
    
    
    def clear(self):
        pass

    def generateDeadCertifiticate(self,packet_digest):
        tmp = DeadCertificate(packet_digest)
        self.deadCertificatesHistory[packet_digest] = tmp

    
    
    def getDeadCertificateNotSeen(self,addr):
        tmplst = []
        for dc in self.deadCertificatesHistory.values():
            if not dc.hasPassed(addr):
                tmplst.append(dc)
        return tmplst
            