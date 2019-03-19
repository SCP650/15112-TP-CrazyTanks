# This class is the easter mode. 
#It will be triggered when palyer shoot the title "crazy tank" 5 times
#every 100 points the background color will change to a random color
#every 1000 points the size of the tank will be bigger 
#and bullets will be shot at a faster frquency, making the game more difficult

# Is user press "esc" during game, they can keep the background color
# if user died during the game, the background color will be set to white
#user can also see the ranking of all other players
    
import pygame

from GameObjects.tank import *
from GameObjects.tank2 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from pygamegame import PygameGame
import random
class EasterMode():
    def init():
        EasterMode.ExploEffect = pygame.mixer.Sound('music/effects/bomb.wav')
        EasterMode.ExploEffect.set_volume(1)
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.margin = 20
        self.bgColor = (255, 0, 255)
        self.gameMode = "EasterMode"
        self.isPaused = False 
        self.timeDelay = 0
        pygame.font.init() 
        self.textFont = pygame.font.SysFont('Comic Sans MS', width//20)
        self.isInvs = False
        # the tank is not invinsible 
        self.headFont = pygame.font.SysFont('Comic Sans MS', self.width//12)
        self.startText = self.headFont.render('Hello Gunter!', False, (0, 0, 205))
        self.starRec = self.startText.get_rect(center=(self.width/2,self.margin))
        self.bulletInterval = 30
        # the time interval between one bullets and another
        
            
        #tank stuff
        Tank.init() 
        Tank.init()
        Tank2.init() 
        x,y = random.randint(10,self.width-10),random.randint(10,self.height-10),
        self.tankGroup = pygame.sprite.Group()
        self.tank1 = Tank(x,y,self.width,self.height)
        
        x,y = random.randint(self.width/5, self.width ),random.randint(self.height/5,4*self.height/5),
        self.tank2 = Tank2(x, y,self.width,self.height,15)
        self.tankGroup.add(self.tank2)
        
        
        Map.init(True)
        self.map = Map(self.width, self.height)
        
        self.bullets = pygame.sprite.Group()
       
     
        self.tankExplo2 = False
        #check if tank is exploding
        self.exploTime = 0
        #the time when a tank explode
        self.exploDelay = 2000
        #show explosion in 2000 milisenconds before going to the next round
    def getbgColor(self):
        if self.tankExplo2:
            return (255,255,255)
        if self.timeDelay > 200 and self.timeDelay % 100 == 0:
            a,b,c =random.randint(100,255),random.randint(100,255),random.randint(100,255)
            return (a,b,c)
        return None
    def redrawAll(self, screen):
        self.tankGroup.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.startText, (self.width//4, self.margin) )
        
         
        if self.tankExplo2:
            tank = self.tank2
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
            screen.blit(self.tank2Text,self.tank2Rect)
        else:
            tank1Text = self.textFont.render('Score: '+str(self.timeDelay-1), False, (200, 200, 200))
            screen.blit(tank1Text,(5/8 * self.width ,self.height - 1/8*self.height))
            
    def keyPressed(self, code, mod):
        if code == pygame.K_r:
            self.__init__(self.width,self.height)
        if code ==pygame.K_p:
            self.isPaused = not self.isPaused
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
        if  self.tankExplo2:
            return None
    
        if code == pygame.K_1:
            self.timeDelay += 1000
            if self.bulletInterval > 10:
                self.bulletInterval = 10
            if self.bulletInterval-2 != 0:
                self.bulletInterval -= 2
            self.tank2.biggerSize()
        if code == pygame.K_i:
            self.isInvs = not self.isInvs
    def timerFired(self, dt, isKeyPressed):
        if (self.isPaused):
            return None
        
        #after delay, reset the game for next round
        if  self.tankExplo2 and pygame.time.get_ticks() > self.exploTime + self.exploDelay:
            self.tankExplo2 = False
            self.gameMode = "RankScreen"
        if self.tankExplo2:
            return None
        
        self.timeDelay += 1
        if self.timeDelay == 10:
            pygame.mixer.music.load("music/8Bit Are Scary.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
        if self.timeDelay  == 280:
            self.bulletInterval = 10
            #sudden increas in bullets initially to match to bgm
        elif self.timeDelay % 1000 == 0 and self.bulletInterval-2 != 0:
            self.bulletInterval -= 2
            self.tank2.biggerSize()
        if self.timeDelay % self.bulletInterval == 0:
            tank = self.tank1
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
      
            
        #move tanks and bullets
        self.tank1.update(isKeyPressed,self.width,self.height,self.map,True)
        self.tankGroup.update(isKeyPressed,self.width,self.height,self.map)            
        self.bullets.update(self.width, self.height)
        
        
        
        if self.isInvs:
            return None 
        #chekc if bullet1 collide with tanks
        a=pygame.sprite.groupcollide(
            self.bullets,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in a:
            
            if a[bullet][0] == self.tank1:
                pass
            else:
                self.tankExplo2 = True
                EasterMode.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                self.tank2Text = self.headFont.render('You got '+str(self.timeDelay)+" points!", False, (0, 0, 0))
                self.tank2Rect = self.tank2Text.get_rect(center=(self.width/2,self.height/2))
       
        
    def mousePressed(self, x, y):
        pass
    def getGameMode(self):
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode = "EasterMode"
    def getResults(self):
        a = (1,self.timeDelay,None,True)
        return a