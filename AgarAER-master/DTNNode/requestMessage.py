from message import Message
from message import MessageTypes


class RequestMessage(Message):
    """Mensagem para pedir dados do multicast Do overlay"""
    def __init__(self,):
        Message.__init__(self, MessageTypes.REQUEST_MESSAGE)
        self.mrg = {}

    def set_mrg(self, dictWithMCStats)
        self.mrg = dictWithMCStats
    