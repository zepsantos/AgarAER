from drawable import Drawable
import random
import pygame
import math
import common

class Player(Drawable):
    """Used to represent the concept of a player.
    """
    FONT_COLOR = (50, 50, 50)
    
    def __init__(self, surface,camera, id , name,mass, color , speed, x, y):
        super().__init__(surface, camera)
        self.id = id
        self.x = x
        self.y = y
        self.mass = mass
        self.speed = speed
        self.color = col = color
        self.rotation = 0

        self.onScreen = False
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.pieces = []

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_mass(self):
        return self.mass

    def set_onScreen(self):
        self.onScreen = True



    def is_onScreen(self):
        return self.onScreen

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
            if (common.getDistance((edible.x, edible.y), (self.x, self.y)) <= self.mass / 2) and (coordDir < 2000 or coordEsq > 0) and (coordBaixo < 2000 or coordCima > 0):
                self.mass+=0.25
                edibles.remove(edible)
                return edible
        return None

    def move(self):
        """Updates players current position depending on player's mouse relative position.
        """
        
        dX, dY = pygame.mouse.get_pos()
        
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        self.rotation = math.atan2(dY - float(common.SCREEN_HEIGHT) / 2, dX - float(common.SCREEN_WIDTH) / 2)
        # Convert radians to degrees [-180, 180]
        self.rotation *= 180 / math.pi
        """
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (90 - math.fabs(self.rotation))/90
        vx = self.speed*normalized
        vy = 0
        if self.rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        
        zoom = self.camera.zoom
        radius= int(self.mass/2 + 3)
        #print('raio ',radius)
        
        
        coordCima = (self.y) - radius 
        coordBaixo= (self.y) + radius  
        coordDir= (self.x) + radius  
        coordEsq = (self.x) - radius

        
        
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

        self.lastposmove = (self.x,self.y)
        """
                   
       
    def get_lastrotation(self):
        return self.rotation

    
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

    def update(self, x, y, mass):
        self.acceptedConfig = True
        self.set_x(x)
        self.set_y(y)
        #self.set_mass(mass)

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_mass(self, mass):
        self.mass = mass

        

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
