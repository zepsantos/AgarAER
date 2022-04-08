from drawable import Drawable
import random
import pygame
class Cell(Drawable): # Semantically, this is a parent class of player
    """Used to represent the fundamental entity of game.
    A cell can be considered as a quantom of mass.
    It can be eaten by other entities.
    """
    CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255)]
    
    def __init__(self, surface, camera,x,y):
        super().__init__(surface, camera)
        self.x = x
        self.y = y
        self.mass = 7
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        """Draws a cell as a simple circle.
        """
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass*zoom))
        

class CellList(Drawable):
    """Used to group and organize cells.
    It is also keeping track of living/ dead cells.
    """

    def __init__(self, surface, camera,cellsposition, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        self.eaten_cells = []
        for i in range(self.count):
            (x,y) = cellsposition[i]
            self.list.append(Cell(self.surface, self.camera,x,y))
        
    def add(self,cell):
        if not cell: return
        self.list.append(cell)

    def add_list_from_server(self,cells):
        for x,y in cells:
            self.list.append(Cell(self.surface, self.camera,x,y))

    def draw(self):
        for cell in self.list:
            cell.draw()

    def add_to_eaten_cells(self,cell):
        self.eaten_cells.append((cell.x,cell.y))

    def get_eaten_cells(self):
        return self.eaten_cells

    def clean_eaten_cells(self):
        self.eaten_cells = []

    def removeByPoint(self,cell):
        x,y = cell
        for i in range(len(self.list)):
            if self.list[i].x == x and self.list[i].y == y:
                self.list.pop(i)
                break
