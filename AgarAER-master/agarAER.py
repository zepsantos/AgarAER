import threading
import time
from json.tool import main
import pygame,random,math

from network import NetworkClient, PlayerUpdate
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
from drawable import Drawable
from camera import Camera
from agarGame import agarGame
import common
import logging
import pygame_menu

logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s')

 # Other Definitions
NAME = "agarAER.py"
VERSION = "0.0"

#Pygame initialization
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))

player_name = 'gostosa'


client = NetworkClient()

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
    menu.add.text_input('Name :', font_color='Black', default=player_name, onchange=retrieve_name)
    menu.add.button('Play', initConnectionToServer)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(common.MAIN_SURFACE)



#Inicia ligaçao com o server (Configuracao do jogo)
def initConnectionToServer():
    client.initConnectionToServer(player_name, startGame)


# Inicia a thread que vai escutar o canal do jogo e o jogo
def startGame(config):
    #logging.info('Config obtida: {}'.format(config))
    agargame = agarGame()
    p = config['player']
    game = config['game']
    agargame.configGame(p,game)
    listenGameThread = threading.Thread(target=client.listenToGameChannel, args=(game['port'],agargame.update_game))
    listenGameThread.start()
    agargame.set_atTickIsOver(send_playerUpdateToServer)
    agargame.startGameLoop()
    """if config == {}:
            time.sleep(1)
            client.initConnectionToServer(player_name,startGame)
            return"""


#Envia reports dos jogadores para o servidor
def send_playerUpdateToServer(player,cells):
    p_update = {'rotation':player.get_lastrotation(), 'mass':player.get_mass(), 'cells_eaten': cells.get_eaten_cells() }
    cells.clean_eaten_cells()
    msg = PlayerUpdate(p_update)
    msg.set_sender(player.get_id())
    client.sendToServer(msg)

def gameOver():
    menu = pygame_menu.Menu('agarAER.io', 1200, 800,
            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :')
    menu.add.text('GAME OVER')
    menu.add.button('Main Menu', mainMenu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(common.MAIN_SURFACE)

mainMenu()