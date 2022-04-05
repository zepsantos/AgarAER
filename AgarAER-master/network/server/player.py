import random


class ServerPlayer:
    def __init__(self,addr,id,name) -> None:
        self.addr = addr
        self.id = id # generateID()
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.color = 2 #escolhe uma cor random
        self.speed = 4 
        self.name = name
        self.killed = []

    def convert_to_dic(self):
        p = {'id':self.id,'x' : self.x, 'y' : self.y, 'mass' : self.mass, 'color' : self.color, 'speed' : self.speed, 'name' : self.name, 'killed' : self.killed}
        return p

    def brief_convert_to_dic(self):
        p = {'id':self.id,'x' : self.x, 'y' : self.y, 'mass' : self.mass, 'speed' : self.speed, 'name' : self.name}
        return p

    def get_id(self):
        return self.id 


    