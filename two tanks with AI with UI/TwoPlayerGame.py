# This is the two player game


import pygame

from GameObjects.tank import *
from GameObjects.tank2 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from GameObjects.Box import Box
import random


class TwoPlayerGame():
    @staticmethod
    def init():
        TwoPlayerGame.tank1Score = 0
        TwoPlayerGame.tank1Counts = 0
        TwoPlayerGame.tank2Score = 0
        TwoPlayerGame.tank2Counts = 0
        
        TwoPlayerGame.ExploEffect = pygame.mixer.Sound('music/effects/bomb.wav')
        TwoPlayerGame.ExploEffect.set_volume(1)
        TwoPlayerGame.ShootEffect = pygame.mixer.Sound('music/effects/shoot.wav')
        TwoPlayerGame.ShootEffect.set_volume(0.5)
        TwoPlayerGame.winningScore = 10
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.isPaused = False 
        self.gameMode = "TwoPlayerMode"
         
        
        self.bgColor = (255, 255, 255)
        pygame.font.init() 
        self.overFont = pygame.font.SysFont('Comic Sans MS', 70)
        self.overText = self.overFont.render('Game Is OVER!', False, (0, 50, 0))
        self.textFont = pygame.font.SysFont('Comic Sans MS', width//20)
        self.isOver = False
        self.time = 0
        self.winner = 0
       
        
        Map.init()
        self.map = Map(self.width, self.height)
        self.mapGroup = pygame.sprite.GroupSingle(self.map)
        
        Tank.init() 
        Tank2.init() 
        self.tankGroup = pygame.sprite.Group()
  
        #put tank1 and tank2 at random location without coliding with wall or each other
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
        self.mapGroup.draw(screen)
        self.boxGroup.draw(screen)
        
        self.tankGroup.draw(screen)
        #check if any tank won
        if self.tankExplo:
            tank = self.tank1
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
 
        if self.tankExplo2:
            tank = self.tank2
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
        
        
        self.bullets.draw(screen)
        self.bullets2.draw(screen)
            
        if TwoPlayerGame.tank1Score >= TwoPlayerGame.winningScore :
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player1 Won!', False, (0, 225, 0))
            screen.blit(line2,(self.width//3, self.height//3))
            self.winner = 1
            if self.time % 300 == 0:
                self.gameMode = "RankScreen"
        elif TwoPlayerGame.tank2Score >= TwoPlayerGame.winningScore :
            self.isOver = True
            screen.blit(self.overText,(self.width//4, self.height//4))
            line2 = self.overFont.render('Player2 Won!', False, (0, 0, 225))
            screen.blit(line2,(self.width//4, self.height//3))
            self.winner = 2
            if self.time % 300 == 0:
                self.gameMode = "RankScreen"
            
        #print the score of each player
        tank1Text = self.textFont.render('Player1: '+str(TwoPlayerGame.tank1Score), False, (0, 225, 0))
        screen.blit(tank1Text,(1/10 * self.width  ,self.height - 1/8*self.height))
        tank2Text = self.textFont.render('Player2: '+ str(TwoPlayerGame.tank2Score), False, (0, 0, 225))
        screen.blit(tank2Text,(7/10 * self.width  ,self.height - 1/8*self.height))
 
         
        
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
            TwoPlayerGame.winningScore = 2
            
        if code == pygame.K_l:            
            tank = self.tank1
            TwoPlayerGame.ShootEffect.play()
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
            TwoPlayerGame.tank1Counts += 1
        if code == pygame.K_SPACE:
            tank2 = self.tank2
            TwoPlayerGame.ShootEffect.play()
            self.bullets2.add(Bullets(tank2.x, tank2.y, tank2.angle,tank2.w,tank2.h))
            TwoPlayerGame.tank2Counts += 1
  
    def timerFired(self, dt, isKeyPressed):
        self.time += 1
        #after delay, reset the game for next round
        if (self.tankExplo or self.tankExplo2) and pygame.time.get_ticks() > self.exploTime + self.exploDelay:
            if self.tankExplo:
                self.tankExplo = False
            else:
                self.tankExplo2 = False
            self.__init__(self.width,self.height)
            
        if (self.isPaused or self.isOver or self.tankExplo or self.tankExplo2):
            return None
     
        
        #move tanks and bullets
        self.tankGroup.update(isKeyPressed,self.width,self.height,self.map)            
        self.bullets.update(self.width, self.height)
        self.bullets2.update(self.width, self.height)

        #bouncing effect when hit wall
        if self.tank1.isigWalls() == False:
            for bullet in self.bullets:
                bullet.collide(self.map,self.width, self.height)
        if self.tank2.isigWalls() == False:
            for bullet in self.bullets2:
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
            
                if c[aBox][0] == self.tank1:
                    self.tank1.powerups()
                    aBox.remove(self.boxGroup)
                else:
                    self.tank2.powerups()
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
                TwoPlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                TwoPlayerGame.tank2Score += 1
            else:
                self.tankExplo2 = True
                TwoPlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                TwoPlayerGame.tank1Score += 1
       
        #check if bullet2 collide with tanks 
        b=pygame.sprite.groupcollide(
            self.bullets2,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in b:
           
            if b[bullet][0] == self.tank1:
                self.tankExplo = True
                TwoPlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                TwoPlayerGame.tank2Score += 1
            else:
                self.tankExplo2 = True
                TwoPlayerGame.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                TwoPlayerGame.tank1Score += 1
        
    def getGameMode(self):
     
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode =  "TwoPlayerMode"
    def getResults(self):
        a = (self.winner,TwoPlayerGame.tank1Counts,TwoPlayerGame.tank2Counts)
        return a