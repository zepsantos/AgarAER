from message import MessageTypes
from message import Message


class DeadCertificate(Message):

    def __init__(self,message_hash):
        Message.__init__(self, MessageTypes.DEAD_CERTIFICATE)
        self.message_hash = message_hash
        # INFO DA MENSAGEM A ENVIAR
