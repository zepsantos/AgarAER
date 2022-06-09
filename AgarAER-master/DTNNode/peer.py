import threading
import uuid
import socket

import dill
from message import MessageTypes
from neighbor import Neighbor
from discovery import Discovery


class Peer:
    UDP_IP = '::'
    UDP_PORT = 10000

    def __init__(self):
        self.neighbors = dict()
        self.sock = socket.socket(socket.AF_INET6,  # Internet
                                  socket.SOCK_DGRAM)
        self.sock.bind((Peer.UDP_IP, Peer.UDP_PORT))

    def listenPeerMessages(self, onPeerMessageReceived):
        listenthread = threading.Thread(target=self.receivePeerMessages, args=(onPeerMessageReceived,))
        listenthread.daemon = True
        listenthread.start()

    def receivePeerMessages(self, onPeerMessageReceived):
        while True:
            data, addr = self.sock.recvfrom(1500)  # buffer size is 1024 bytes
            onPeerMessageReceived(data, addr)

    def sendMessageToNeighbour(self, message, addr):
        pickledmessage = dill.dumps(message)
        self.sock.sendto(pickledmessage, addr)

    def newPeer(self, recObject):
        data, addr = recObject
        hellomessage = dill.loads(data)
        if hellomessage.get_type() != MessageTypes.HELLO_MESSAGE:
            return
        neighb = self.neighbors.get(addr, None)
        if neighb:
            neighb = self.neighbors[addr]
            neighb.alive()
        else:
            neighb = Neighbor(addr)
            self.neighbors[addr] = neighb
        if hellomessage.isOverlay():
            neighb.set_isOverlay(True)
        else:
            overlayStats = hellomessage.get_overlayStats()
            if overlayStats:
                delay,timestamp = overlayStats
                neighb.get_stats().set_average_delay_overlay(delay,timestamp)

    def getNeighborsIPView(self):
        return self.neighbors.keys()

    def get_overlay_neighbors(self):
        lst = []
        for neigh in self.neighbors:
            if neigh.isOverlay():
                lst.append(neigh)
        return lst
