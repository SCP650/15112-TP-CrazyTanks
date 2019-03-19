'''
GameObject.py

implements the base GameObject class, which defines the wraparound motion
Lukas Peraza, 2015 for 15-112 Pygame Lecture
'''
import pygame
import math
from GameObject import *
import random
# this is the class for AI tanks in singleplayer mode

class TankAI(GameObject):
    @staticmethod
    def init():
        TankAI.image = pygame.image.load('images/tank2.png').convert_alpha()
        TankAI.explo = pygame.image.load("images/expl.png").convert_alpha()
        
        TankAI.FS =  pygame.mixer.Sound('music/effects/Faster Speed.wav')
        TankAI.FS.set_volume(1)
        TankAI.IB =  pygame.mixer.Sound('music/effects/Invincible Bullets.wav')
        TankAI.IB.set_volume(1)
        TankAI.SS =  pygame.mixer.Sound('music/effects/Smaller Size.wav')
        TankAI.SS.set_volume(1)
        
    def __init__ (self, x,y,screenWidth, screenHeight,size = 13):
        self.side = 20
        self.sw, self.sh = screenWidth,screenHeight
        self.size = size
        self.w,self.h = int(self.sw//self.size),int(self.sh//self.size)
        self.time = 0
        self.x, self.y = x,y
        self.angle = 0
        self.angleSpeed = 20
        self.angleMargin = 20
        self.velo = 2
        self.move = True
        self.igWalls = False
      
        #center of the box
        TankAI.image = pygame.transform.smoothscale(TankAI.image, (self.w,self.h))
        TankAI.explo = pygame.transform.smoothscale(TankAI.explo, (self.w,self.h))
        super().__init__(self.x,self.y,TankAI.image,self.side//2)
     
       
    def update(self,keysDown, screenWidth, screenHeight,map,oppoX,oppoY):
        if self.move == False:
            return None 
        self.time += 1
     
        if self.time % 100 == 0: 
         
            cosAngle =  (self.y- oppoY)/ self.getDistance(self.x,self.y,oppoX,oppoY)
            if oppoX < self.x:
                
                ang = math.degrees(math.acos(cosAngle))  
            else:
                ang = -1* math.degrees(math.acos(cosAngle))  % 360
 
            self.adjustAngle(ang-self.angleMargin,ang + self.angleMargin,map)
            
           
        self.tryReachOppoL(map)          
        super(TankAI, self).update(screenWidth, screenHeight)
    
    def getDistance(self,x1,y1,x2,y2):
        a = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return a
 
        
    def tryReachOppoL(self,map):
        #void walking towards walls by turning left
        
        ox, oy = self.x, self.y
        self.moveForward(map)
        if ox == self.x and oy == self.y:
           
            self.moveBackward(map)
            self.moveBackward(map)
       
            self.angle += self.angleSpeed
           
    
   
            
    #turn the tank directly without moving it
    #return True if turned successfully, False otherwise
    def adjustAngle(self,minAngle,maxAngle,map):
        self.angle %= 360 
        times = 0
        while not (self.angle >= minAngle and self.angle <= maxAngle) and times < 20:
            # self.rotateLeft(map)
            self.angle += self.angleSpeed
            self.angle %= 360 
            times += 1
        if times > 20:
            times = 0
            while not (self.angle >= minAngle and self.angle <= maxAngle) and times < 20:
                self.angle += self.angleSpeed
                self.angle %= 360 
                times += 1
        return self.angle >= minAngle and self.angle <= maxAngle 
        
    def moveForward(self,map):
        
        self.moveF()
        super(TankAI, self).update(self.sw, self.sh)
        if pygame.sprite.collide_mask(self,map):
            self.moveB()
            return False 
        return True 
        
    def moveBackward(self,map):
        
        self.moveB()
        super(TankAI, self).update(self.sw, self.sh)
        if pygame.sprite.collide_mask(self,map):
            self.moveF()
            return False 
        return True 
            
    def rotateLeft(self,map):
        self.angle += self.angleSpeed
        super(TankAI, self).update(self.sw, self.sh)
        if pygame.sprite.collide_mask(self,map):
            self.angle -= self.angleSpeed
            self.angle -= self.angleSpeed
            
    def rotateRight(self,map):
        self.angle -= self.angleSpeed
        super(TankAI, self).update(self.sw, self.sh)
        if pygame.sprite.collide_mask(self,map):
            self.angle += self.angleSpeed
            self.angle += self.angleSpeed
   
        
    def moveF(self):
        angle = math.radians(self.angle)
        self.x -= self.velo * math.sin(angle)
        self.y -= self.velo * math.cos(angle)
    def moveB(self):
        angle = math.radians(self.angle)
        self.x += self.velo * math.sin(angle)
        self.y += self.velo * math.cos(angle)
    
     
    def drawExplosion(self,screen):
        self.move = False
        screen.blit(TankAI.explo, (self.x-self.w/2, self.y-self.h/2))
    
    def shootBullets(self,oppoX,oppoY):
         
        if self.getDistance(oppoX,oppoY,self.x,self.y) < 100:
            return True
         
    
    #power up effects
    def powerups(self):
        num = random.randint(0,10)
        if num <= 4:
        #5/11 chance of getting this, etc
            TankAI.FS.play()
            self.addSpeed()
        elif num <= 9:
            TankAI.SS.play()
            self.smallerSize()
        elif num <= 10:
            TankAI.IB.play()
            self.ignoreWalls()
     
    def smallerSize(self):
        self.size *= 1.2
        self.__init__(self.x, self.y,self.sw,self.sh,self.size)
    def addSpeed(self):
        self.velo *= 1.5
    def ignoreWalls(self):
        self.igWalls = True
    def isigWalls(self):
        return self.igWalls