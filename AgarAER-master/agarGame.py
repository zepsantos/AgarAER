import pygame,random,math
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
import queue
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
        self.cells = None
        self.painter = Painter()
        self.atTickIsOver = None
        self.current_player = None
        self.current_play_queue = queue.Queue()
        self.packets_in = 0
        self.networkTime = 0
        self.hud = HUD(common.MAIN_SURFACE, self.cam)
        self.drawOnScreen()
        
    def drawOnScreen(self):
        self.painter.add(self.grid)
        #self.painter.add(self.cells)
        self.painter.add(self.hud)
        

        

    def set_atTickIsOver(self, atTickIsOver):
        self.atTickIsOver = atTickIsOver

    def startGameLoop(self):
        # Game main loop
        logging.info("Starting game loop")


        self.drawPlayers()
        self.painter.add(self.cells)
        self.hud.set_current_player(self.current_player)
        self.hud.set_players(self.players)
        counter = 0
        debugtime = pygame.time.get_ticks()
        packet_out = 0
        while  True :
            self.clock.tick(60)
            currentTime = pygame.time.get_ticks()

            #cell = Cell(common.MAIN_SURFACE, self.cam)
            #self.cells.add(cell)
            playerMove = self.current_play_queue.get()
            self.current_player.update(playerMove['x'], playerMove['y'], playerMove['mass'])

            self.reactToInput()
            counter += 1
            self.current_player.move()    
                
            #self.current_player.feed(self.players, self.painter.paintings) rever isto
            
            cell_eaten = self.current_player.collisionDetection(self.cells.list)
            if cell_eaten:
                self.cells.add_to_eaten_cells(cell_eaten)
            self.cam.update(self.current_player)
            if self.atTickIsOver is not None and currentTime - self.networkTime > 5:
                self.atTickIsOver(self.current_player,self.cells)
                packet_out += 1
                self.networkTime = pygame.time.get_ticks()
            common.MAIN_SURFACE.fill((242,251,255))
            # Uncomment next line to get dark-theme
            #common.MAIN_SURFACE.fill((0,0,0))
            self.painter.paint()

            if currentTime - debugtime > 1000:
                logging.info("FPS: {} , packet out {} in {}".format(counter, packet_out,self.packets_in))
                debugtime = pygame.time.get_ticks()
                counter = 0
                packet_out = 0
                self.packets_in = 0
                self.current_play_queue.empty()
            # Start calculating next frame
            pygame.display.flip()
    
  ## verificar no painter se existem os players de forma a remover dps
    def drawPlayers(self):
        for p in self.players.values():
            if not p.is_onScreen():
                p.set_onScreen()
                self.painter.add(p)

    def reactToInput(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if(e.key == pygame.K_ESCAPE):
                    pass
                    #pygame.quit()
                    #print("Quiting game!")
                    #quit()
                if(e.key == pygame.K_SPACE):
                    pass
                        #del(self.cam)
                        #self.current_player.split()
                    #if(e.key == pygame.K_w):
                        
            if(e.type == pygame.QUIT):
                pygame.quit()
                quit()
                    
    def add_player(self,id,x,y,mass,color,speed,name):
        #tmpid = self.generateID(player)
        p = Player(common.MAIN_SURFACE,self.cam,id , name,mass, color , speed, x, y)
        if id not in self.players:
            self.players[id] = p
            if self.current_player is None:
                self.current_player = p
        else:
            pass
            #Caso exista o id do jogador 
        #self.painter.add(p) #Nota: isto vai dar barraco a adicionar um jogador a meio do jogo


    def set_currentPlayer(self, player):
        self.current_player = player
        
    def remove_player(self,player):
        self.players.pop(player)
        pass

    def update_player(self, id, x, y, mass):
        if id in self.players:
            self.players[id].update(x, y, mass)

    def update_game(self, msg):
        logging.debug("Received update from server ping: {}".format(msg.get_ping()))
        self.packets_in += 1
        game = msg.get_game_state()
        if msg.get_newplayers_status() :
            for p in msg.get_newplayers():
                if p['id'] not in self.players:
                    self.add_player(p['id'],p['x'],p['y'],p['mass'],p['color'],p['speed'],p['name'])
                    self.painter.add(self.players[p['id']])
        players = game['players']
        #cells = game.get('cells', [])
        #self.cells.add(cells)
        cells_eaten = game.get('cells_eaten', [])
        for cell in cells_eaten:
            self.cells.removeByPoint(cell)

        for player in players:
            self.update_player(player['id'], player['x'], player['y'], player['mass'])
            if player['id'] == self.current_player.get_id():
                self.current_play_queue.put(player)

    def configGame(self,p,game):
        self.add_player(p['id'],p['x'],p['y'],p['mass'],p['color'],p['speed'],p['name'])
        players = game['players']
        cellsserverl = game['cells']
        self.cells = CellList(common.MAIN_SURFACE, self.cam, cellsserverl,len(cellsserverl))
        for player in players:
            if player['id'] == p['id']:
                continue
            self.add_player(player['id'],player['x'],player['y'],player['mass'],player['color'],player['speed'],player['name'])
        
            
    def get_player_playing(self):
        return self.current_player


    """ retorna a lista de jogadores menos o proprio player"""
    def getPlayersPlaying(self):
        return self.players.values()