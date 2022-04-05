import pygame,random,math
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
from drawable import Drawable
from camera import Camera
from agarGame import agarGame
import common

# Other Definitions
NAME = "agarAER.py"
VERSION = "0.0"

#Pygame initialization
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))

    
agarGame = agarGame()
agarGame.configGame({})
agarGame.startGameLoop()
