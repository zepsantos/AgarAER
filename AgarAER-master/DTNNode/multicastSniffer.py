import socket
import threading

from pypacker.layer3 import ip6, icmp6
from pypacker.layer12 import ethernet
from pypacker.layer4 import udp


class multicastSniffer:
    ETH_FRAME_LEN = 1514  # Max. octets in frame sans FCS
    ETH_P_ALL = 3

    def __init__(self, interface):
        interface = interface
        self.rawsocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(multicastSniffer.ETH_P_ALL))
        self.rawsocket.bind((interface, 0))
        self.sniffAddr = set()

    def sniffAddress(self, address):
        self.sniffAddr.add(address)

    def removeAddressFromSniff(self, address):
        self.sniffAddr.remove(address)

    def watchAddresses(self):
        return set(self.sniffAddr)

    def sniffPackets(self, onPacketReceived):
        sniffThread = threading.Thread(target=self.sniffPacketsLoop)
        sniffThread.daemon = True
        sniffThread.start()

    def sniffPacketsLoop(self,onPacketReceived):
        while True:
            data = self.rawsocket.recv(multicastSniffer.ETH_FRAME_LEN)
            onPacketReceived(data)
    def parsePacket(self, data):
        eth = ethernet.Ethernet(data)
        ip1 = eth[ip6.IP6]
        if ip1.src_s not in self.sniffAddr:  # Pode não ser o ip1.src_s
            return

        icmp1 = ip1[icmp6.ICMP6]
        udp2 = ip1[udp.UDP]
        if icmp1:
            print('ICMP', ip1.src_s)
            return

        if udp2:
            print('UDP', ip1.src_s, eth.body_bytes)
            return
