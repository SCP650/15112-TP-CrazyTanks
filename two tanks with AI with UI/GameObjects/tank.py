#this class is tank1, which implement GameObject from the 112 website
#it init the tank and allows tanks to move around and shoot bullets 
import pygame
import math
from GameObject import *
import random

class Tank(GameObject):
    @staticmethod
    def init():
        Tank.image = pygame.image.load('images/tank.png').convert_alpha()
        Tank.explo = pygame.image.load("images/expl.png").convert_alpha()
        
        Tank.FS =  pygame.mixer.Sound('music/effects/Faster Speed.wav')
        Tank.FS.set_volume(1)
        Tank.IB =  pygame.mixer.Sound('music/effects/Invincible Bullets.wav')
        Tank.IB.set_volume(1)
        Tank.SS =  pygame.mixer.Sound('music/effects/Smaller Size.wav')
        Tank.SS.set_volume(1)
        Tank.BS =  pygame.mixer.Sound('music/effects/Bigger Size.wav')
        Tank.BS.set_volume(1)
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
        
        Tank.image = pygame.transform.smoothscale(Tank.image, (self.w,self.h))
        self.explo = pygame.transform.smoothscale(Tank.explo, (self.w,self.h))
        super().__init__(self.x,self.y,Tank.image,self.side//2,angle)
        
    def update(self,keysDown, screenWidth, screenHeight,map,isEaster = False):
        if self.move == True:
            if isEaster or keysDown(pygame.K_LEFT):
                #in easter mode, tank will constantly rotate left
                self.angle += self.angleSpeed
                super(Tank, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.angle -= self.angleSpeed
                    self.angle -= self.angleSpeed
            if keysDown(pygame.K_RIGHT):

                self.angle -= self.angleSpeed
                super(Tank, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.angle += self.angleSpeed
                    self.angle += self.angleSpeed
                    
            if keysDown(pygame.K_UP):
                self.moveF()
                super(Tank, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.moveB()
      
            if keysDown(pygame.K_DOWN):
                 
                self.moveB()
                super(Tank, self).update(screenWidth, screenHeight)
                if pygame.sprite.collide_mask(self,map):
                    self.moveF()
                    
                    
            super(Tank, self).update(screenWidth, screenHeight)
        
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
    #4 kinds: more speed, smaller size, bullets that ignore walls and nothing
    
    def powerups(self):
        num = random.randint(0,11)
        if num <= 4:
        #5/11 chance of getting this, etc
            Tank.FS.play()
            self.addSpeed()
        elif num <= 9:
            Tank.SS.play()
            self.smallerSize()
        elif num <= 10:
            Tank.IB.play()
            self.ignoreWalls()
        else:
            Tank.BS.play()
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