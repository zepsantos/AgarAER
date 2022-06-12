import ipaddress
import socket
import struct

import dill as pickle
from ..messaging import AuthenticationRequest , MessageType , AuthenticationResponse
from ..channel import Watcher


def icslistenparameter(data, addr):
    if data:
        unpck = pickle.loads(data)
        return unpck.get_type() == MessageType.AUTHENTICATION_RESPONSE
    return False

def gameChannelBool(data, addr):
    unpck = pickle.loads(data)
    return unpck.get_type() == MessageType.GAME_STATE

class NetworkClient:
    def __init__(self) -> None:
        self.UDP_IP = "::"
        self.authGamePort = 5005
        self.gameReportPort = None
        self.group_addr = 'ff0e::2'
        self.sock = socket.socket(socket.AF_INET6, # Internet
						socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS ,64)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IP_MULTICAST_TTL ,64)
        #self.sock.settimeout(0.2)


    def initConnectionToServer(self,name,gameConfigListener):
        msg = AuthenticationRequest(None, name)
        pckmsg = pickle.dumps(msg)
        self.sock.sendto(pckmsg, (self.group_addr,self.authGamePort))
        self.gameReportPort = msg.get_port()
        watch_authchannel = Watcher(self.UDP_IP, self.gameReportPort,self.group_addr)
        try:
            data,addr = watch_authchannel.listenWhileTimeout(icslistenparameter,100)
        except socket.timeout:
            gameConfigListener({})
        # while data is None:
            #data,addr = watch_authchannel.listenWhileTimeout(icslistenparameter,10000)
        authresponse = pickle.loads(data)
        config = authresponse.get_config()
        for i in range(0,authresponse.get_last_packet_no()):
            data, addr = watch_authchannel.listenWhile(icslistenparameter)
            authresponse = pickle.loads(data)
            config = self.joinConfig(config,authresponse.get_config())
        watch_authchannel.close()
        gameConfigListener(config)





    def joinConfig(self,config,sndconfig):

        sndgpacket = sndconfig['game']
        config['player'].update(sndconfig['player'])
        config['game']['players'].extend(sndgpacket['players'])
        config['game']['cells'].extend(sndgpacket['cells'])
        return config



    def listenToGameChannel(self, port, listener):
        watch_gamechannel = Watcher(self.UDP_IP, port ,self.group_addr)
        while True:
            data,addr = watch_gamechannel.listenWhile(gameChannelBool)
            msg = pickle.loads(data)
            listener(msg)


    def sendToServer(self, p_update):
        pckmsg = pickle.dumps(p_update)
        self.sock.sendto(pckmsg, (self.group_addr,self.gameReportPort))



""" Receber e transmitir os dados para o servidor """


""" Aqui a meio vai aparecer um observers pattern """
  #

