import logging
import math
import random
from .utils import generateTimestamp,getTimeStampDifMilis

class ServerPlayer:
    COLOR_LIST = [
        (37,7,255),
        (35,183,253),
        (48,254,241),
        (19,79,251),
        (255,7,230),
        (255,7,23),
        (6,254,13)]

    def __init__(self,addr,id,name,port) -> None:
        self.addr = addr
        self.watcherport = port
        self.id = id 
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.firstTimeSeen = generateTimestamp()
        self.lastTimeSeen = self.firstTimeSeen
        self.acceptedConfig = False
        self.color = random.choice(ServerPlayer.COLOR_LIST) #escolhe uma cor random
        self.speed = 3 
        self.name = name
        self.watcher = None
        self.killed = []

    def convert_to_dic(self):
        p = {'id':self.id,'x' : self.x, 'y' : self.y, 'mass' : self.mass, 'color' : self.color, 'speed' : self.speed, 'name' : self.name, 'killed' : self.killed}
        return p

    def brief_convert_to_dic(self):
        p = {'id':self.id,'x' : self.x, 'y' : self.y, 'mass' : self.mass}
        return p

    def get_id(self):
        return self.id 


    def set_watcher(self,watcher):
        self.watcher = watcher

    def get_watcher(self):
        return self.watcher

    def update(self,p_update):
        self.lastTimeSeen = generateTimestamp()
        self.calculateMove(p_update['rotation'])
        logging.debug('Player {} moved to {}'.format(self.name,(self.x,self.y)))
        self.mass = p_update.get('mass',self.mass)

    def getLastTimeSeenDifMilis(self):
        return getTimeStampDifMilis(self.lastTimeSeen)


    def calculateMove(self,rotation):
        normalized = (90 - math.fabs(rotation)) / 90
        vx = self.speed * normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)

        radius = int(self.mass / 2 + 3)
        # print('raio ',radius)

        coordCima = (self.y) - radius
        coordBaixo = (self.y) + radius
        coordDir = (self.x) + radius
        coordEsq = (self.x) - radius

        if (coordEsq > 0):
            self.x += vx
        else:
            if (vx > 0):
                self.x += vx
            else:
                self.x = radius

        if (coordDir < 2000):
            self.x += vx
        else:
            if (vx < 0):
                self.x += vx
            else:
                # self.x = radius
                self.x = 2000 - radius

        if (coordCima > 0):
            self.y += vy
        else:
            if (vy > 0):
                self.y += vy
            else:
                self.y = radius

        if (coordBaixo < 2000):
            self.y += vy
        else:
            if (vy < 0):
                self.y += vy
            else:
                self.y = 2000 - radius



    def get_acceptconf_status(self):
        return self.acceptedConfig

    def accepted_conf(self):
        self.acceptedConfig = True

    def get_watcher_port(self):
        return self.watcherport

