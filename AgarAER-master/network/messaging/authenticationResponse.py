from .message import Message
from .messageType import MessageType
class AuthenticationResponse(Message) :
    def __init__(self,id, config) :
        Message.__init__(self, MessageType.AUTHENTICATION_RESPONSE)
        self.id = id
        self.config = config
        self.finalmessage = False
        self.packet_no = 0 # packet number
        self.last_packet_no = 0 # last packet number

    def set_id(self, id) :
        self.id = id

    def set_config(self, config) :
        self.config = config

    def set_packet_no(self, packet_no):
        self.packet_no = packet_no


    def set_last_packet_no(self, last_packet_no):
        self.last_packet_no = last_packet_no

    def get_last_packet_no(self):
        return self.last_packet_no

    def get_config(self) :
        return self.config

    def get_id(self) :
        return self.id

    def is_finished(self):
        return self.finalmessage

    def set_finalmessage(self, finalmessage):
        self.finalmessage = finalmessage

    def get_packet_no(self):
        return self.packet_no