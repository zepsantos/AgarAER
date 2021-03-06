import datetime
import logging

class NeighborStat:

    def __init__(self,addr):
        self.counter = 0
        self.lastTimeSeen = self.generate_timestamp()
        self.passedByTime = 0
        self.averageDelay = 0
        self.averageDelayToOverlay = 0
        self.lastTimeUpdateAverageOverlay = None
        self.isOverlayNode = False
        self.timeList = []
        self.addr = addr

    def passedBy(self):
        self.counter += 1
        timediff = self.get_time_diff()
        self.update_lastTimeSeen()
        self.passedByTime = self.lastTimeSeen
        self.timeList.append(timediff)
        sum = 0
        for t in self.timeList:
            sum += t
        self.averageDelay = sum/self.counter



    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts

    def get_time_diff(self):
        current_time = self.generate_timestamp()
        return current_time - self.lastTimeSeen

    def update_lastTimeSeen(self):
        self.lastTimeSeen = self.generate_timestamp()

    def get_lastTimeSeen(self):
        return self.lastTimeSeen


    def get_average_delay(self):
        return self.averageDelay

    def get_average_delay_overlay(self):
        return self.averageDelayToOverlay, self.lastTimeUpdateAverageOverlay

    def get_average_delay_withTimeDiff(self):
        if self.lastTimeUpdateAverageOverlay is None:
            return self.averageDelayToOverlay,None
        tmp = (self.generate_timestamp() - self.lastTimeUpdateAverageOverlay)
        return self.averageDelayToOverlay, tmp

    def set_average_delay_overlay(self,delay,timestamp):
        self.averageDelayToOverlay = delay
        self.lastTimeUpdateAverageOverlay = timestamp


    def get_passedByTime(self):
        return self.passedByTime