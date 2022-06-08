from message import MessageTypes
from message import Message


class HelloMessage(Message):

    def __init__(self):
        Message.__init__(self, MessageTypes.HELLO_MESSAGE)
        self.isOverlay = False
        # INFO DA MENSAGEM A ENVIAR



    def set_isOverlay(self,isOverlay):
        self.isOverlay = isOverlay
