from drawable import Drawable
from painter import Painter

import random
import common
import pygame
import math

class Player(Drawable):
    """Used to represent the concept of a player.
    """
    COLOR_LIST = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface,camera, id , name):
        super().__init__(surface, camera)
        self.id = id
        self.x = random.randint(100,2000)
        self.y = random.randint(100,2000)
        self.mass = 200
        self.speed = 3
        self.color = col = random.choice(Player.COLOR_LIST)
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []


    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        zoom = self.camera.zoom
        radius= int(self.mass/2 + 3)*zoom
        
        coordCima = (self.y) + radius  
        coordBaixo= (self.y) - radius  
        coordDir= (self.x) + radius  
        coordEsq = (self.x) - radius  
         
        for edible in edibles:
            if( (common.getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2) and (coordDir  < 2000 or coordEsq > 0) and (coordBaixo < 2000 or coordCima> 0) ):
                self.mass+=0.25
                edibles.remove(edible)


    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """
        
        dX, dY = pygame.mouse.get_pos()
        
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(common.SCREEN_HEIGHT)/2, dX - float(common.SCREEN_WIDTH)/2)
        # Convert radians to degrees [-180, 180]
        rotation *= 180/math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(rotation))/90
        vx = self.speed*normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        
        zoom = self.camera.zoom
        radius= int(self.mass/2 + 3)
        #print('raio ',radius)
        
        
        coordCima = (self.y) - radius 
        coordBaixo= (self.y) + radius  
        coordDir= (self.x) + radius  
        coordEsq = (self.x) - radius
        
        #print('centro y ', self.y, 'coordCima ',coordCima, 'coordBaixo ', coordBaixo)
        #print('centro x ', self.x, 'coordDir ',coordDir, 'coordEsq ', coordEsq)
        #print('velX ', vx, 'velY ', vy)
        
        
        if (coordEsq > 0):
            self.x += vx
        else:
            if (vx > 0):
                self.x += vx
            else:
                self.x = radius 
            
        if (coordDir < 2000):
            self.x += vx    
        else:
            if(vx < 0):
                self.x += vx 
            else:
                #self.x = radius  
                self.x = 2000-radius    
                
        if (coordCima > 0):
            self.y += vy
        else:
            if (vy > 0):
                self.y += vy
            else:
                self.y = radius    
                        
                
        if (coordBaixo < 2000):
            self.y += vy    
        else:
            if(vy < 0):
                self.y += vy
            else:
                self.y= 2000-radius     
                   
       
        

    def withinBounds(self,pos):
        (x,y) = pos
        pass
    
    def removePlayer(players,player2remove):
        for  player in players:
            if (player.value == player2remove):
                players.pop(player)
        
        
    def feed(self, players,paintings):
        """Detects other players being inside the radius of current player.
        Those players are eaten.
        """    
        for key,player in players.items():
            if(common.getDistance((player.x, player.y), (self.x,self.y)) <= self.mass/2):
                self.mass+= (player.mass/2) 
                players.pop(key)
                paintings.remove(player)
                
                break
           
                     
        

    def split(self):
        """Unsupported feature.
        """
        pass


    def draw(self):
        """Draws the player as an outlined circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        
        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass/2 + 3)*zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass/2*zoom))
        # Draw player's name
        fw, fh = common.font.size(self.name) ## isto pode tar mal
        common.drawText(self.name, (self.x*zoom + x - int(fw/2), self.y*zoom + y - int(fh/2)),
                 Player.FONT_COLOR)
