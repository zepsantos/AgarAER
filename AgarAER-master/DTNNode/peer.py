import uuid
import socket
from neighbor import Neighbor
from discovery import Discovery


class Peer:

    def __init__(self):
        self.neighbors = dict()
        self.sock = socket.socket(socket.AF_INET6,  # Internet
                                  socket.SOCK_DGRAM)

    def listenPeerMessages(self):
        pass

    def sendPeerMessage(self, message):
        pass

    def startDiscovery(self):
        Discovery(self.newPeer)

    def newPeer(self, recObject):
        data, addr = recObject
        if addr in self.neighbors:
            neighb = self.neighbors[addr]
            neighb.alive()
        self.neighbors[addr] = Neighbor(addr)

    def getNeighborsIPList(self):
        return self.neighbors.keys()
