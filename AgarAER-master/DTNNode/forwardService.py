import queue

from forwarderPredictor import ForwarderPredictor
class ForwardService:

    def __init__(self, peer, storeService):
        self.predictor = ForwarderPredictor()
        self.peer = peer
        self.queueToForward = queue.PriorityQueue()
        self.nextHopNeighbor = None
        self.storeService = storeService

    def forward(self,packet,addr): #TODO: FALTA CONSTRUIR O DTNPACKET COM O PACKET
        self.peer.sendMessageToNeighbour(packet,addr)

    def call_predictor(self):
        self.nextHopNeighbor = self.predictor.predict()


    def  get_nextHopNeighbor(self):
        return self.nextHopNeighbor