#this class is tankAI, which implement GameObject from the 112 website
#it init the tankAI and allows tanks to move around and shoot bullets 
#tankAI will shoot testbullets which are not drawn to the screen, 
#to test distance and decide next move
import pygame
import math
from GameObject import *
from GameObjects.testbullets import testBullets
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
        TankAI.BS =  pygame.mixer.Sound('music/effects/Bigger Size.wav')
        TankAI.BS.set_volume(1)
    def __init__ (self, x,y,screenWidth, screenHeight,size = 13,angle = 0):
        self.side = 20
        self.sw, self.sh = screenWidth,screenHeight
        self.size = size
        self.w,self.h = int(self.sw//self.size),int(self.sh//self.size)
        self.time = 0
        self.x, self.y = x,y
        self.angleSpeed = 20
        self.angleMargin = 20
        self.velo = 2
        self.igWalls = False
        self.isshooting = False 
        self.tracking = True
        self.sendTime = 0
        #the time bullets are sent
        self.sendDelay =  500
        #wait in 1000 milisenconds avoiding its own bullets
        self.turnedTimes = 0
        self.testDataOrignal = tuple()
        self.testDataNew = tuple()
        self.differTimes = 0
        #how many times data differs
       
        
        #center of the box
        TankAI.image = pygame.transform.smoothscale(TankAI.image, (self.w,self.h))
        self.explo = pygame.transform.smoothscale(TankAI.explo, (self.w,self.h))
        super().__init__(self.x,self.y,TankAI.image,self.side//2,angle)
     
    def trackingMode(self,oppoX,oppoY,screenWidth, screenHeight):
    
        cosAngle =  (self.y- oppoY)/ self.getDistance(self.x,self.y,oppoX,oppoY)
        if oppoX < self.x:
            ang = math.degrees(math.acos(cosAngle))  
        else:
            ang = -1* math.degrees(math.acos(cosAngle))  % 360
        self.adjustAngle(ang-self.angleMargin,ang + self.angleMargin,map)
        self.moveF()
        super(TankAI, self).update(screenWidth, screenHeight)
            
    def update(self,keysDown, screenWidth, screenHeight,map,oppoX,oppoY):
 
        self.time += 1
        #if AI shoot bullets, it need to avoid its own bullets
        if self.isshooting and pygame.time.get_ticks() > self.sendTime + self.sendDelay:
            self.avoidWall(map,False)
            self.isshooting = False 
        if self.isshooting:
            return None
        if self.tracking == True:
            temp = self.tryReachOppoL(map)  
            super(TankAI, self).update(screenWidth, screenHeight)
            if not temp:
                self.tracking = False
        elif self.tracking == False:
            if self.turnedTimes == 0:
            
                self.avoidWall(map)
                self.turnedTimes += 1
                
            elif self.turnedTimes == 1:
                
                if self.testDataOrignal == self.testDataNew:
                  
                    a = self.moveForward(map)
                    super(TankAI, self).update(screenWidth, screenHeight)
                    self.testDataNew = self.sendBullets(map)
                    if a == False:
                        self.turnedTimes = 0
                else:
                 
                    self.differTimes += 1
                    if self.differTimes < 25:
                        a = self.moveForward(map)
                        super(TankAI, self).update(screenWidth, screenHeight)
                        if a == False :
                            self.turnedTimes = 0
                            self.differTimes = 0
                    elif self.differTimes == 25:
                       
                        self.oppoTurnAvoidWall(self.testDataOrignal[0])
                    
                    elif self.differTimes < 45:
                        a = self.moveForward(map)
                        super(TankAI, self).update(screenWidth, screenHeight)
                        if a == False :
                            self.turnedTimes = 0
                            self.differTimes = 0
                    elif self.differTimes == 45:
                        self.trackingMode(oppoX,oppoY,screenWidth, screenHeight)
                        self.differTimes = 0
                        self.tracking = True 
                        self.turnedTimes = 0
       
    
    def avoidWall(self,map,bool = True):
         
        ins1,t1 = self.sendBullets(map)
        self.turnAvoidWall(ins1)
        self.moveF()
        super(TankAI, self).update(self.sw, self.sh)
        if bool:
            ins1,t1 = self.sendBullets(map)
            self.testDataOrignal = ins1,t1
            self.testDataNew = ins1,t1
        
    def oppoTurnAvoidWall(self,ins):
        #turn to the opposite direction as the ins
        
        if ins == "Move Down":
            
            self.angle = 0
        elif ins == "Move Up":
            
            self.angle = 180
        elif ins == "Move Left":
            
            self.angle = 270
        elif ins == "Move Right":
         
            self.angle = 90
        self.moveF()
    def turnAvoidWall(self,ins):
        
        if ins == "Move Down":
            
            self.angle = 180
        elif ins == "Move Up":
            
            self.angle = 0
        elif ins == "Move Left":
            
            self.angle = 90
        elif ins == "Move Right":
         
            self.angle = 270
            
    def sendBullets(self,map):
        #send testing bullets
        self.angle = self.angle % 360
        
        if 45 <= self.angle <= 135 or 225 <= self.angle <= 315:
             
            if 45 <= self.angle <= 135 :
            #tanks if facing left  
                downAngle = self.angle + 90
            elif 225 <= self.angle <= 315:
            #tanks if facing right
                downAngle = self.angle - 90
            
            testDown =  testBullets(self.x, self.y, downAngle ,self.sw,self.sh)
            downTime = 0
            while testDown.y >= self.y and downTime < 1000:
                self.updateTestBullets(testDown,map,self.sw,self.sh)
                downTime += 1
    
            testUp = testBullets(self.x, self.y, downAngle+180 ,self.sw,self.sh)
            upTime = 0
            while testUp.y <= self.y and upTime < 1000:
                self.updateTestBullets(testUp,map,self.sw,self.sh)
                upTime += 1
             
            if downTime > upTime:
                
                return ("Move Down",min(downTime,upTime))
            else:
                return ("Move Up",min(downTime,upTime))
            
        else:
            if 45 > self.angle or self.angle > 315:
            #tank face up
                leftAngle = self.angle + 90
            elif 135 <self.angle  < 225 :
                leftAngle = self.angle - 90
                
            testLeft =  testBullets(self.x, self.y, leftAngle,self.sw,self.sh)
            leftTime = 0
            while testLeft.x <= self.x and leftTime < 1000:
                self.updateTestBullets(testLeft,map,self.sw,self.sh)
                leftTime += 1
    
            testRight = testBullets(self.x, self.y, leftAngle+180,self.sw,self.sh)
            rightTime = 0
            while testRight.x >= self.x and rightTime < 1000:
                self.updateTestBullets(testRight,map,self.sw,self.sh)
                rightTime += 1
             
            if leftTime > rightTime:
                
                return ("Move Left",min(leftTime,rightTime))
            else:
                return ("Move Right",min(leftTime,rightTime))
        
    def updateTestBullets(self,bullet,map,sw,sh):
         
        bullet.collide(map,sw,sh)
        bullet.update(sw,sh,map)
        
        
        
    def tryReachOppoL(self,map):
        #void walking towards walls by turning left
        
        ox, oy = self.x, self.y
        self.moveForward(map)
        if ox == self.x and oy == self.y:
            self.tracking = False
            return False
        return True
    def shootBullets(self,oppo,map):
       
        angle = 0
        while angle <= 360:
        
            if self.sendAdjustOneDirection(angle,map,oppo):
                self.sendTime = pygame.time.get_ticks()
                return True
            angle += 45
            #shoot bullets in 8 directions 
        return False
         
        
        #send bullets and adjust angle in one direction
    def sendAdjustOneDirection(self, angle,map,oppo):
        testDown =  testBullets(self.x, self.y, angle ,self.sw,self.sh)
        downTime = 0
        while testDown.y >= self.y and downTime < 100:
            self.updateTestBullets(testDown,map,self.sw,self.sh)
            downTime += 1
            if downTime > 5 and pygame.sprite.collide_circle(testDown,self):
                return None
            if pygame.sprite.collide_rect(testDown,oppo):
                
                self.angle = angle
                self.moveF()
                self.isshooting = True
                super(TankAI, self).update(self.sw, self.sh)
                return True
        
            
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
        screen.blit(self.explo, (self.x-self.w/2, self.y-self.h/2))
    
  
         
    
    def getDistance(self,x1,y1,x2,y2):
        a = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return a
    
    #power up effects
    def powerups(self):
        num = random.randint(0,11)
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
        else:
            TankAI.BS.play()
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