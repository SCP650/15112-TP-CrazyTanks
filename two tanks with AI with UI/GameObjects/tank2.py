#this class is tank2, which implement GameObject from the 112 website
#it init the tank2 and allows tanks to move around and shoot bullets 

import pygame
import math
from GameObject import *
import random

class Tank2(GameObject):
    @staticmethod
    def init():
        Tank2.image = pygame.image.load('images/tank2.png').convert_alpha()
        Tank2.explo = pygame.image.load("images/expl.png").convert_alpha()
        
        Tank2.FS =  pygame.mixer.Sound('music/effects/Faster Speed.wav')
        Tank2.FS.set_volume(1)
        Tank2.IB =  pygame.mixer.Sound('music/effects/Invincible Bullets.wav')
        Tank2.IB.set_volume(1)
        Tank2.SS =  pygame.mixer.Sound('music/effects/Smaller Size.wav')
        Tank2.SS.set_volume(1)
        Tank2.BS =  pygame.mixer.Sound('music/effects/Bigger Size.wav')
        Tank2.BS.set_volume(1)
        #load the three sound effects for powerups 
    def __init__ (self, x,y,screenWidth, screenHeight,size = 13,angle = 0):
        self.side = 20
        self.sw, self.sh = screenWidth,screenHeight
        self.size = size
        self.w,self.h = int(screenWidth//self.size),int(screenHeight//self.size)
        
        self.x, self.y = x,y
        self.angleSpeed = 5
        self.velo = 10
        self.move = True
        self.igWalls = False
        #center of the box
        Tank2.image = pygame.transform.smoothscale(Tank2.image, (self.w,self.h))
        self.explo = pygame.transform.smoothscale(Tank2.explo, (self.w,self.h))
        super().__init__(self.x,self.y,Tank2.image,self.side//2,angle)
        
    def update(self,keysDown, screenWidth, screenHeight,map):
        if self.move == True:
            if keysDown(pygame.K_a):
                self.angle += self.angleSpeed
                super(Tank2, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.angle -= self.angleSpeed
                    self.angle -= self.angleSpeed
            if keysDown(pygame.K_d):
                # not elif! if we're holding left and right, don't turn
                self.angle -= self.angleSpeed
                super(Tank2, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.angle += self.angleSpeed
                    self.angle += self.angleSpeed
            if keysDown(pygame.K_w):
                self.moveF()
                super(Tank2, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.moveB()
      
                
            if keysDown(pygame.K_s):
                 
                self.moveB()
                super(Tank2, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.moveF()
                    
                    
            super(Tank2, self).update(screenWidth, screenHeight)
        
    def drawExplosion(self,screen):
        self.move = False
        screen.blit(self.explo, (self.x-self.w/2, self.y-self.h/2))
        
    def moveF(self):
        angle = math.radians(self.angle)
        self.x -= self.velo * math.sin(angle)
        self.y -= self.velo * math.cos(angle)
    def moveB(self):
        angle = math.radians(self.angle)
        self.x += self.velo * math.sin(angle)
        self.y += self.velo * math.cos(angle)
    
    #power up effects
    def powerups(self):
        num = random.randint(0,11)
        if num <= 4:
        #5/11 chance of getting this, etc
            Tank2.FS.play()
            self.addSpeed()
        elif num <= 9:
            Tank2.SS.play()
            self.smallerSize()
        elif num <= 10:
            Tank2.IB.play()
            self.ignoreWalls()
        else:
            Tank2.BS.play()
            self.biggerSize()
    def biggerSize(self):
        self.size *= 0.9
        self.__init__(self.x, self.y,self.sw,self.sh,self.size,self.angle)
    def smallerSize(self):
        self.size *= 1.2
        self.__init__(self.x, self.y,self.sw,self.sh,self.size,self.angle)
    def addSpeed(self):
        self.velo *= 1.5
    def ignoreWalls(self):
        self.igWalls = True
    def isigWalls(self):
        return self.igWalls