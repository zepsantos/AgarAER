import uuid
from .player import ServerPlayer
class Game:
    def __init__(self) -> None:
        self.players = {}
        self.port = 6000
        self.newplayers = []
    def add_player(self,addr,id,name):
        if id is None:
            temp_id = self.generate_id()
            p = ServerPlayer(addr,temp_id,name)
            self.players[temp_id] = p
            return p
        else:
            print('not implemented')


    def update_player(self,id, p_update):
        self.players[id].update(p_update)

    def start(self):
        pass

    def get_player(self,id):
        return self.players[id]

    def get_player_list(self):
        return self.players.values()

    def get_player_count(self):
        return len(self.players.values())

    def get_player_names(self):
        return [p.name for p in self.players]

    def convertGameToDic(self):
        game = {
            'players' : [p.convert_to_dic() for p in self.players.values()],
            'port' : self.get_port()
        }
        return game

    def brief_convert_game_to_dic(self):
        game = {
            'players' : [p.brief_convert_to_dic() for p in self.players.values()]
        }
        return game
    def generate_id(self):
        temp_id = uuid.uuid4()
        while temp_id in self.players:
            temp_id = uuid.uuid4()
        return str(temp_id)


    def get_newplayers(self):
        tmp = []
        for p,c in self.newplayers:
            self.newplayers.remove((p,c))
            c -= 1
            tmp.append(p.convert_to_dic())
            if c != 0:
                self.newplayers.append((p,c))
        return tmp

    def add_to_newplayers(self,p,warntime):
        self.newplayers.append((p,warntime))





    def remove_player(self):
        pass


    def get_port(self):
        return self.port