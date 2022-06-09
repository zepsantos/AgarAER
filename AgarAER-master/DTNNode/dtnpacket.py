from message import Message
from message import MessageTypes


class DTNPacket(Message):

    def __init__(self, src_addr, dst_addr,port, packet, packet_digest,packet_timestamp):
        Message.__init__(self, MessageTypes.DTN_MESSAGE)
        self.src_addr = src_addr
        self.port = port
        self.dest_addr = dst_addr
        self.digest = packet_digest
        self.packet = packet
        self.packet_timestamp = packet_timestamp
