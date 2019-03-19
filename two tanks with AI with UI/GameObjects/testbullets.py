#this is the test bullets that AI shoot to test distance and player's location
import pygame
import math
from GameObject import *

class testBullets(GameObject):
    speed = 7
    time = 400
    size = 7

        
    def __init__ (self, x,y,angle,w,h):
        angle = math.radians(angle)
        size = testBullets.size
        self.x, self.y = x,y
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(image, (0, 0, 0), (size // 2, size // 2), size // 2)
        super(testBullets, self).__init__(self.x, self.y, image, size // 2)
        vy = -testBullets.speed * math.cos(angle)
        vx = -testBullets.speed * math.sin(angle)
         
        self.velocity = vx,vy
         
        self.timeOnScreen = 0
        
    def update(self,screenWidth, screenHeight, map):
        super(testBullets, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1
        if self.timeOnScreen > testBullets.time:
            self.kill()
    
    def collide(self,map,screenWidth, screenHeight):
        vx,vy = self.velocity
        if pygame.sprite.collide_mask(self,map):
            self.velocity = -vx, vy
            super(testBullets, self).update(screenWidth, screenHeight)
            
            if pygame.sprite.collide_mask(self,map):
                
                self.velocity = vx, -vy
                super(testBullets, self).update(screenWidth, screenHeight)
                super(testBullets, self).update(screenWidth, screenHeight)
        if pygame.sprite.collide_mask(self,map):
            self.velocity = -vx, -vy
            super(testBullets, self).update(screenWidth, screenHeight)
           
        
        