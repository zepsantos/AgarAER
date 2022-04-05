from time import sleep

from .game import Game
import threading
import socket
import dill as pickle
import select
import logging
from ..channel import Watcher
from ..messaging import MessageType, AuthenticationResponse , GameState
class Server: 
    def __init__(self) -> None:
        self.broadCastThread = None
        self.UDP_IP = "::" # = 0.0.0.0 u IPv4
        self.group_addr = 'ff02::5'
        self.UDP_PORT = 5005
        self.game = Game()
        self.poll = select.poll()
        self.watcherDic = {}
        self.gameStarted = False
        #self.poll.register(self.main_socket.fileno(), select.POLLIN)
        #self.game_worker = Worker(self.UDP_IP,6000,self.group_addr)
        self.newconn_watcher = Watcher(self.UDP_IP,self.UDP_PORT,self.group_addr)

    def start_listening(self):

        self.poll.register(self.newconn_watcher.get_watch(), select.POLLIN)
        try:
            while True:
                sleep(0.01)
                events = self.poll.poll(1)
                # For each new event, dispatch to its handler
                for key, event in events:
                    logging.log(logging.DEBUG, "Event: %s" % str(key))
                    if key == self.newconn_watcher.get_watch():
                        self.handle_new_connection(key,event)
                    else:
                        self.handler(key, event)
        finally:
            pass
            #self.warnImGoingOffline()
            #self.poll.unregister(self.main_socket.fileno())
            #self.main_socket.close()

    def handler(self, key, event):
        pass

    def handle_new_connection(self, key, event):
        data ,addr = self.newconn_watcher.retrieveMessage()
        authrequest = pickle.loads(data)
        if authrequest.type != MessageType.AUTHENTICATION_REQUEST:
            return
        logging.log(logging.INFO, "New connection from %s" % str(addr))
        tmpsock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        p = self.game.add_player(addr, authrequest.get_id(), authrequest.get_name())
        msgToSend = AuthenticationResponse(p.get_id(), self.createConfigForNewPlayers(p))
        finalmsg = pickle.dumps(msgToSend)
        tmpsock.sendto(finalmsg, (self.group_addr, authrequest.get_port()))
        if not self.gameStarted:
            self.initGame()

    def initGame(self):
        self.gameStarted = True
        self.game.start()
        self.broadCastThread = threading.Thread(target=self.broadcastGameToGameChannel)
        self.broadCastThread.start()

    #THREAD AQUI
    def broadcastGameToGameChannel(self):

        tmpsock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        while True:
            msgToSendunpc = GameState(self.game.brief_convert_game_to_dic())
            msgToSend = pickle.dumps(msgToSendunpc)
            tmpsock.sendto(msgToSend, (self.group_addr, self.game.get_port()))





    def createConfigForNewPlayers(self, p):
        config = {'player': p.convert_to_dic(), 'game': self.game.convertGameToDic() , 'group': (self.group_addr, self.game.get_port())}
        return config

""""
Servidor liga-se fica a escuta"""


""""

Cliente liga pela primeira vez, servidor envia o seu id e a sua cor e a sua posição"""

"""
Cliente a cada frame envia mensagem com id e estado de jogo"""

"""Servidor pega na mensagem de cada cliente e retransmite aos outros"""



