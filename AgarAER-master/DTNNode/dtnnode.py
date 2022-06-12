import threading

import dill

from discovery import Discovery
from requestService import RequestService
from forwardService import ForwardService
from deliveryService import DeliveryService
from helloMessage import HelloMessage
from multicastSniffer import multicastSniffer
from peer import Peer
import time
from repeatTimer import setInterval
from storeService import StoreService
from message import MessageTypes
from concurrent.futures import ThreadPoolExecutor
import logging
from multicastWatcher import MulticastWatcher

class DTNNode:
    def __init__(self, isOverlayNode, interface, overlayInterface):
        self.peer = Peer(interface)
        self.discoveryService = Discovery(interface,self.newPeerDiscovery)
        self.mc = multicastSniffer(interface)
        self.isOverlayNode = isOverlayNode
        self.overlayInterface = overlayInterface
        if self.isOverlayNode:
            self.mcwatcher = MulticastWatcher(self.overlayInterface)
            self.mcoverlaysniffer = multicastSniffer(self.overlayInterface)
        self.storeService = StoreService()
        self.forwardService = ForwardService(self.peer, self.storeService)
        self.requestService = RequestService(self.peer, self.storeService)
        self.deliveryService = DeliveryService(self.storeService)
        self.threadPool = ThreadPoolExecutor(10)

    def start(self):
        self.updateMulticastWatchAddr()
        if not self.isOverlayNode:
            hellomessage = self.buildHelloMessage()
            self.discoveryService.announcePeer(hellomessage)
            self.mc.sniffPackets(self.onPacketReceived,False)
        else:
            self.mcoverlaysniffer.sniffPackets(self.onPacketReceivedFromOverlay,True)
        self.startNode()


    def onPacketReceivedFromOverlay(self,data):
        self.threadPool.submit(self.storeService.receivePacket, data, True)

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

    @setInterval(1)
    def updateMulticastWatchAddr(self):  # TESTAR IsTO
        peersset = self.peer.get_neighborsaddr_to_sniff()
        address_set = self.mc.watchAddresses()
        if len(peersset) == 0:
            self.mc.sniffAddress(self.peer.get_ip())
            return
        toRemoveSet = address_set.difference(peersset)
        tmpAddressSet = address_set.difference(toRemoveSet)
        self.mc.sniffAddress(self.peer.ip)
        #logging.debug(f'toADDSET: {to AddSet}')
        for addr in toRemoveSet:
            self.mc.removeAddressFromSniff(addr)
        for addr in peersset:
            self.mc.sniffAddress(addr)

    def startNode(self):

        self.peer.listenPeerMessages(
            self.onPeerMessageReceived)  ## CUIDADO COM O FIO DE EXECUÇÃO , talvez usar uma queue para passar os dados
        if not self.isOverlayNode:
            self.requestServiceThread()
        while True:
            online_neigh = self.peer.get_online_neighbors()
            #logging.debug(f'online neigh count : {len(online_neigh)}')
            if len(online_neigh) == 0: continue
            for n in online_neigh:
                self.threadPool.submit(self.sendDeadCertificate, n)
            if not self.isOverlayNode:
                self.threadPool.submit(self.forwardService.forward())


    @setInterval(0.2)
    def requestServiceThread(self):
        for n in self.peer.get_online_neighbors():
            self.requestService.requestOverlayPacket(n.ip)

    def sendDeadCertificate(self, neigh):
        tmplst = self.storeService.getDeadCertificateNotSeen(neigh.ip)
        for dc in tmplst:
            dc.passedBy(neigh.ip)
            self.peer.sendMessageToNeighbour(dc, neigh.ip)

    def onPeerMessageReceived(self, message, addr):
        handler_peerMessage = {MessageTypes.FORWARD_MESSAGE: self.handleForwardMessage,
                               MessageTypes.DTN_MESSAGE: self.handleDTNPacket,
                               MessageTypes.DEAD_CERTIFICATE: self.handleDeadCertificateMessage,
                               MessageTypes.REQUEST_MESSAGE: self.handleRequestMessage,
                               MessageTypes.HELLO_MESSAGE: self.handleHelloMessage}
        unpck_msg = dill.loads(message)
        handler = handler_peerMessage.get(unpck_msg.get_type(), None)
        if handler:
            self.threadPool.submit(handler, unpck_msg, addr[0])

    def handleHelloMessage(self,message,addr):
        self.peer.newPeer(message,addr)

    def newPeerDiscovery(self,message,addr):
        hellomessage = dill.loads(message)
        if self.isOverlayNode:
            hellomessage = self.buildHelloMessage()
            self.peer.sendMessageToNeighbour(hellomessage, addr[0])
        self.peer.newPeer(hellomessage,addr[0])

    def handleForwardMessage(self, message, addr):
        if message.toSniff():
            self.peer.neighbors[addr].set_sniff(True)
            for neig in message.addrlst:
                self.peer.neighbors[neig].set_sniff(True)
        return

    def handleRequestMessage(self, message, addr):

        packetsList = self.requestService.acceptRequest(message, addr)

        self.mcwatcher.joinGroup(message.group_addr)
        self.mcoverlaysniffer.sniffAddress(message.group_addr)

        for p in packetsList:
            self.forwardService.forwardPacket(p, addr)

    def handleDTNPacket(self, message, addr):
        packet_report = self.storeService.dtnPacketReceived(message)

        if self.isOverlayNode:
            if packet_report.fromOverlay:  # REVER ISTO
                return
            self.deliveryService.deliverToOverlay(packet_report)

            self.storeService.generateDeadCertifiticate(packet_report.packet_digest)
        else:
            if message.fromOverlay:
                self.deliveryService.deliverOnNode(packet_report)

    def handleDeadCertificateMessage(self, message, addr):
        logging.debug(f'received dead certificate')
        self.storeService.deadPacketReceived(message)

    ## PACOTE RECEBIDO PELO SNIFFER
    def onPacketReceived(self, packet):  # TALVEZ EXECUTAR ISTO NA POOL DE THREADS
        self.threadPool.submit(self.storeService.receivePacket, packet, False)


if __name__ == '__main__':
    DTNNode(False).start()
