from peer import Peer
from multicastSniffer import multicastSniffer
from discovery import Discovery
from repeatTimer import RepeatTimer
from storeService import StoreService
class DTNNode:
    def __init__(self):
        self.peer = Peer()
        self.discoveryService = Discovery(self.peer.newPeer)
        self.mc = multicastSniffer('eth0')
        self.multicastTable = {}
        self.neighbors_peers_view = self.peer.getNeighborsIPView()
        self.storeService = StoreService()
    def start(self):
        self.mc.sniffPackets(self.onPacketReceived)
        self.startNode()

    def updateMulticastWatchAddr(self):
        peersset = set(self.neighbors_peers_view)
        address_set = self.mc.watchAddresses()

        toRemoveSet = address_set-peersset
        tmpAddressSet = address_set - toRemoveSet
        toAddSet = tmpAddressSet + peersset
        for addr in toRemoveSet:
            self.mc.removeAddressFromSniff(addr)
        for addr in toAddSet:
            self.mc.sniffAddress(addr)

    def startNode(self):
        timer = RepeatTimer(1, self.updateMulticastWatchAddr)
        timer.daemon = True
        timer.start()


    def onPacketReceived(self,type,src_ip,port,payload):
        pass



if __name__ == '__main__':
    DTNNode().start()