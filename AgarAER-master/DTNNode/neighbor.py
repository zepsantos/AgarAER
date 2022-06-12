import datetime
import logging
import time
from neighborStat import NeighborStat
from repeatTimer import setInterval


class Neighbor:

    def __init__(self, ip):
        self.ip = ip
        self.stats = NeighborStat(self.ip)
        self.sniff = False
        self.connected = False
        self.checkAliveDaemon = self.checkAlive()

    def alive(self):
        if not self.connected:
            self.connected = True
            self.checkAliveDaemon = self.checkAlive()
            self.stats.passedBy()
        else:
            self.stats.update_lastTimeSeen()

    ## VERIFICAR SE TA CERTO
    def isAlive(self):
        current_time = self.generate_timestamp()
        timepassed = (current_time - self.stats.get_lastTimeSeen())
        self.connected = timepassed < 0.7
        return self.connected

    @setInterval(.7)
    def checkAlive(self):
        #logging.debug('CheckAliveNeighb Thread a correr')
        aliveStatus = self.isAlive()
        if aliveStatus == False:
            self.sniff = False
            #logging.debug('CheckAliveNeighb Thread a parar de correr')
            self.checkAliveDaemon.set()
        else:
            
            return

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts

    def set_isOverlay(self, isOverlayNode):
        self.stats.isOverlayNode = isOverlayNode

    def isOverlay(self):
        return self.stats.isOverlayNode

    def get_stats(self):
        return self.stats

    def get_overlay_stats(self):
        return self.stats.get_average_delay_overlay()

    def set_sniff(self, boolean):
        self.sniff = boolean
