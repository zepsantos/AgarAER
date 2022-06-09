from message import MessageTypes
from message import Message


class DTNPacket(Message):

    def __init__(self, src_addr, dst_addr,port, packet, packet_digest):
        Message.__init__(self, MessageTypes.DTN_MESSAGE)
        self.src_addr = src_addr
        self.port = port
        self.dest_addr = dst_addr
        self.digest = packet_digest
        self.packet = packet
