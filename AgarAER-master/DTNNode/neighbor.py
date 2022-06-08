import datetime
import logging

from neighborStat import NeighborStat
from repeatTimer import RepeatTimer


class Neighbor:

    def __init__(self, ip):
        self.ip = ip
        self.stats = NeighborStat(self.ip)
        self.isOverlay = False
        self.connected = False
        self.checkAliveDaemon = RepeatTimer(1, self.checkAlive)
        self.checkAliveDaemon.daemon = True
        self.checkAliveDaemon.start()

    def alive(self):
        if not self.connected:
            self.connected = True
            self.checkAliveDaemon.start()
            self.stats.passedBy()
        else:
            self.stats.update_lastTimeSeen()

    ## VERIFICAR SE TA CERTO
    def isAlive(self):
        current_time = self.generate_timestamp()
        self.connected = ((current_time - self.stats.get_lastTimeSeen()) < 70)
        return self.connected

    def checkAlive(self):
        logging.debug('CheckAliveNeighb Thread a correr')
        if not self.isAlive():
            logging.debug('CheckAliveNeighb Thread a parar de correr')
            self.checkAliveDaemon.cancel()
        else:
            return

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts

    def set_isOverlay(self):
        self.isOverlay = True
