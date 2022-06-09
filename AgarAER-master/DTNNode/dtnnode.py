from peer import Peer
from multicastSniffer import multicastSniffer
from discovery import Discovery
from repeatTimer import RepeatTimer
from storeService import StoreService
from helloMessage import HelloMessage
from forwardService import ForwardService

class DTNNode:
    def __init__(self,isOverlayNode):
        self.peer = Peer()
        self.ip = "2001:9::2"
        self.discoveryService = Discovery(self.peer.newPeer)
        self.mc = multicastSniffer('eth0')
        self.isOverlayNode = isOverlayNode
        self.multicastTable = {}
        self.neighbors_peers_view = self.peer.getNeighborsIPView()
        self.storeService = StoreService()
        self.forwardService = ForwardService(self.peer,self.storeService)

    def start(self):
        hellomessage = self.buildHelloMessage()
        self.discoveryService.announcePeer(hellomessage)
        self.mc.sniffPackets(self.onPacketReceived)
        self.startNode()


    def buildHelloMessage(self):
        hellomessage = HelloMessage()
        hellomessage.set_isOverlay(self.isOverlayNode)
        overlayneighlist = self.peer.get_overlay_neighbors()
        min = 10000
        stat = None
        for ovneigh in overlayneighlist:
            (delay,timestamp) = ovneigh.get_overlay_stats()
            if delay < min:
                min = delay
                stat = (delay,timestamp)
        hellomessage.set_overlayStats(stat)
        return hellomessage

    def updateMulticastWatchAddr(self):
        peersset = set(self.neighbors_peers_view)
        address_set = self.mc.watchAddresses()
        if len(peersset) == 0:
            self.mc.sniffAddress(self.ip)
            return
        toRemoveSet = address_set.difference(peersset)
        tmpAddressSet = address_set.difference(toRemoveSet)
        toAddSet = tmpAddressSet.add(peersset)
        if len(toAddSet) == 0 : # Falta aqui a condição do forwardService
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


    ## PACOTE RECEBIDO PELO SNIFFER
    def onPacketReceived(self,packet):
        self.storeService.receivePacket(packet)



if __name__ == '__main__':
    DTNNode(True).start()