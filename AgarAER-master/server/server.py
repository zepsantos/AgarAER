import socket
import pickle
from game import Game

class Server: 
    def __init__(self) -> None:
        self.UDP_IP = "::" # = 0.0.0.0 u IPv4
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET6, # Internet
						socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        self.sock.setsockopt()
        self.game = Game()

    def startServer(self):
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes  # vai começar uma thread quando recebe dados 
            dados = pickle.loads(data)
            print ("received message:", dados)

    def broadcastToClients(self):
        pass







""""
Servidor liga-se fica a escuta"""


""""
Cliente liga pela primeira vez, servidor envia o seu id e a sua cor e a sua posição"""

"""
Cliente a cada frame envia mensagem com id e estado de jogo"""

"""Servidor pega na mensagem de cada cliente e retransmite aos outros"""



def run():
    pass




if __name__ == '__main__':
    run()