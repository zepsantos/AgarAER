import threading
import uuid
import socket

import dill

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
        if addr in self.neighbors:
            neighb = self.neighbors[addr]
            neighb.alive()
        self.neighbors[addr] = Neighbor(addr)

    def getNeighborsIPView(self):
        return self.neighbors.keys()
