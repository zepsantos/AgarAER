import datetime

class Neighbor:

    def __init__(self,ip):
        self.ip = ip
        self.lastTimeSeen = self.generate_timestamp()

    def alive(self):
        self.lastTimeSeen = self.generate_timestamp()

    ## VERIFICAR SE TA CERTO
    def isAlive(self):
        current_time = self.generate_timestamp()
        return (current_time - self.timestamp) < 70 ##SLEEP da discovery message é de 50ms logo com uma margem de pacotes perdidos 70 parece bem

    def generate_timestamp(self):
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        return ts