from peer import Peer
from multicastSniffer import multicastSniffer
from discovery import Discovery
class DTNNode:
    def __init__(self):
        self.peer = Peer()
        self.discoveryService = Discovery(self.peer.newPeer)
        self.mc = multicastSniffer('eth0')
        self.multicastTable = {}


    def start(self):
        self.mc.sniffPackets(self.onPacketReceived)

    def onPacketReceived(self,type,src_ip,port,payload):
        pass



if __name__ == '__main__':
    DTNNode().start()