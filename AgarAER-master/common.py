import pygame
import math
# Definição de dimensões
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (2000,2000)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
SCOREBOARD_SURFACE = pygame.Surface((95,25),pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155,278),pygame.SRCALPHA) 
SCOREBOARD_SURFACE.fill((50,50,50,80))
LEADERBOARD_SURFACE.fill((50,50,50,80))    
pygame.font.init()
try:
    font = pygame.font.Font("/home/mjloirinha/Downloads/Ubuntu/Ubuntu-Medium.ttf",20)
    big_font = pygame.font.Font("/home/mjloirinha/Downloads/Ubuntu/Ubuntu-Bold.ttf",24)
except:
    print("Font file not found: Ubunto-Medium")
    font = pygame.font.SysFont('times',20,True)
    big_font = pygame.font.SysFont('times',24,True)

# Auxiliary Functions
def drawText(message,pos,color=(255,255,255)):
    """Blits text to main (global) screen.
    """
    MAIN_SURFACE.blit(font.render(message,1,color),pos)

def getDistance(a, b):
    """Calculates Euclidean distance between given points.
    """
    diffX = math.fabs(a[0]-b[0])
    diffY = math.fabs(a[1]-b[1])
    return ((diffX**2)+(diffY**2))**(0.5)