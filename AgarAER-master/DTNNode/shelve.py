import queue
from repeatTimer import RepeatTimer

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
        packetQ.put(packet_report)




    def getPortQueue(self,port):
        packetQ = self.portToPacketDic.get(port)
        if not packetQ:
            packetQ = queue.Queue()
            self.portToPacketDic[port] = packetQ
        return packetQ

    def clean(self):
        pass