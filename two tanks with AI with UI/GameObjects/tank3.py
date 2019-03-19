#this class is tank3, which implement GameObject from the 112 website
#it init the tank3 and allows tanks to move around and shoot bullets 
import pygame
import math
from GameObject import *
import random

class Tank3(GameObject):
    @staticmethod
    def init():
        Tank3.image = pygame.image.load('images/Tank3.png').convert_alpha()
        Tank3.explo = pygame.image.load("images/expl.png").convert_alpha()
        
        Tank3.FS =  pygame.mixer.Sound('music/effects/Faster Speed.wav')
        Tank3.FS.set_volume(1)
        Tank3.IB =  pygame.mixer.Sound('music/effects/Invincible Bullets.wav')
        Tank3.IB.set_volume(1)
        Tank3.SS =  pygame.mixer.Sound('music/effects/Smaller Size.wav')
        Tank3.SS.set_volume(1)
        Tank3.BS =  pygame.mixer.Sound('music/effects/Bigger Size.wav')
        Tank3.BS.set_volume(1)
        #load the three sound effects for powerups 
    def __init__ (self, x,y,screenWidth, screenHeight,size = 13,angle = 0):
        self.side = 20
        self.sw, self.sh = screenWidth,screenHeight
        self.size = size
        self.w,self.h = int(screenWidth//self.size),int(screenHeight//self.size)
        
        self.angleMargin = 10
        self.x, self.y = x,y
        self.angleSpeed = 5
        self.velo = 10
        self.move = True
        self.igWalls = False
        self.time = 0
        #center of the box
        Tank3.image = pygame.transform.smoothscale(Tank3.image, (self.w,self.h))
        self.explo = pygame.transform.smoothscale(Tank3.explo, (self.w,self.h))
        super().__init__(self.x,self.y,Tank3.image,self.side//2,angle)
        
    def update(self,keysDown, screenWidth, screenHeight,map):
        self.time += 1
        if self.move == True and self.time%5==0:
             
             
            self.moveF()
            super(Tank3, self).update(screenWidth, screenHeight)
            if pygame.sprite.collide_mask(self,map):
                self.moveB()
                super(Tank3, self).update(screenWidth, screenHeight)
    def getDistance(self,x1,y1,x2,y2):
        a = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return a
        
    def adjustAngle(self,x,y,map):
        #adjust angle according to mouse location 
        cosAngle =  (self.y- y)/ self.getDistance(self.x,self.y,x,y)
        if x < self.x:
            ang = math.degrees(math.acos(cosAngle))  
        else:
            ang = -1* math.degrees(math.acos(cosAngle))  % 360
        self.angle = ang
        # self.modifyAngle(ang-self.angleMargin,ang + self.angleMargin,map)
        super(Tank3, self).update(self.sw, self.sh)
    
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
            Tank3.FS.play()
            self.addSpeed()
        elif num <= 9:
            Tank3.SS.play()
            self.smallerSize()
        elif num <= 10:
            Tank3.IB.play()
            self.ignoreWalls()
        else:
            Tank3.BS.play()
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