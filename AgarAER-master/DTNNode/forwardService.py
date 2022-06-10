import queue

from forwarderPredictor import ForwarderPredictor
from dtnpacket import DTNPacket

class ForwardService:
    """Class que trata de dar forward dos pacotes da cache """
    def __init__(self, peer, storeService):
        self.peer = peer
        self.predictor = ForwarderPredictor(self.peer.neighbors)
        self.queueToForward = queue.PriorityQueue()
        self.nextHopNeighbor = None
        self.storeService = storeService

    def forward(self,packet_report,addr):
        packet_digest = packet_report.get_digest()
        packet = self.storeService.requestPackets(packet_digest)
        dtnpacket = DTNPacket(packet_report.packet_src, packet_report.packet_dst,
                              packet_report.port, packet, packet_digest,packet_report.timestamp)
        self.peer.sendMessageToNeighbour(dtnpacket,addr)

    def call_predictor(self):
        self.nextHopNeighbor = self.predictor.predict()


    def  get_nextHopNeighbor(self):
        return self.nextHopNeighbor