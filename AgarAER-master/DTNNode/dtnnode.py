from peer import Peer
from multicastSniffer import multicastSniffer
from discovery import Discovery
from repeatTimer import RepeatTimer
from storeService import StoreService
class DTNNode:
    def __init__(self):
        self.peer = Peer()
        self.ip = "2001:9::2"
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
        if len(peersset) == 0:
            self.mc.sniffAddress(self.ip)
            return
        toRemoveSet = address_set.difference(peersset)
        tmpAddressSet = address_set.difference(toRemoveSet)
        print(tmpAddressSet)
        print(peersset)
        toAddSet = tmpAddressSet.add(peersset)
        toAddSet.add(self.ip)
        for addr in toRemoveSet:
            self.mc.removeAddressFromSniff(addr)
        for addr in toAddSet:
            self.mc.sniffAddress(addr)

    def startNode(self):
        timer = RepeatTimer(1, self.updateMulticastWatchAddr)
        timer.daemon = True
        timer.start()
        self.peer.listenPeerMessages(self.onPeerMessageReceived) ## CUIDADO COM O FIO DE EXECUÇÃO , talvez usar uma queue para passar os dados

    def onPeerMessageReceived(self,message,addr):
        pass

    def onPacketReceived(self,packet):
        self.storeService.receivePacket(packet)



if __name__ == '__main__':
    DTNNode().start()