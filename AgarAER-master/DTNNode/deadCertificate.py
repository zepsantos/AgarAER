from message import Message
from message import MessageTypes


class DeadCertificate(Message):

    def __init__(self,message_hash):
        Message.__init__(self, MessageTypes.DEAD_CERTIFICATE)
        self.message_hash = message_hash
        self.passedBy = []
        # INFO DA MENSAGEM A ENVIAR

    def passedBy(self,addr):
        self.passedBy.append(addr)

    def hasPassed(self,addr):
        return addr in self.passedBy