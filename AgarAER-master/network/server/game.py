import uuid
from .player import ServerPlayer
from .cell import CellList
class Game:
    def __init__(self) -> None:
        self.players = {}
        self.cells = CellList(500)
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


    def update_from_player(self, id, p_update):
        if id in self.players:
            self.players[id].update(p_update)
            cells = p_update['cells_eaten']
            for c in cells:
                self.cells.add_to_cells_eaten(c)
                self.cells.removeByPoint(c)

    def start(self):
        pass

    def get_player(self,id):
        return self.players.get(id)

    def get_player_list(self):
        return self.players.values()

    def get_player_count(self):
        return len(self.players.values())

    def get_player_names(self):
        return [p.name for p in self.players]

    def convertGameToDic(self):
        game = {
            'players' : [p.convert_to_dic() for p in self.players.values()],
            'cells' : [(c.get_x(),c.get_y()) for c in self.cells.get_list()],
            'port' : self.get_port()
        }
        return game

    def brief_convert_game_to_dic(self):
        game = {
            'players' : [p.brief_convert_to_dic() for p in self.players.values()],
            'cells_eaten' : self.cells.get_cells_eaten()
        }
        self.cells.clean_eaten_cells()
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


    def get_cells(self):
        return self.cells.get_list()


    def remove_player(self):
        pass


    def get_port(self):
        return self.port