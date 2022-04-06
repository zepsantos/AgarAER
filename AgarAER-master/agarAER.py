from json.tool import main
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
import pygame_menu



 # Other Definitions
NAME = "agarAER.py"
VERSION = "0.0"

#Pygame initialization
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))

player_name = 'gostosa'

#agarGame.startGameLoop()


def retrieve_name(value: str) -> None:
        """
        This function tests the text input widget.
        :param value: The widget value
        """
        global player_name
        player_name = value
        
        
def mainMenu():
    menu = pygame_menu.Menu('agarAER.io', 1200, 800,
               theme=pygame_menu.themes.THEME_BLUE)
    name = menu.add.text_input('Name :', font_color='Black', default='player', onchange=retrieve_name)
        
    
    cam = Camera()
    current_Player = Player(common.MAIN_SURFACE,cam,1, player_name,300)
    agargame = agarGame(current_Player,cam)
    agargame.configGame({})
    menu.add.button('Play', agargame.startGameLoop)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(common.MAIN_SURFACE)


def gameOver():
    menu = pygame_menu.Menu('agarAER.io', 1200, 800,
            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :')
    menu.add.text('GAME OVER')
    menu.add.button('Main Menu', mainMenu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(common.MAIN_SURFACE)

mainMenu()