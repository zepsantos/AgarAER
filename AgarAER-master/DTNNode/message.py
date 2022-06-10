import datetime
from enum import Enum



class MessageTypes(Enum):
    HELLO_MESSAGE = 1
    ACK_MESSAGE = 2,
    FORWARD_MESSAGE = 3, 
    DEAD_CERTIFICATE = 4,
    DTN_MESSAGE = 5,
    REQUEST_MESSAGE = 6
    


class Message:
    def __init__(self, type):
        self.type = type
        self.timestamp = self.generate_timestamp()

    def get_type(self):
        return self.type




    def get_ping(self):
        current_time = self.generate_timestamp()
        return current_time - self.timestamp

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts