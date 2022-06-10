import queue

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

    def forwardPacket(self,packet_report,addr):
        packet_digest = packet_report.get_digest()
        packet = self.storeService.requestPackets(packet_digest)
        dtnpacket = DTNPacket(packet_report.packet_src, packet_report.packet_dst,
                              packet_report.port, packet, packet_digest,packet_report.timestamp)
        self.peer.sendMessageToNeighbour(dtnpacket,addr)

    def call_predictor(self):
        self.nextHopNeighbor = self.predictor.predict()

    def forward(self):
        if self.nextHopNeighbor is None:
            return
        if self.nextHopNeighbor.isAlive():
            self.send_ForwardMessage(self.peer.get_ip(),True)
            shelves = self.storeService.getShelves()
            for shelve in shelves:
                tmpl = shelve.listPortQueueSortedByTimestamp()
                for p, queuelist in tmpl:
                    for packet_report in queuelist:
                        if packet_report.timestamp > self.nextHopNeighbor.stats.get_passedByTime():
                            continue
                        if packet_report.packet_src == self.nextHopNeighbor.ip:
                            continue
                        self.forwardPacket(packet_report,self.nextHopNeighbor.ip)

                # Obter os pacotes todos em cache
                # Enviar para o no predicted
                # So obter os que ainda não foram capturados




    def send_ForwardMessage(self,addr,sniff):
        forwardMessage = Forward_Message(addr,sniff)
        self.peer.sendMessageToNeighbour(forwardMessage,self.nextHopNeighbor.ip)

    def  get_nextHopNeighbor(self):
        return self.nextHopNeighbor