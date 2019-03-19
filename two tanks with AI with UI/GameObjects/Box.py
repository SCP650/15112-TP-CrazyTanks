# This class generate a powerup box
import pygame
from GameObject import *
import random

class Box(GameObject):
    @staticmethod
    def init():
        Box.image = pygame.image.load('images/box.png').convert_alpha()
     
        
    def __init__ (self, x,y,screenWidth, screenHeight):
        #center of the box
        self.sw, self.sh = screenWidth,screenHeight
        self.x, self.y = x,y
        self.w, self.h = screenWidth//10, screenHeight//10
        self.side = 20
        Box.image = pygame.transform.smoothscale(Box.image, (self.w, self.h))
        
        
        super().__init__(self.x,self.y,Box.image,self.side//2)
        
 
    def getRanLocation(self,map,tank1,tank2):
        #get a location that is not colliding with walls or any tanks
        isColiding = True
        while isColiding:
            x,y = random.randint(1,self.sw),random.randint(1,self.sh)
            box = Box (x, y,self.sw,self.sh)
            if pygame.sprite.collide_mask(box,map) == None and pygame.sprite.collide_mask(box,tank1) == None and pygame.sprite.collide_mask(box,tank2) == None:
                isColiding = False
                
                
                
        return box
   
        
    def update(self, screenWidth, screenHeight):
         
        super(Box, self).update(screenWidth, screenHeight)
        