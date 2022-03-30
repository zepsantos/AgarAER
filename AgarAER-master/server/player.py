class serverPlayer:
    def __init__(self) -> None:
        self.id = 1 # generateID()
        self.x = 1 #random
        self.y = 2 #random
        self.mass = 20
        self.color = 2 #escolhe uma cor random
        self.speed = 4 
        self.name = "teste"
        self.killed = []


    def get_id(self):
        return self.id 


    