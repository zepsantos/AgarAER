import pygame,random,math
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
import logging
from drawable import Drawable
from camera import Camera

import common

class agarGame :
    def __init__(self) -> None:
        self.players = {}

        # Initialize essential entities
        self.cam = Camera()
        self.clock = pygame.time.Clock()
        self.grid = Grid(common.MAIN_SURFACE, self.cam)
        self.cells = CellList(common.MAIN_SURFACE, self.cam, 2000)
        self.painter = Painter()
        self.atTickIsOver = None
        self.current_player = None

        self.hud = HUD(common.MAIN_SURFACE, self.cam)
        self.drawOnScreen()
        
    def drawOnScreen(self):
        self.painter.add(self.grid) 
        self.painter.add(self.cells)
        self.painter.add(self.hud)
        

        

    def set_atTickIsOver(self, atTickIsOver):
        self.atTickIsOver = atTickIsOver

    def startGameLoop(self):
        # Game main loop
        logging.info("Starting game loop")


        for p in self.players.values():
            if not p.is_onScreen():
                p.set_onScreen()
                self.painter.add(p)

        self.hud.set_current_player(self.current_player)
        self.hud.set_players(self.players)
        while  True : #len(self.players) > 0:
            
            self.clock.tick(70)

            cell = Cell(common.MAIN_SURFACE, self.cam)
            self.cells.add(cell)
            
            self.reactToInput()
            
            self.current_player.move()    
                
            #self.current_player.feed(self.players, self.painter.paintings) rever isto
            
            self.current_player.collisionDetection(self.cells.list)
            self.cam.update(self.current_player)
            if self.atTickIsOver is not None:
                self.atTickIsOver(self.current_player)
            common.MAIN_SURFACE.fill((242,251,255))
            # Uncomment next line to get dark-theme
            #common.MAIN_SURFACE.fill((0,0,0))
            self.painter.paint()
            # Start calculating next frame
            pygame.display.flip()
    
  


    def reactToInput(self):
        for e in pygame.event.get():
                if(e.type == pygame.KEYDOWN):
                    if(e.key == pygame.K_ESCAPE):
                        pygame.quit()
                        print("Quiting game!")
                        quit()
                    if(e.key == pygame.K_SPACE):
                        #del(self.cam)
                        self.current_player.split()
                    #if(e.key == pygame.K_w):
                        
                if(e.type == pygame.QUIT):
                    pygame.quit()
                    quit()
                    
    def add_player(self,id,x,y,mass,color,speed,name):
        #tmpid = self.generateID(player)
        p = Player(common.MAIN_SURFACE,self.cam,id , name,mass, color , speed, x, y)
        self.players[id] = p
        if self.current_player is None:
            self.current_player = p
        #self.painter.add(p) #Nota: isto vai dar barraco a adicionar um jogador a meio do jogo


    def set_currentPlayer(self, player):
        self.set_currentPlayer = player    
        
    def remove_player(self,player):
        self.players.pop(player)
        pass

    def update_player(self, id, x, y, mass):
        self.players[id].update(x, y, mass)

    def update_game(self, game):
        players = game['players']
       # for player in players:
           # self.update_player(player['id'], player['x'], player['y'], player['mass'])

    def configGame(self,p,game):
        self.add_player(p['id'],p['x'],p['y'],p['mass'],p['color'],p['speed'],p['name'])
        players = game['players']
        print(players)
        for player in players:
            if player['id'] == p['id']:
                continue
            self.add_player(player['id'],player['x'],player['y'],player['mass'],player['color'],player['speed'],player['name'])
        
            
    def get_player_playing(self):
        return self.current_player


    """ retorna a lista de jogadores menos o proprio player"""
    def getPlayersPlaying(self):
        return self.players.values()