

from urllib import request
from requestMessage import RequestMessage
import logging

class RequestService:

    def __init__(self, peer, storeService):
        self.peer = peer
        self.storeService = storeService
        self.addrHasSeen = {}
    
    def requestOverlayPacket(self,addr):
        shelves = list(self.storeService.getShelves())
        for shelve in shelves:
            requestm = RequestMessage(shelve.group_addr)
            portxpacket = shelve.listPortQueueSortedByTimestamp()
            result = self.buildRequestStats(portxpacket)
            requestm.set_mrg(result)
            self.peer.sendMessageToNeighbour(requestm,addr)
            
    def buildRequestStats(self,portxpacket):
        tmp = []
        for p,packetlist in portxpacket:
            timestamp = None
            if len(packetlist) == 0:
                continue
            elif len(packetlist) == 1:
                timestamp = packetlist[0].timestamp
            else:
                timestamp = packetlist[-1].timestamp
            tmp.append((p,timestamp))
        return tmp

    def acceptRequest(self,requestMessage,addr):
        packets_tosend = []
        helper_dict = dict(requestMessage.mrg)
        shelve = self.storeService.getShelve(requestMessage.group_addr)
        lpqtime = shelve.listPortQueueSortedByTimestampFiltered(lambda packet_report: packet_report.fromOverlay)
        for p,listqueue in lpqtime:
            if p in helper_dict:
                packets_tosend.extend(self.listAfterTimeReceived(listqueue,helper_dict[p]))
            else:
                packets_tosend.extend(listqueue)
                
        tmp = self.addrHasSeen.get(addr,[])
        tmp.extend(packets_tosend)
        self.addrHasSeen[addr] = tmp
        return packets_tosend
                      
    def listAfterTimeReceived(self,packet_list, timestamp):
        lastReceived = len(packet_list)
        i = 0
        for p in packet_list:
            if p.timestamp > timestamp:
                lastReceived = i
                break
            i += 1
        res = packet_list[lastReceived:] #testar
        return res