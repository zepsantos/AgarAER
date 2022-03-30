import pygame
from common import SCREEN_HEIGHT,SCOREBOARD_SURFACE,SCREEN_WIDTH,MAIN_SURFACE,LEADERBOARD_SURFACE,drawText
from drawable import Drawable

""" VAMOS ter de ser nós a implementar um hud também não tava feito para o que nós queriamos era estático
"""
class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen.
    """
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        
    def draw(self):
        """w,h = pygame.font.size("Score: "+str(int(blob.mass*2))+" ")
        self.surface.blit(pygame.transform.scale(SCOREBOARD_SURFACE, (w, h)),
                          (8,SCREEN_HEIGHT-30))
        self.surface.blit(LEADERBOARD_SURFACE,(SCREEN_WIDTH-160,15))
        drawText("Score: " + str(int(blob.mass*2)),(10,SCREEN_HEIGHT-30))
        self.surface.blit(big_font.render("Leaderboard", 0, (255, 255, 255)),
                          (SCREEN_WIDTH-157, 20))
        drawText("1. G #1",(SCREEN_WIDTH-157,20+25))
        drawText("2. G #2",(SCREEN_WIDTH-157,20+25*2))
        drawText("3. ISIS",(SCREEN_WIDTH-157,20+25*3))
        drawText("4. ur mom",(SCREEN_WIDTH-157,20+25*4))
        drawText("5. w = pro team",(SCREEN_WIDTH-157,20+25*5))
        drawText("6. jumbo",(SCREEN_WIDTH-157,20+25*6))
        drawText("7. [voz]plz team",(SCREEN_WIDTH-157,20+25*7))
        drawText("8. G #3",(SCREEN_WIDTH-157,20+25*8))
        drawText("9. doge",(SCREEN_WIDTH-157,20+25*9))
        if(blob.mass <= 500):
            common.drawText("10. G #4",(SCREEN_WIDTH-157,20+25*10))
        else:
            common.drawText("10. Viliami",(SCREEN_WIDTH-157,20+25*10),(210,0,0)) """