#this class generate a map for the players to play on
import pygame
from GameObject import *
import random
class Map(GameObject):
    
    @staticmethod
    def init(start = False):
        
        if start == False:
            #load all map images
            mapNum = 7 #currently have 7 maps 
            i = 1 #1st map
        else:
            #only want the transparent map
            mapNum = 0
            i = 0
            
        Map.mapImages = [ ]
        while i <= mapNum:
           
            filename = 'images/maps/'+str(i)+'.PNG'
            temp = pygame.image.load(filename).convert_alpha()
            Map.mapImages.append(temp)
            i += 1
            
    def __init__(self, screenWidth, screenHeight):
        map = random.choice(Map.mapImages)
        map = pygame.transform.smoothscale(map, (screenWidth, screenHeight))
        super(Map,self).__init__(400,400, map, screenWidth)
        self.mask = pygame.mask.from_surface(map)
