import datetime
import logging

from neighborStat import NeighborStat
from repeatTimer import RepeatTimer


class Neighbor:

    def __init__(self, ip):
        self.ip = ip
        self.stats = NeighborStat(self.ip, self.isOverlay)
        self.isOverlay = False
        self.sniff = False
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
            self.sniff = False
            logging.debug('CheckAliveNeighb Thread a parar de correr')
            self.checkAliveDaemon.cancel()
        else:
            return

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts

    def set_isOverlay(self, isOverlayNode):
        self.isOverlay = isOverlayNode

    def isOverlay(self):
        return self.isOverlay

    def get_stats(self):
        return self.stats

    def get_overlay_stats(self):
        return self.stats.get_average_delay_overlay()

    def set_sniff(self, boolean):
        self.sniff = boolean
