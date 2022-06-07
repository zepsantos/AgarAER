import datetime


class NeighborStat:

    def __init__(self,addr):
        self.counter = 0
        self.lastTimeSeen = self.generate_timestamp()
        self.averageDelay = 10000
        self.timeList = []
        self.addr = addr

    def passedBy(self):
        self.counter += 1
        timediff = self.get_time_diff()
        self.update_lastTimeSeen()
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