from drawable import Drawable

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
    
    def __init__(self, surface,camera, id , name = ""):
        super().__init__(surface, camera)
        self.id = id
        self.x = random.randint(100,400)
        self.y = random.randint(100,400)
        self.mass = 20
        self.speed = 4
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
        for edible in edibles:
            if(common.getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
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
        if tmpX > 0+int((self.mass/2 + 3))  and tmpX < 2000-int((self.mass/2 + 3)):
            self.x = tmpX
        if tmpY >0+int((self.mass/2 + 3)) and tmpY<2000-int((self.mass/2 + 3)):
            self.y = tmpY        
        #print(tmpX , tmpY)
     
        

    def feed(self, players):
        """Detects other players being inside the radius of current player.
        Those players are eaten.
        """
        for player in players:
            if(common.getDistance((player.x, player.y), (self.x,self.y)) <= self.mass/2):
                self.mass+=0.5
                players.remove(player)
        pass

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
