import ipaddress
import socket
import struct

import dill as pickle
from ..messaging import AuthenticationRequest , MessageType , AuthenticationResponse
from ..channel import Watcher


def icslistenparameter(data, addr):
    unpck = pickle.loads(data)
    return unpck.get_type() == MessageType.AUTHENTICATION_RESPONSE

def gameChannelBool(data, addr):
    unpck = pickle.loads(data)
    return unpck.get_type() == MessageType.GAME_STATE

class NetworkClient:
    def __init__(self) -> None:
        self.UDP_IP = "::"
        self.authGamePort = 5005
        self.group_addr = 'ff02::5'
        self.sock = socket.socket(socket.AF_INET6, # Internet
						socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.settimeout(0.2)


    def initConnectionToServer(self,name,gameConfigListener):
        print('initConnectionToServer')
        msg = AuthenticationRequest(None, name)
        pckmsg = pickle.dumps(msg)
        self.sock.sendto(pckmsg, (self.group_addr,self.authGamePort))
        watch_authchannel = Watcher(self.UDP_IP, msg.get_port(),self.group_addr)
        data,addr = watch_authchannel.listenWhile(icslistenparameter)
        watch_authchannel.close()
        authresponse = pickle.loads(data)
        gameConfigListener(authresponse.get_config())

    def listenToGameChannel(self, port, listener):
        watch_gamechannel = Watcher(self.UDP_IP, port ,self.group_addr)
        while True:
            data,addr = watch_gamechannel.listenWhile(gameChannelBool)
            listener(pickle.loads(data))



""" Receber e transmitir os dados para o servidor """


""" Aqui a meio vai aparecer um observers pattern """
  #

