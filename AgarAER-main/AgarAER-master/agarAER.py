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

class agarAER :

    # Other Definitions
    NAME = "agarAER.py"
    VERSION = "0.0"

    #Pygame initialization
    pygame.init()
    pygame.display.set_caption("{} - v{}".format(NAME, VERSION))

    player_name = 'gostosa'

    #agarGame.startGameLoop()


    def check_name_test(self,value: str) -> None:
        """
        This function tests the text input widget.
        :param value: The widget value
        """
        self.player_name = value
        
        
    def mainMenu(self):
        menu = pygame_menu.Menu('agarAER.io', 1200, 800,
               theme=pygame_menu.themes.THEME_BLUE)
        name = menu.add.text_input('Name :', font_color='Black', default='player', onreturn=self.check_name_test)
        
    
        cam = Camera()
        current_Player = Player(common.MAIN_SURFACE,cam,1, self.player_name,300)
        agargame = agarGame(current_Player,cam)
        agargame.configGame({})
        menu.add.button('Play', agargame.startGameLoop)
        menu.add.button('Quit', pygame_menu.events.EXIT) 
        menu.mainloop(common.MAIN_SURFACE)


    def gameOver(self):
        menu = pygame_menu.Menu('agarAER.io', 1200, 800,
               theme=pygame_menu.themes.THEME_BLUE)
        menu.add.text_input('Name :')
        menu.add.text('GAME OVER')
        menu.add.button('Main Menu', self.mainMenu)
        menu.add.button('Quit', pygame_menu.events.EXIT) 
        menu.mainloop(common.MAIN_SURFACE)  

    mainMenu()