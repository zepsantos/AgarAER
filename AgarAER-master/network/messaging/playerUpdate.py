from .message import Message
from .messageType import MessageType
class PlayerUpdate(Message) :
    def __init__(self, p_update) :
        Message.__init__(self, MessageType.PLAYER_UPDATE)
        self.p_update = p_update


    def get_player_update(self) :
        return self.p_update


