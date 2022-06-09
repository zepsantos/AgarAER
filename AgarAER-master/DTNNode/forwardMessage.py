from message import Message
from message import MessageTypes


class Forward_Message(Message):
    """Mensagem para o sniffer do multicast saber se apanha ou não os pacotes deste ip"""
    def __init__(self):
        Message.__init__(self, MessageTypes.FORWARD_MESSAGE)
        self.sniff = True

    def set_sniff(self,toSniff):
        self.sniff = toSniff

