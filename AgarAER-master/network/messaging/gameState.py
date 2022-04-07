from .message import Message
from .messageType import MessageType
class GameState(Message) :
    def __init__(self, gameState) :
        Message.__init__(self, MessageType.GAME_STATE)
        self.gameState = gameState


    def get_game_state(self) :
        return self.gameState


