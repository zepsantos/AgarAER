import datetime
from enum import Enum



class MessageTypes(Enum):
    HELLO_MESSAGE = 1
    ACK_MESSAGE = 2,
    FORWARD_MESSAGE = 3,
    DEAD_CERTIFICATE = 4
    


class Message:
    def __init__(self, type):
        self.type = type
        self.senderID = None
        self.senderIP = None
        self.messageDigest = None # Correr o digest para a mensagem
        self.timestamp = self.generate_timestamp()

    def get_type(self):
        return self.type


    def get_sender(self):
        return self.senderID

    def set_sender(self, sender):
        self.senderID = sender


    def get_ping(self):
        current_time = self.generate_timestamp()
        return current_time - self.timestamp

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts