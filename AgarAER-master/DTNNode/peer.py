import socket
import threading
import netifaces as ni
import dill
import logging
from message import MessageTypes
from neighbor import Neighbor


class Peer:
    UDP_IP = '::'
    UDP_PORT = 10000

    def __init__(self, interface):
        self.neighbors = dict()
        self.sock = socket.socket(socket.AF_INET6,  # Internet
                                  socket.SOCK_DGRAM)
        self.ip = ni.ifaddresses(interface)[ni.AF_INET6][0]['addr']

        self.sock.bind((self.ip, Peer.UDP_PORT))

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
        addrwport = ((addr), Peer.UDP_PORT)
        self.sock.sendto(pickledmessage, addrwport)

    def newPeer(self, hellomessage, addr):

        if hellomessage.get_type() != MessageTypes.HELLO_MESSAGE:
            return
        neighb = self.neighbors.get(addr, None)
        if neighb is not None:
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
                delay, timestamp = overlayStats
                neighb.get_stats().set_average_delay_overlay(delay, timestamp)

    def getNeighborsIPView(self):
        return self.neighbors.keys()

    def get_overlay_neighbors(self):
        lst = []
        tmp = list(self.neighbors.values())
        for neigh in tmp:
            if neigh.isOverlay():
                lst.append(neigh)
        return lst

    def get_online_neighbors(self):
        lst = []
        tmp = list(self.neighbors.values())
        for neigh in tmp:
            if neigh.connected:
                lst.append(neigh)
        #logging.debug(f'list online: {lst}')
        return lst

    def get_neighborsaddr_to_sniff(self):
        tmp = set()
        lst = list(self.neighbors.values())
        for n in lst:
            if n.sniff:
                tmp.add(n.ip)
        return tmp

    def get_ip(self):
        return self.ip
