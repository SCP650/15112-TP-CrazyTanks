#this class generate a usual bullet when tank fire
import pygame
import math
from GameObject import *

class Bullets(GameObject):
    speed = 7
    time = 300
    size = 10

        
    def __init__ (self, x,y,angle,w,h):
        angle = math.radians(angle)
        size = Bullets.size
        self.x, self.y = x-w//2*math.sin(angle),y-h//2*math.cos(angle)
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(image, (0, 0, 0), (size // 2, size // 2), size // 2)
        super(Bullets, self).__init__(self.x, self.y, image, size // 2)
        vy = -Bullets.speed * math.cos(angle)
        vx = -Bullets.speed * math.sin(angle)
         
        self.velocity = vx,vy
         
        self.timeOnScreen = 0
        
    def update(self,screenWidth, screenHeight):
        super(Bullets, self).update(screenWidth, screenHeight)
        self.timeOnScreen += 1
        if self.timeOnScreen > Bullets.time:
            self.kill()
    
    def collide(self,map,screenWidth, screenHeight):
        vx,vy = self.velocity
        if pygame.sprite.collide_mask(self,map):
            self.velocity = -vx, vy
            super(Bullets, self).update(screenWidth, screenHeight)
            
            if pygame.sprite.collide_mask(self,map):
                
                self.velocity = vx, -vy
                super(Bullets, self).update(screenWidth, screenHeight)
                super(Bullets, self).update(screenWidth, screenHeight)
        if pygame.sprite.collide_mask(self,map):
            self.velocity = -vx, -vy
            super(Bullets, self).update(screenWidth, screenHeight)
           
        
        