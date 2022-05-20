from message import MessageTypes
from message import Message


class HelloMessage(Message):

    def __init__(self):
        Message.__init__(self, MessageTypes.HELLO_MESSAGE)
        # INFO DA MENSAGEM A ENVIAR
