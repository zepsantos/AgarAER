import datetime


class Message:
    def __init__(self, type):
        self.type = type
        self.senderID = None
        self.senderAddr = None
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

    def generate_timestamp(self,):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts
