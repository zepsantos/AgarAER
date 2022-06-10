

from urllib import request
from requestMessage import RequestMessage


class RequestService:

    def __init__(self, peer, storeService):
        self.peer = peer
        self.storeService = storeService
    
    
    def requestOverlayPacket(self,addr):
        requestm = RequestMessage()
        shelves = self.storeService.getShelves()
        requestStatHelper = {}
        for shelve in shelves:
            portxpacket = shelve.listPortQueueSortedByTimestamp()
            result = map(lambda port,packet : (port,packet[-1].timestamp),portxpacket) # TODO:CONFIRMAR ISTO
            requestStatHelper[shelve.group_addr] = result
        requestm.set_mrg(requestStatHelper)
        self.peer.sendMessageToNeighbour(requestm,addr)