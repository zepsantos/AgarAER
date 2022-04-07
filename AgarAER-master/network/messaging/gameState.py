from .message import Message
from .messageType import MessageType
class GameState(Message) :
    def __init__(self, gameState) :
        Message.__init__(self, MessageType.GAME_STATE)
        self.gameState = gameState
        self.newplayers = []

    
    
    def get_newplayers_status(self):
        return len(self.newplayers) > 0
    
    def get_game_state(self) :
        return self.gameState

    def get_newplayers(self):
        return self.newplayers
        
    def set_newplayers(self,newplayers):
        self.newplayers = newplayers