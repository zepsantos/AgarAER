from message import Message
from message import MessageTypes


class RequestMessage(Message):
    """Mensagem para pedir dados do multicast Do overlay"""
    def __init__(self,group_addr):
        Message.__init__(self, MessageTypes.REQUEST_MESSAGE)
        self.group_addr = group_addr
        self.mrg = []

    def set_mrg(self, listwithmcstats):
        self.mrg = listwithmcstats
    