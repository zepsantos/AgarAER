import uuid
from .player import ServerPlayer
class Game:
    def __init__(self) -> None:
        self.players = {}
        self.port = 6000

    def add_player(self,addr,id,name):
        if id is None:
            temp_id = self.generate_id()
            p = ServerPlayer(addr,temp_id,name)
            self.players[temp_id] = p
            return p
        else:
            print('not implemented')

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
            'players' : [p.convert_to_dic() for p in self.players.values()]
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
        return temp_id

    def remove_player(self):
        pass


    def get_port(self):
        return self.port