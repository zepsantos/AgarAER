from enum import Enum
class MessageType(Enum):
    PLAYER_UPDATE = 4
    AUTHENTICATION_REQUEST = 1,
    AUTHENTICATION_RESPONSE = 2,
    GAME_STATE = 3
