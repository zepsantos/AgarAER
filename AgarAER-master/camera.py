from common import SCREEN_HEIGHT,SCREEN_WIDTH
from player import Player
class Camera:
    """Used to represent the concept of POV.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    
    def centre(self,blobOrPos):
        """Makes sure that the given object will be at the center of player's view. 
        Zoom is taken into account as well.
        """
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x*self.zoom)) - x + (SCREEN_WIDTH/2)
            self.y = (y - (y*self.zoom)) - y + (SCREEN_HEIGHT/2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos


    def update(self, target):
        self.zoom = 100/(target.mass)+0.3
        self.centre(target)