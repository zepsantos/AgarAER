from .message import Message
from .messageType import MessageType
class GameState(Message) :
    def __init__(self, gameState) :
        Message.__init__(self, MessageType.GAME_STATE)
        self.gameState = gameState


    def getGameState(self) :
        return self.gameState


