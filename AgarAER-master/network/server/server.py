import time
from time import sleep
import sys
from .game import Game
import threading
from concurrent.futures import ThreadPoolExecutor
import socket
import dill as pickle
import select
import pygame
import logging
from ..channel import Watcher
from ..messaging import MessageType, AuthenticationResponse , GameState

class Server: 
    def __init__(self) -> None:
        self.broadCastThread = None
        self.UDP_IP = "::" # = 0.0.0.0 u IPv4
        self.group_addr = 'ff0e::2'
        self.UDP_PORT = 5005
        self.game = Game()
        self.poll = select.poll()
        self.watcherDic = {}
        self.threadpool = ThreadPoolExecutor(max_workers=5)
        self.gameStarted = False
        #self.poll.register(self.main_socket.fileno(), select.POLLIN)
        #self.game_worker = Worker(self.UDP_IP,6000,self.group_addr)
        self.newconn_watcher = Watcher(self.UDP_IP,self.UDP_PORT,self.group_addr)

    def start_listening(self):
        self.poll.register(self.newconn_watcher.get_watch(), select.POLLIN)
        #threading.Thread(target=self.checkPlayerStatus).start()
        try:
            while True:
                sleep(0.01)
                events = self.poll.poll(1)
                # For each new event, dispatch to its handler
                for key, event in events:
                    if key == self.newconn_watcher.get_watch():
                        self.handle_new_connection(key,event)
                    else:
                        self.threadpool.submit(self.handler, key, event)
        finally:
            pass
            #self.warnImGoingOffline()
            #self.poll.unregister(self.main_socket.fileno())
            #self.main_socket.close()

    def checkPlayerStatus(self):
        while True:
            for p in self.game.get_player_list():
                #print('player ', p.getLastTimeSeenDifMilis())
                if p.getLastTimeSeenDifMilis() > 1000:
                    if not p.get_acceptconf_status():
                        self.sendConfig(p,p.get_watcher_port())




    def handler(self, key, event):
        watcher = self.watcherDic[key]
        data ,addr = watcher.retrieveMessage()
        msg = pickle.loads(data)
        #logging.debug("Received player update from %s" % format(msg.get_player_update()))
        if msg.type == MessageType.PLAYER_UPDATE:
            self.received_client_update(msg, addr)
        else:
            return


    def received_client_update(self, msg, addr):
        self.game.update_from_player(msg.get_sender(), msg.get_player_update())


    def handle_new_connection(self, key, event):
        data ,addr = self.newconn_watcher.retrieveMessage()
        authrequest = pickle.loads(data)
        if authrequest.type != MessageType.AUTHENTICATION_REQUEST:
            return
        logging.log(logging.INFO, "New connection from %s" % str(addr))

        p = self.game.add_player(addr, authrequest.get_id(), authrequest.get_name(),authrequest.get_port())
        self.threadpool.submit(self.sendConfig,p,authrequest.get_port())
        self.listenForClientUpdates(authrequest.get_port())
        if not self.gameStarted:
            self.initGame()
        else:
            self.game.add_to_newplayers(p, 20)


    def sendConfig(self,p,port):
       # while not p.get_acceptconf_status():
        sleep(1)
        #print('im here')
        tmpsock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        tmpsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS ,64)
        tmpsock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL ,64)
        msgToSend = AuthenticationResponse(p.get_id(), self.createConfigForNewPlayers(p))
        finalmsg = pickle.dumps(msgToSend)
        if len(finalmsg) > 1200:
            res = self.createConfigInPacketSize(p,msgToSend.get_config())
            for i in range(len(res)):
                tmpauthpck = res[i]
                tmpauthpck.set_last_packet_no(len(res)-1)
                tmpauthpck.set_packet_no(i)
                tmpauthpckpick = pickle.dumps(tmpauthpck)
                tmpsock.sendto(tmpauthpckpick, (self.group_addr, port))
                sleep(0.01)
        else:
            tmpsock.sendto(finalmsg, (self.group_addr, port))



    def createConfigInPacketSize(self,p, config):
        tmp = []
        fstconfig = {'player':config.get('player',{}),'game':{'players':config['game']['players'],'cells':[],'port':config['game']['port']}}
        cellslist = config['game']['cells']
        cellsize = sys.getsizeof(cellslist[0])
        fstauth = AuthenticationResponse(p.get_id(), fstconfig)
        tmp.append(fstauth)
        while len(cellslist) > 0:
            ncells = round(1000/cellsize)
            cellstoadd = cellslist[:ncells]
            cellslist = cellslist[ncells:]
            tmconfig = {'player': {}, 'game': {'players': {}, 'cells': cellstoadd, 'port': config['game']['port']}}
            tmpauth = AuthenticationResponse(p.get_id(), tmconfig)
            tmp.append(tmpauth)
        return tmp



    def initGame(self):
        self.gameStarted = True
        self.broadCastThread = threading.Thread(target=self.broadcastGameToGameChannel)
        self.broadCastThread.start()

    def listenForClientUpdates(self,port):
        watcher = Watcher(self.UDP_IP,port,self.group_addr)
        self.poll.register(watcher.get_watch(), select.POLLIN)
        self.watcherDic[watcher.get_watch()] = watcher

    def broadcastGameToGameChannel(self):
        clock = pygame.time.Clock()
        tmpsock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        tmpsock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS ,64)
        tmpsock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL ,64)
        while True:
            clock.tick(60)
            msgToSendunpc = GameState(self.game.brief_convert_game_to_dic())
            msgToSendunpc.set_newplayers(self.game.get_newplayers())
            msgToSend = pickle.dumps(msgToSendunpc)
            tmpsock.sendto(msgToSend, (self.group_addr, self.game.get_port()))






    def createConfigForNewPlayers(self, p):
        config = {'player': p.convert_to_dic(), 'game': self.game.convertGameToDic()}
        return config

""""
Servidor liga-se fica a escuta"""


""""

Cliente liga pela primeira vez, servidor envia o seu id e a sua cor e a sua posição"""

"""
Cliente a cada frame envia mensagem com id e estado de jogo"""

"""Servidor pega na mensagem de cada cliente e retransmite aos outros"""



