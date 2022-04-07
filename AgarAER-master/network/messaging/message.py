class Message:
    def __init__(self, type):
        self.type = type
        self.senderID = None
        self.senderAddr = None

    def get_type(self):
        return self.type


    def get_sender(self):
        return self.senderID

    def set_sender(self, sender):
        self.senderID = sender
