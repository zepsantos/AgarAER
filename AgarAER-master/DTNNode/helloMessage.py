from message import Message
from message import MessageTypes


class HelloMessage(Message):

    def __init__(self):
        Message.__init__(self, MessageTypes.HELLO_MESSAGE)
        self.isOverlayNode = False
        self.delayToOverlay = None #(AVERAGE DELAY, TIMESTAMP)
        # INFO DA MENSAGEM A ENVIAR



    def set_isOverlay(self,isOverlayBool):
        self.isOverlayNode = isOverlayBool

    def isOverlay(self):
        return self.isOverlayNode

    def set_overlayStats(self,delayToOverlay):
        self.delayToOverlay = delayToOverlay

    def get_overlayStats(self):
        return self.delayToOverlay