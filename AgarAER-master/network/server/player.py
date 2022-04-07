import random


class ServerPlayer:
    COLOR_LIST = [
        (37,7,255),
        (35,183,253),
        (48,254,241),
        (19,79,251),
        (255,7,230),
        (255,7,23),
        (6,254,13)]

    def __init__(self,addr,id,name) -> None:
        self.addr = addr
        self.id = id 
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
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
        self.x = p_update.get('x',self.x)
        self.y = p_update.get('y',self.y)
        self.mass = p_update.get('mass',self.mass)