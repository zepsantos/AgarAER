from tkinter import CENTER
import pygame as pg
from drawable import Drawable
import common
class Grid(Drawable):
    """Used to represent the background grid.
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230,240,240)

   
    
    def draw(self):
        # A grid is a set of horizontal and prependicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        
        
        for i in range(0,common.PLATFORM_WIDTH,25):
           pg.draw.line(self.surface,  self.color, (x, i*zoom + y), (2000*zoom + x, i*zoom + y), 3)
           pg.draw.line(self.surface, self.color, (i*zoom + x, y), (i*zoom + x, 2000*zoom + y), 3)