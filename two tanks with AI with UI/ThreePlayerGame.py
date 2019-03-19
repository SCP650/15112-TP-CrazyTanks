# This is the Three player game
#third player can use mouse to control
import pygame

from GameObjects.tank import *
from GameObjects.tank2 import *
from GameObjects.tank3 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from GameObjects.Box import Box
import random


class ThreePlayerGame():
    @staticmethod
    def init():
        ThreePlayerGame.tank1Score = 0
        ThreePlayerGame.tank2Score = 0
        ThreePlayerGame.tank3Score = 0
        
        ThreePlayerGame.tank1Counts = 0
        ThreePlayerGame.tank2Counts = 0
        ThreePlayerGame.tank3Counts = 0
        
        ThreePlayerGame.ExploEffect = pygame.mixer.Sound('music/effects/bomb.wav')
        ThreePlayerGame.ExploEffect.set_volume(1)
        ThreePlayerGame.ShootEffect = pygame.mixer.Sound('music/effects/shoot.wav')
        ThreePlayerGame.ShootEffect.set_volume(0.5)
        
        ThreePlayerGame.winningScore = 10
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.isPaused = False 
        self.gameMode = "ThreePlayerMode"
        self.winner = 0
        
        self.bgColor = (255, 255, 255)
        pygame.font.init() 
        self.overFont = pygame.font.SysFont('Comic Sans MS', 70)
        self.overText = self.overFont.render('Game Is OVER!', False, (0, 50, 0))
        self.textFont = pygame.font.SysFont('Comic Sans MS', width//20)
        self.isOver = False
       
        
        Map.init()
        self.map = Map(self.width, self.height)
        self.mapGroup = pygame.sprite.GroupSingle(self.map)
        
        Tank.init() 
        Tank2.init() 
        Tank3.init() 
        self.tankGroup = pygame.sprite.Group()
  
        #put tank1,tank2 and tank3 at random location without coliding with wall or each other
        isColiding = True
        while isColiding != None:
            x,y = random.randint(1,self.width),random.randint(1,self.height)
            self.tank1 = Tank(x,y,self.width,self.height)
            isColiding = pygame.sprite.collide_mask(self.tank1,self.map)
        self.tankGroup.add(self.tank1)
        
        isColiding = True
        while isColiding != None:
            x,y = random.randint(1,self.width),random.randint(1,self.height)
            self.tank2 = Tank2(x,y,self.width,self.height)
            isColiding = pygame.sprite.collide_mask(self.tank2,self.map) or  pygame.sprite.collide_mask(self.tank2,self.tank1) 
        self.tankGroup.add(self.tank2)
        
        isColiding = True
        while isColiding != None:
            x,y = random.randint(1,self.width),random.randint(1,self.height)
            self.tank3 = Tank3(x,y,self.width,self.height)
            isColiding = pygame.sprite.collide_mask(self.tank3,self.map) or  pygame.sprite.collide_mask(self.tank3,self.tank1)  or pygame.sprite.collide_mask(self.tank3,self.tank2) 
        self.tankGroup.add(self.tank3)
        
        #init the powerups
        Box.init()        
        self.boxGroup = pygame.sprite.Group()
    
        self.bullets = pygame.sprite.Group()
        self.bullets2 = pygame.sprite.Group()
        self.bullets3 = pygame.sprite.Group()
        self.tankExplo = False
        self.tankExplo2 = False
        self.tankExplo3 = False
        #check if tank is exploding
        self.exploTime = 0
        #the time when a tank explode
        self.exploDelay = 2000
        #show explosion in 2000 milisenconds before going to the next round
    
        self.time = 0
    def redrawAll(self, screen):
        self.mapGroup.draw(screen)
        self.boxGroup.draw(screen)
        self.tankGroup.draw(screen)
        self.bullets.draw(screen)
        self.bullets2.draw(screen)
        self.bullets3.draw(screen)
        if self.tankExplo:
            tank = self.tank1
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
 
        if self.tankExplo2:
            tank = self.tank2
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
        
        if self.tankExplo3:
            tank = self.tank3
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
            
            
        #check if any tank won
        if ThreePlayerGame.tank1Score >= ThreePlayerGame.winningScore:
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player1 Won!', False, (0, 225, 0))
            screen.blit(line2,(self.width//3, self.height//3))
            self.winner = 1
            if self.time % 300 == 0:
                self.gameMode = "RankScreen"
        elif ThreePlayerGame.tank2Score >= ThreePlayerGame.winningScore:
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player2 Won!', False, (0, 0,225))
            screen.blit(line2,(self.width//4, self.height//3))
            self.winner = 2
            if self.time % 300 == 0:
                self.gameMode = "RankScreen"
        elif ThreePlayerGame.tank3Score >= ThreePlayerGame.winningScore:
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player3 Won!', False, (225, 0, 0))
            screen.blit(line2,(self.width//4, self.height//3))
            self.winner = 3
            if self.time % 300 == 0:
                self.gameMode = "RankScreen"
        #print the score of each player
        tank1Text = self.textFont.render('Player1: '+str(ThreePlayerGame.tank1Score), False, (0, 225, 0))
        screen.blit(tank1Text,(1/10 * self.width ,self.height - 1/8*self.height))
        tank2Text = self.textFont.render('Player2: '+ str(ThreePlayerGame.tank2Score), False, (0, 0, 225))
        screen.blit(tank2Text,(4/10 * self.width ,self.height - 1/8*self.height))
        tank3Text = self.textFont.render('Player3: '+ str(ThreePlayerGame.tank3Score), False, (225, 0, 0))
        screen.blit(tank3Text,(7/10 * self.width ,self.height - 1/8*self.height))

         
    def mousePressed(self,x,y):
        tank = self.tank3
        ThreePlayerGame.ShootEffect.play()
        self.bullets3.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
        ThreePlayerGame.tank3Counts += 1
        
    def keyPressed(self, code, mod):
        if code == pygame.K_r:
            self.__init__(self.width,self.height)
        if code ==pygame.K_p:
            self.isPaused = not self.isPaused
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
        if self.isOver or self.tankExplo or self.tankExplo2:
            return None
        if code == pygame.K_2:
            ThreePlayerGame.winningScore = 2
            
        if code == pygame.K_l:            
            tank = self.tank1
            ThreePlayerGame.ShootEffect.play()
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
            ThreePlayerGame.tank1Counts += 1
        if code == pygame.K_SPACE:
            tank2 = self.tank2
            ThreePlayerGame.ShootEffect.play()
            self.bullets2.add(Bullets(tank2.x, tank2.y, tank2.angle,tank2.w,tank2.h))
            ThreePlayerGame.tank2Counts += 1
        
  
    def timerFired(self, dt, isKeyPressed):
        self.time += 1
        if (self.isPaused):
            return None
     
        
        #after delay, reset the game for next round
        if (self.tankExplo or self.tankExplo2 or self.tankExplo3 ) and pygame.time.get_ticks() > self.exploTime + self.exploDelay:
            if self.tankExplo:
                self.tankExplo = False
            elif self.tankExplo2:
                self.tankExplo2 = False
            elif self.tankExplo3:
                self.tankExplo3 = False
            self.__init__(self.width,self.height)
            
        if (self.isPaused or self.isOver or self.tankExplo or self.tankExplo2 or self.tankExplo3):
            return None
            
        if self.time % 10 == 0 :
            x,y =  pygame.mouse.get_pos()
            self.tank3.adjustAngle(x,y,self.map)
            
        #move tanks and bullets
        self.tankGroup.update(isKeyPressed,self.width,self.height,self.map)            
        self.bullets.update(self.width, self.height)
        self.bullets2.update(self.width, self.height)
        self.bullets3.update(self.width, self.height)
        #bouncing effect when hit wall
        if self.tank1.isigWalls() == False:
            for bullet in self.bullets:
                bullet.collide(self.map,self.width, self.height)
        if self.tank2.isigWalls() == False:
            for bullet in self.bullets2:
                bullet.collide(self.map,self.width, self.height)
        if self.tank3.isigWalls() == False:
            for bullet in self.bullets3:
                bullet.collide(self.map,self.width, self.height)
                
        
            
        #every 5 seconds or so there will be a new powerups
        if pygame.time.get_ticks() % 5000 //15 == 0:
            box = Box (0, 0,self.width,self.height)
            box = box.getRanLocation(self.map,self.tank1,self.tank2)
            self.boxGroup.add(box)
        #check if any tank colide with box(powerups)
        c=pygame.sprite.groupcollide(
            self.boxGroup,self.tankGroup, True, False,
            pygame.sprite.collide_rect)
        if c:
            for aBox in c:
            
                if  self.tank1 in c[aBox]:
                    self.tank1.powerups()
                    aBox.remove(self.boxGroup)
                if self.tank2 in c[aBox] :
                    self.tank2.powerups()
                    aBox.remove(self.boxGroup)
                if self.tank3 in c[aBox] :
                    self.tank3.powerups()
                    aBox.remove(self.boxGroup)
        if self.isOver or self.tankExplo or self.tankExplo2:
            return None
        #chekc if bullet1 collide with tanks
        a=pygame.sprite.groupcollide(
            self.bullets,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in a:
            
            if self.tank1 in a[bullet] :
                self.tankExplo = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank2Score += 1
                ThreePlayerGame.tank3Score += 1
            if self.tank2 in a[bullet] :
                self.tankExplo2 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank1Score += 1
                
            if self.tank3 in a[bullet] :
                self.tankExplo3 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank1Score += 1
                
        #check if bullet2 collide with tanks 
        b=pygame.sprite.groupcollide(
            self.bullets2,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in b:
           
            if self.tank1 in b[bullet] :
                self.tankExplo = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank2Score += 1
            if self.tank2 in b[bullet] :
                self.tankExplo2 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank1Score += 1
                ThreePlayerGame.tank3Score += 1
            if self.tank3 in b[bullet] :
                self.tankExplo3 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank2Score += 1
        #check if bullet3 collide with tanks 
        c =pygame.sprite.groupcollide(
            self.bullets3,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in c:
           
            if self.tank1 in c[bullet] :
                self.tankExplo = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank3Score += 1
            if self.tank3 in c[bullet] :
                self.tankExplo3 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank1Score += 1
                ThreePlayerGame.tank2Score += 1
            if self.tank2 in c[bullet] :
                self.tankExplo2 = True
                ThreePlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                ThreePlayerGame.tank3Score += 1
                
                
    def getGameMode(self):
     
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode =  "ThreePlayerMode"
    def getResults(self):
        a = (self.winner,ThreePlayerGame.tank1Counts,ThreePlayerGame.tank2Counts,ThreePlayerGame.tank3Counts )
        return a