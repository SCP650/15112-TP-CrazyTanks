 
# This is the single player game with AI
#human player can choose wither to use keyboard or mouse to control
 
    
import pygame

from GameObjects.tank import *
from GameObjects.TankAI import *
from GameObjects.tank3 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from GameObjects.Box import Box
import random


class SinglePlayerGame():
    @staticmethod
    def init():
        SinglePlayerGame.tank1Score = 0
        SinglePlayerGame.TankAIScore = 0
        
        SinglePlayerGame.tank1Counts = 0
        SinglePlayerGame.tankAICounts = 0
        
        SinglePlayerGame.isMouse = False
        SinglePlayerGame.isSettingMode = True 
        
        SinglePlayerGame.ExploEffect = pygame.mixer.Sound('music/effects/bomb.wav')
        SinglePlayerGame.ExploEffect.set_volume(1)
        SinglePlayerGame.ShootEffect = pygame.mixer.Sound('music/effects/shoot.wav')
        SinglePlayerGame.ShootEffect.set_volume(0.5)
        
        SinglePlayerGame.winningScore = 10
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.isPaused = False 
        self.gameMode = "SinglePlayerMode"
        self.winner = 0
       
        
        self.bgColor = (255, 255, 255)
        pygame.font.init() 
        self.margin = 20
        self.headFont = pygame.font.SysFont('Comic Sans MS', self.width//12)
        self.overFont = pygame.font.SysFont('Comic Sans MS', 70)
        self.overText = self.overFont.render('Game Is OVER!', False, (0, 50, 0))
        self.textFont = pygame.font.SysFont('Comic Sans MS', width//20)
        self.isOver = False
        self.timeDelay = 0
        
        Map.init()
        self.map = Map(self.width, self.height)
        self.mapGroup = pygame.sprite.GroupSingle(self.map)
         
        Tank.init() 
        TankAI.init() 
        self.tankGroup = pygame.sprite.Group()
        self.AIShoot = False 
        
        if SinglePlayerGame.isSettingMode == False:
            self.initTanks()
            
        self.startText = self.headFont.render('Crazy Tanks', False, (0, 0, 225))
        self.settingText = self.headFont.render('Keyboard Control', False, (0, 225, 0))
        self.settingText2 = self.headFont.render('Mouse Control', False, (225, 0, 0))
        self.settingRect = self.settingText.get_rect(center=((1/2* self.width ,2*self.height/5)))
        self.settingRect2 = self.settingText2.get_rect(center=((1/2*self.width ,3*self.height/5)))
        self.starRec = self.startText.get_rect(center=(self.width/2,self.margin))
        
        #init the powerups
        Box.init()        
        self.boxGroup = pygame.sprite.Group()
    
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        self.tankExplo = False
        self.tankExplo2 = False
        #check if tank is exploding
        self.exploTime = 0
        #the time when a tank explode
        self.exploDelay = 2000
        #show explosion in 2000 milisenconds before going to the next round
    
        
    def redrawAll(self, screen):
        if SinglePlayerGame.isSettingMode:
            screen.blit(self.startText, (self.width//4, self.margin) )
            screen.blit(self.settingText,self.settingRect)
            screen.blit(self.settingText2, self.settingRect2)
            return None
            
        self.mapGroup.draw(screen)
        self.boxGroup.draw(screen)
        
        self.tankGroup.draw(screen)
        self.bullets.draw(screen)
        self.bullets2.draw(screen)
        if self.tankExplo:
            tank = self.tank1
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
 
        if self.tankExplo2:
            tank = self.TankAI
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
            
        #check if any tank won
        if SinglePlayerGame.tank1Score >= SinglePlayerGame.winningScore:
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player1 Won!', False, (0, 225, 0))
            screen.blit(line2,(self.width//3, self.height//3))
            self.winner = 1
            if self.timeDelay % 300 == 0:
                self.gameMode = "RankScreen"
        elif SinglePlayerGame.TankAIScore >= SinglePlayerGame.winningScore:
            self.isOver = True
            screen.blit(self.overText,(self.width//3, self.height//4))
            line2 = self.overFont.render('PlayerAI Won!', False, (0, 0, 225))
            screen.blit(line2,(self.width//4, self.height//3))
            self.winner = -1
            if self.timeDelay % 300 == 0:
                self.gameMode = "RankScreen"
            
        #print the score of each player
        if SinglePlayerGame.isMouse:
            color = (225,0, 0)
        else:
            color = (0, 225, 0)
        tank1Text = self.textFont.render('Player1: '+str(SinglePlayerGame.tank1Score), False, color)
        screen.blit(tank1Text,(1/10 * self.width ,self.height - 1/8*self.height))
        TankAIText = self.textFont.render('Player2: '+ str(SinglePlayerGame.TankAIScore), False, (0, 0, 225))
        screen.blit(TankAIText,(7/10 * self.width ,self.height - 1/8*self.height))
        
    def mousePressed(self,x,y):
        if self.settingRect.collidepoint(x,y) and SinglePlayerGame.isSettingMode:
            SinglePlayerGame.isSettingMode = False
            SinglePlayerGame.isMouse = False
            self.initTanks()
        elif self.settingRect2.collidepoint(x,y) and SinglePlayerGame.isSettingMode:
            SinglePlayerGame.isSettingMode = False
            SinglePlayerGame.isMouse = True
            self.initTanks()
        elif SinglePlayerGame.isSettingMode == False and SinglePlayerGame.isMouse:
            #shoot bullets for mouse control
            tank = self.tank1
            SinglePlayerGame.ShootEffect.play()
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
            SinglePlayerGame.tank1Counts += 1
        
    def initTanks(self):
        #init tanks depending on whether user want mouse control or keyboard control
        #put tank1 and TankAI at random location without coliding with wall or each other
       
        if SinglePlayerGame.isMouse == False:
            isColiding = True
            while isColiding != None:
                x,y = random.randint(1,self.width),random.randint(1,self.height)
                self.tank1 = Tank(x,y,self.width,self.height)
                isColiding = pygame.sprite.collide_mask(self.tank1,self.map)
            self.tankGroup.add(self.tank1)
        else:
            isColiding = True
            while isColiding != None:
                x,y = random.randint(1,self.width),random.randint(1,self.height)
                self.tank1 = Tank3(x,y,self.width,self.height)
                isColiding = pygame.sprite.collide_mask(self.tank1,self.map)
            self.tankGroup.add(self.tank1)
        
        isColiding = True
        while isColiding != None:
            x,y = random.randint(1,self.width),random.randint(1,self.height)
            self.TankAI = TankAI(x,y,self.width,self.height)
            isColiding = pygame.sprite.collide_mask(self.TankAI,self.map) or  pygame.sprite.collide_mask(self.TankAI,self.tank1) 
        self.tankGroup.add(self.TankAI)
        
    def keyPressed(self, code, mod):
        if code == pygame.K_r:
            self.__init__(self.width,self.height)
        if code ==pygame.K_p:
            self.isPaused = not self.isPaused
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
            
        if code == pygame.K_2:
            SinglePlayerGame.winningScore = 2
            
        if self.isOver or self.tankExplo or self.tankExplo2:
            return None
        if code == pygame.K_l and SinglePlayerGame.isMouse == False:            
            tank = self.tank1
            SinglePlayerGame.ShootEffect.play()
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
            SinglePlayerGame.tank1Counts += 1
        
  
    def timerFired(self, dt, isKeyPressed):
        if SinglePlayerGame.isSettingMode == True:
            return
        self.timeDelay += 1
        
            
        #after delay, reset the game for next round
        if (self.tankExplo or self.tankExplo2) and pygame.time.get_ticks() > self.exploTime + self.exploDelay:
            if self.tankExplo:
                self.tankExplo = False
            else:
                self.tankExplo2 = False
            self.__init__(self.width,self.height)
            
        if (self.isPaused or self.isOver or self.tankExplo or self.tankExplo2):
            return None
        if SinglePlayerGame.isMouse and self.timeDelay % 10 == 0:
            x,y =  pygame.mouse.get_pos()
            self.tank1.adjustAngle(x,y,self.map)
        #check whether  AI tank wants to shoot bullets
        if self.timeDelay % 20 == 0:
           
            self.AIShoot = self.TankAI.shootBullets(self.tank1,self.map)
            if self.AIShoot :
                SinglePlayerGame.ShootEffect.play()
                self.bullets2.add(Bullets(self.TankAI.x, self.TankAI.y, self.TankAI.angle,self.TankAI.w,self.TankAI.h))
                self.AIShoot = False
                SinglePlayerGame.tankAICounts += 1
        #move tanks and bullets
        self.tank1.update(isKeyPressed,self.width,self.height,self.map)
        self.TankAI.update(isKeyPressed,self.width,self.height,self.map,\
        self.tank1.x,self.tank1.y)            
        self.bullets.update(self.width, self.height)
        self.bullets2.update(self.width, self.height)
         
        #bouncing effect when hit wall
        if self.tank1.isigWalls() == False:
            for bullet in self.bullets:
                bullet.collide(self.map,self.width, self.height)
        if self.TankAI.isigWalls() == False:
            for bullet in self.bullets2:
                bullet.collide(self.map,self.width, self.height)
        
            
        #every 5 seconds or so there will be a new powerups
        if pygame.time.get_ticks() % 5000 //15 == 0:
            box = Box (0, 0,self.width,self.height)
            box = box.getRanLocation(self.map,self.tank1,self.TankAI)
            self.boxGroup.add(box)
        #check if any tank colide with box(powerups)
        c=pygame.sprite.groupcollide(
            self.boxGroup,self.tankGroup, True, False,
            pygame.sprite.collide_rect)
        if c:
            for aBox in c:
            
                if c[aBox][0] == self.tank1:
                    self.tank1.powerups()
                    aBox.remove(self.boxGroup)
                else:
                    self.TankAI.powerups()
                    aBox.remove(self.boxGroup)
        
        if self.isOver or self.tankExplo or self.tankExplo2:
            return None
        #chekc if bullet1 collide with tanks
        a=pygame.sprite.groupcollide(
            self.bullets,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in a:
            
            if a[bullet][0] == self.tank1:
                self.tankExplo = True
                SinglePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                SinglePlayerGame.TankAIScore += 1
            else:
                self.tankExplo2 = True
                SinglePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                SinglePlayerGame.tank1Score += 1
       
        #check if bullet2 collide with tanks 
        b=pygame.sprite.groupcollide(
            self.bullets2,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in b:
           
            if b[bullet][0] == self.tank1:
                self.tankExplo = True
                SinglePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                SinglePlayerGame.TankAIScore += 1
            else:
                self.tankExplo2 = True
                SinglePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                SinglePlayerGame.tank1Score += 1
                
    def getGameMode(self):
     
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode =  "SinglePlayerMode"
    def getResults(self):
        a = (self.winner,SinglePlayerGame.tank1Counts,SinglePlayerGame.tankAICounts)
        return a