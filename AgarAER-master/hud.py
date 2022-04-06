from unittest.util import _count_diff_all_purpose
import pygame
import operator
from common import SCREEN_HEIGHT,SCOREBOARD_SURFACE,SCREEN_WIDTH,MAIN_SURFACE,LEADERBOARD_SURFACE,big_font,font, drawText
from player import Player
from drawable import Drawable

""" VAMOS ter de ser nós a implementar um hud também não tava feito para o que nós queriamos era estático
"""
class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen.
    """
    
    def __init__(self, surface, camera, current_player, players):
        super().__init__(surface, camera)
        self.current_player = current_player
        self.players = players
        
    def sortDic_byMass(self):
        temp = self.players
        temp[len(temp)] = self.current_player
        final = sorted(self.players.values(), key=operator.attrgetter('mass'))  
        return final
            
        
    def draw(self):
        counter=1
       
        w,h = font.size("Score: "+str(int(self.current_player.mass*2))+" ")
        self.surface.blit(pygame.transform.scale(SCOREBOARD_SURFACE, (w, h)),
                          (8,SCREEN_HEIGHT-30))
        self.surface.blit(LEADERBOARD_SURFACE,(SCREEN_WIDTH-160,15))
        drawText("Score: " + str(int(self.current_player.mass*2)),(10,SCREEN_HEIGHT-30))
        self.surface.blit(big_font.render("Leaderboard", 0, (255, 255, 255)), (SCREEN_WIDTH-157, 20))
        
        
        
        
        for key in (sorted(self.players.values(), key=operator.attrgetter('mass'))):
            print(key.mass)
            '''
            if(self.current_player.mass > key.mass):
                counter_str = str(counter)
                message = counter_str + self.current_player.name
                drawText(message,(SCREEN_WIDTH-157,20+(2*counter)*10))
               
            else:
                counter_str = str(counter)
                message = counter_str + self.key.name
                drawText(message,(SCREEN_WIDTH-157,20+(2*counter)*10))
            counter+=1
            '''
       
        if(self.current_player.mass <= 500):
            drawText("10. G #4",(SCREEN_WIDTH-157,20+25*10))
        else:
            drawText("10. Viliami",(SCREEN_WIDTH-157,20+25*10),(210,0,0)) 
            