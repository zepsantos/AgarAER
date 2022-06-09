from message import MessageTypes
from message import Message


class HelloMessage(Message):

    def __init__(self):
        Message.__init__(self, MessageTypes.HELLO_MESSAGE)
        self.isOverlay = False
        self.delayToOverlay = None #(AVERAGE DELAY, TIMESTAMP)
        # INFO DA MENSAGEM A ENVIAR



    def set_isOverlay(self,isOverlay):
        self.isOverlay = isOverlay

    def isOverlay(self):
        return self.isOverlay

    def set_overlayStats(self,delayToOverlay):
        self.delayToOverlay = delayToOverlay

    def get_overlayStats(self):
        return self.delayToOverlay