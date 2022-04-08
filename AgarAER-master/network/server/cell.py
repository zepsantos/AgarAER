import random


class Cell():  # Semantically, this is a parent class of player
    """Used to represent the fundamental entity of game.
    A cell can be considered as a quantom of mass.
    It can be eaten by other entities.
    """

    def __init__(self):
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_mass(self):
        return self.mass



class CellList():
    """Used to group and organize cells.
    It is also keeping track of living/ dead cells.
    """

    def __init__(self, numOfCells):
        super()
        self.count = numOfCells
        self.list = []
        self.cells_eaten = []
        for i in range(self.count):
            self.list.append(Cell())

    def add(self, cell):
        self.list.append(cell)

    def get_list(self):
        return self.list
    

    def generate_cells(self, numOfCells):
        tmp = []
        for i in range(numOfCells):
            c = Cell()
            self.add(c)
            tmp.append(c)
        return tmp

    def get_cells_eaten(self):
        return self.cells_eaten

    def add_to_cells_eaten(self, cell):
        self.cells_eaten.append(cell)

    def removeByPoint(self,cell):
        x,y = cell
        for i in range(len(self.list)):
            if self.list[i].x == x and self.list[i].y == y:
                self.list.pop(i)
                break

    def clean_eaten_cells(self):
        self.cells_eaten = []