from .message import Message
from .messageType import MessageType
class AuthenticationResponse(Message) :
    def __init__(self,id, config) :
        Message.__init__(self, MessageType.AUTHENTICATION_RESPONSE)
        self.id = id
        self.config = config

    def set_id(self, id) :
        self.id = id

    def set_config(self, config) :
        self.config = config


    def get_config(self) :
        return self.config

    def get_id(self) :
        return self.id


