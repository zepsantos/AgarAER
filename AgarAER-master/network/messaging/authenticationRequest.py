from .message import Message
import random
from .messageType import MessageType
class AuthenticationRequest(Message) :
    def __init__(self,id,name) :
        Message.__init__(self, MessageType.AUTHENTICATION_REQUEST)
        self.id = id
        self.name = name
        self.port = random.randint(5000,5999)

    def get_id(self) :
        return self.id

    def get_name(self) :
        return self.name

    def get_port(self):
        return self.port