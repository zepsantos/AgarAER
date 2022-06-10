from collections import deque


class Shelve:
    """
        Esta classe tem como função ser uma cache indivual para um determinado grupo multicast em uma determinada porta
        esta guarda o payload do pacote ,num dicionario em que o hash vai ser o message digest do payload
        De x em x tempo limpa a cache
    """

    def __init__(self, group_addr):
        self.group_addr = group_addr
        self.portToPacketDic = {}

    def addPacket(self, packet_report):
        packetQ = self.getPortQueue(packet_report.get_port()) 
        
        packetQ.append(packet_report)

    def getPortQueue(self, port):  # TODO: Testar aqui a deque
        packetQ = self.portToPacketDic.get(port)
        if not packetQ:
            packetQ = deque()
            self.portToPacketDic[port] = packetQ
        return deque(packetQ)

    def getPortQueueAsList(self, port):  # TODO: Testar aqui a deque
        packetQ = self.portToPacketDic.get(port)
        if not packetQ:
            packetQ = deque()
            self.portToPacketDic[port] = packetQ
        return list(packetQ)

    def listPortQueueSortedByTimestamp(self):
        tmp = []
        for p,pqueue in self.portToPacketDic:
            sortedList = sorted(pqueue, key=lambda x: x.timestamp)
            tmp.append((p,sortedList))
            #
        return tmp
    
    def getOverlayPackets(self):
        res = []
        for q in  self.portToPacketDic.values():
            for packet_report in q:
                if packet_report.fromOverlay:
                    
                    res.append(packet_report)
        
            

    def removePacketReports(self,port,packet_report_list):
        tmpqueue = self.getPortQueue(port)
        for packet_report in packet_report_list:
            tmpqueue.remove(packet_report)
    
    def clean(self):
        pass
