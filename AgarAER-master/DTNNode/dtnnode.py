import dill

from discovery import Discovery
from forwardService import ForwardService
from helloMessage import HelloMessage
from multicastSniffer import multicastSniffer
from peer import Peer
from repeatTimer import RepeatTimer
from storeService import StoreService
from message import MessageTypes
from concurrent.futures import ThreadPoolExecutor


class DTNNode:
    def __init__(self, isOverlayNode):
        self.peer = Peer()
        self.discoveryService = Discovery(self.peer.newPeer)
        self.mc = multicastSniffer('eth0')
        self.isOverlayNode = isOverlayNode
        self.multicastTable = {}
        self.storeService = StoreService()
        self.forwardService = ForwardService(self.peer, self.storeService)
        self.threadPool = ThreadPoolExecutor(5)

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
            (delay, timestamp) = ovneigh.get_overlay_stats()
            if delay < min:
                min = delay
                stat = (delay, timestamp)
        hellomessage.set_overlayStats(stat)
        return hellomessage

    def updateMulticastWatchAddr(self):  # TESTAR IsTO
        peersset = self.peer.get_neighborsaddr_to_sniff()
        address_set = self.mc.watchAddresses()
        if len(peersset) == 0:
            self.mc.sniffAddress(self.peer.get_ip())
            return
        toRemoveSet = address_set.difference(peersset)
        tmpAddressSet = address_set.difference(toRemoveSet)
        toAddSet = tmpAddressSet.add(peersset)
        toAddSet.add(self.peer.get_ip())

        for addr in toRemoveSet:
            self.mc.removeAddressFromSniff(addr)
        for addr in toAddSet:
            self.mc.sniffAddress(addr)

    def startNode(self):
        timer = RepeatTimer(1, self.updateMulticastWatchAddr)
        timer.daemon = True
        timer.start()
        self.peer.listenPeerMessages(
            self.onPeerMessageReceived)  ## CUIDADO COM O FIO DE EXECUÇÃO , talvez usar uma queue para passar os dados
        while True:

            online_neigh = self.peer.get_online_neighbors()
            if len(online_neigh) == 0: continue
            self.forwardService.forward()



    def onPeerMessageReceived(self, message, addr):
        handler_peerMessage = {MessageTypes.FORWARD_MESSAGE: self.handleForwardMessage,
                               MessageTypes.DTN_MESSAGE: self.handleDTNPacket,
                               MessageTypes.DEAD_CERTIFICATE: self.handleDeadCertificateMessage}
        unpck_msg = dill.loads(message)
        handler = handler_peerMessage.get(unpck_msg.get_type(), None)
        if handler:
            self.threadPool.submit(handler, unpck_msg, addr)

    def handleForwardMessage(self, message, addr):
        if message.toSniff():
            self.peer.neighbors[addr].set_sniff(True)
        return

    def handleDTNPacket(self, message, addr):
        self.storeService.dtnPacketReceived(message)

    def handleDeadCertificateMessage(self, message, addr):
        self.storeService.deadPacketReceived(message)

    ## PACOTE RECEBIDO PELO SNIFFER
    def onPacketReceived(self, packet):  # TALVEZ EXECUTAR ISTO NA POOL DE THREADS
        self.storeService.receivePacket(packet)


if __name__ == '__main__':
    DTNNode(True).start()
