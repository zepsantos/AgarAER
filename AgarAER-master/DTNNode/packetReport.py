import datetime

class PacketReport():

    def __init__(self ,packet_digest ,port ,src_packet ,dest_packet):
        self.packet_digest = packet_digest
        self.port = port
        self.packet_src = src_packet
        self.packet_dst = dest_packet
        self.timestamp = self.generate_timestamp()


    def get_port(self):
        return self.port

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts