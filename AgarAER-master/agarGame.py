import pygame,random,math
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
from drawable import Drawable
from camera import Camera
import common

class agarGame :
    def __init__(self,painter,cam) -> None:
        self.players = {}
        self.counter = 0
        self.painter = painter
        self.cam = cam
        self.current_player = Player(common.MAIN_SURFACE,cam, "GeoVas")

    def add_player(self,player):
        #tmpid = self.generateID(player)
        self.players[self.counter] = player
        self.counter += 1
        self.painter.add(player)
        
    def remove_player(self):
        pass
    
    def update_player(self,player):
        pass
        
    def get_player_playing(self):
        return self.current_player


    """ retorna a lista de jogadores menos o proprio player"""
    def getPlayersPlaying(self):
        return self.players.values()