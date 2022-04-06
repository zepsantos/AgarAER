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
        # { Name : Mass }
        sorted_Dict = {}
        sorted_Dict[self.current_player.name] = self.current_player.mass
        for player in self.players:
            sorted_Dict[player.name]=player.mass
        return sorted_Dict
            
        
    def draw(self):
        counter=1
       
        w,h = font.size("Score: "+str(int(self.current_player.mass*2))+" ")
        self.surface.blit(pygame.transform.scale(SCOREBOARD_SURFACE, (w, h)),
                          (8,SCREEN_HEIGHT-30))
        self.surface.blit(LEADERBOARD_SURFACE,(SCREEN_WIDTH-160,15))
        drawText("Score: " + str(int(self.current_player.mass*2)),(10,SCREEN_HEIGHT-30))
        self.surface.blit(big_font.render("Leaderboard", 0, (255, 255, 255)), (SCREEN_WIDTH-157, 20))
        
        counter=1
        counter_str = str(counter)
        message = counter_str + self.current_player.name
        drawText(message,(SCREEN_WIDTH-157,20+(2*counter)*10))
        counter=2
                    
        #for key in (sorted(self.players.values(), key=operator.attrgetter('mass'))):
            #print(key.mass)
        #sorted_Dic = sortDic_byMass(self) 
        
        sorted_Dict = {}
        sorted_Dict[self.current_player.name] = self.current_player.mass
        for player in self.players.values():
            sorted_Dict[player.name]=player.mass
        
        sorted_d = dict( sorted(sorted_Dict.items(), key=operator.itemgetter(1),reverse=True)) 
            
        print(sorted_d)      
            
        counter=1
        for key in sorted_d:    
            counter_str = str(counter)
            message = counter_str + key
            drawText(message,(SCREEN_WIDTH-157,20+(2*counter)*10))
            counter+=1
            