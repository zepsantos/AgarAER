import pygame,random,math
from painter import Painter
from cell import Cell,CellList
from player import Player
from hud import HUD
from grid import Grid
from drawable import Drawable
from camera import Camera
import common

# Other Definitions
NAME = "agarAER.py"
VERSION = "0.0"

#Pygame initialization
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))
clock = pygame.time.Clock()
    

# Initialize essential entities
cam = Camera()

grid = Grid(common.MAIN_SURFACE, cam)
cells = CellList(common.MAIN_SURFACE, cam, 2000)
blob = Player(common.MAIN_SURFACE, cam, "GeoVas")
hud = HUD(common.MAIN_SURFACE, cam)


painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(blob)
painter.add(hud)

# Game main loop
while(True):
    
    clock.tick(70)
    
    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                print("Quiting game!")
                quit()
            if(e.key == pygame.K_SPACE):
                del(cam)
                blob.split()
            if(e.key == pygame.K_w):
                blob.feed()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()
    
    blob.move()
    blob.collisionDetection(cells.list)
    cam.update(blob)
    common.MAIN_SURFACE.fill((242,251,255))
    # Uncomment next line to get dark-theme
    #surface.fill((0,0,0))
    painter.paint()
    # Start calculating next frame
    pygame.display.flip()