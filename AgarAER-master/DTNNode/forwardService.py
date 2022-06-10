import queue
from struct import pack

from forwarderPredictor import ForwarderPredictor
from dtnpacket import DTNPacket
from forwardMessage import Forward_Message

class ForwardService:
    """Class que trata de dar forward dos pacotes da cache """
    def __init__(self, peer, storeService):
        self.peer = peer
        self.predictor = ForwarderPredictor(self.peer.neighbors)
        self.nextHopNeighbor = None
        self.storeService = storeService
        self.controlMessages = []
        self.neighHasSeen = {}

    def forwardPacket(self, packet_report, addr):
        packet_digest = packet_report.get_digest()
        packet = self.storeService.requestPackets(packet_digest)
        if packet is None:
            return False
        dtnpacket = DTNPacket(packet_report.packet_src, packet_report.packet_dst,
                              packet_report.port, packet, packet_digest,packet_report.timestamp,False)
        self.peer.sendMessageToNeighbour(dtnpacket,addr)
        return True

    def call_predictor(self):
        self.nextHopNeighbor = self.predictor.predict()
        
        
    def neigh_seen_packet(self,packet_digest,addr):
        tmpset = self.neigh_has_seen.get(addr)
        if tmpset is None :
            tmpset = set()
            self.neigh_has_seen[addr] = tmpset
        tmpset.update(packet_digest)
        
    def has_neigh_seen_packet(self,packet_digest,addr):
        tmpset = self.neigh_has_seen.get(addr)
        if tmpset:
            return packet_digest in tmpset
        return False

    def forward(self):## CHAMAR O PREDICTOR ANTES DE DAR FORWARD GARANTE QUE SO PREVEMOS O NEXT HOP QUANDO TAMOS COM ALGUM VIZINHO
        
        self.call_predictor()
        tmp_report_list = []
        if self.nextHopNeighbor is None:
            return
        if self.nextHopNeighbor.isAlive():
            if  not self.nextHopNeighbor.isOverlay():
                lstToSniff = list(self.peer.get_neighborsaddr_to_sniff())
                self.send_ForwardMessage(lstToSniff,True)
            shelves = self.storeService.getShelves()
            for shelve in shelves:
                tmpl = shelve.listPortQueueSortedByTimestamp()
                for p, queuelist in tmpl: 
                    tmp_nopacket_list = []
                    for packet_report in queuelist: 
                        if packet_report.timestamp > self.nextHopNeighbor.stats.get_passedByTime() and not self.nextHopNeighbor.isOverlay():
                            continue
                        if packet_report.packet_src == self.nextHopNeighbor.ip:
                            continue
                        if self.has_neigh_seen_packet():
                            continue
                        status = self.forwardPacket(packet_report,self.nextHopNeighbor.ip)
                        if not status:
                            tmp_nopacket_list.append(packet_report)
                        else:
                            tmp_report_list.append(packet_report)
                        tmpl.removePacketReports(port,tmp_nopacket_list)
      
        self.neigh_seen_packet(tmp_report_list,self.nextHopNeighbor.ip)

                # Obter os pacotes todos em cache
                # Enviar para o no predicted
                # So obter os que ainda não foram capturados




    def send_ForwardMessage(self,addr,sniff):
        forwardMessage = Forward_Message(addr,sniff)
        self.peer.sendMessageToNeighbour(forwardMessage,self.nextHopNeighbor.ip)

    def  get_nextHopNeighbor(self):
        return self.nextHopNeighbor
    
    
    def clear(self):
        pass