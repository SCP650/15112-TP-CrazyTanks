#this is the start screen which allows user to choose different game mode
#there will be two tanks shown in the start screen for user to play with
import pygame

from GameObjects.tank import *
from GameObjects.tank2 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from pygamegame import PygameGame
import random
class StartScreen():
    def init():
        StartScreen.tank1Score = 0
        StartScreen.tank2Score = 0
        
        StartScreen.ExploEffect = pygame.mixer.Sound('music/effects/bomb.wav')
        StartScreen.ExploEffect.set_volume(1)
        StartScreen.ShootEffect = pygame.mixer.Sound('music/effects/shoot.wav')
        StartScreen.ShootEffect.set_volume(0.5)
 
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.margin = 20
        self.bgColor = (255, 255, 255)
        self.gameMode = "StartScreen"
        self.isPaused = False 
        self.easterPoint = 0
        
        pygame.font.init() 
     
        pygame.mixer.music.load("music/Good Morning.mp3")
        pygame.mixer.music.set_volume(0.5)
        #【CITATION】 music from Nintendo game MR. Gimmick
        pygame.mixer.music.play(-1)
        
    
        self.headFont = pygame.font.SysFont('Comic Sans MS', self.width//12)
        self.startText = self.headFont.render('Crazy Tanks', False, (0, 0, 225))
        self.starRec = self.startText.get_rect(center=(self.width/2,self.margin))
        
        
        self.textFont = pygame.font.SysFont('Comic Sans MS', self.width//20)
        self.tabText1 = self.textFont.render('Single Player', False, (0, 0, 0))
        self.tabText2 = self.textFont.render('2 Players', False, (0, 0, 0))
        self.tabText3 = self.textFont.render('Instructions', False, (0, 0, 0))
        self.tabText4 = self.textFont.render('3 Players', False, (0, 0, 0))
        
        self.tab1Rec = self.tabText1.get_rect(center=(self.width/2, 2*self.height/6))
        self.tab2Rec = self.tabText2.get_rect(center=(self.width/2, 3*self.height/6))
        self.tab3Rec = self.tabText3.get_rect(center=(self.width/2, 5*self.height/6))
        self.tab4Rec = self.tabText4.get_rect(center=(self.width/2, 4*self.height/6))
        
        #tank stuff
        Tank.init() 
        Tank.init()
        Tank2.init() 
        x,y = random.randint(self.width/10,self.width/5),random.randint(self.height/5,4*self.height/5),
        self.tankGroup = pygame.sprite.Group()
        self.tank1 = Tank(x,y,self.width,self.height,7)
        self.tankGroup.add(self.tank1)
        x,y = random.randint(4*self.width/5, self.width-20 ),random.randint(self.height/5,4*self.height/5),
        self.tank2 = Tank2(x, y,self.width,self.height,7)
        self.tankGroup.add(self.tank2)
        
        
        Map.init(True)
        self.map = Map(self.width, self.height)
        
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
        self.tankGroup.draw(screen)
        self.bullets.draw(screen)
        self.bullets2.draw(screen)
        screen.blit(self.startText, (self.width//4, self.margin) )
        screen.blit(self.tabText1,(self.tab1Rec))
        screen.blit(self.tabText2,(self.tab2Rec))
        screen.blit(self.tabText3,(self.tab3Rec))
        screen.blit(self.tabText4,(self.tab4Rec))
        if self.tankExplo:
            tank = self.tank1
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
 
        if self.tankExplo2:
            tank = self.tank2
            tank.drawExplosion(screen)
            tank.remove(self.tankGroup)
            
    def keyPressed(self, code, mod):
        if code == pygame.K_r:
            self.__init__(self.width,self.height)
        if code ==pygame.K_p:
            self.isPaused = not self.isPaused
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
        if self.tankExplo or self.tankExplo2:
            return None
        
        if code == pygame.K_l:            
            tank = self.tank1
            StartScreen.ShootEffect.play()
            self.bullets.add(Bullets(tank.x, tank.y, tank.angle,tank.w,tank.h))
        if code == pygame.K_SPACE:
            tank2 = self.tank2
            StartScreen.ShootEffect.play()
            self.bullets2.add(Bullets(tank2.x, tank2.y, tank2.angle,tank2.w,tank2.h))
 
    def timerFired(self, dt, isKeyPressed):
        if (self.isPaused):
            return None
     
        if self.easterPoint > 4:
            self.gameMode = "EasterMode"
        #move tanks and bullets
        self.tankGroup.update(isKeyPressed,self.width,self.height,self.map)            
        self.bullets.update(self.width, self.height)
        self.bullets2.update(self.width, self.height)
        
        #after delay, reset the game for next round
        if (self.tankExplo or self.tankExplo2) and pygame.time.get_ticks() > self.exploTime + self.exploDelay:
            if self.tankExplo:
                self.tankExplo = False
            else:
                self.tankExplo2 = False
            self.__init__(self.width,self.height)
        for bullet in self.bullets:
           
            if self.starRec.collidepoint(bullet.x,bullet.y):
                bullet.remove(self.bullets)
                self.easterPoint += 1
        for bullet in self.bullets2:
            if self.starRec.collidepoint(bullet.x,bullet.y):
                bullet.remove(self.bullets2)
                self.easterPoint += 1
        #chekc if bullet1 collide with tanks
        a=pygame.sprite.groupcollide(
            self.bullets,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in a:
            
            if a[bullet][0] == self.tank1:
                self.tankExplo = True
                StartScreen.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                StartScreen.tank2Score += 1
            else:
                self.tankExplo2 = True
                StartScreen.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                StartScreen.tank1Score += 1
       
        #check if bullet2 collide with tanks 
        b=pygame.sprite.groupcollide(
            self.bullets2,self.tankGroup, True, False,
            pygame.sprite.collide_circle)
        for bullet in b:
           
            if b[bullet][0] == self.tank1:
                self.tankExplo = True
                StartScreen.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                StartScreen.tank2Score += 1
            else:
                self.tankExplo2 = True
                StartScreen.ExploEffect.play()
                self.exploTime = pygame.time.get_ticks()
                StartScreen.tank1Score += 1
                
        
    def mousePressed(self, x, y):
        if self.tab1Rec.collidepoint(x,y):
            self.gameMode = "SinglePlayerMode"
        elif self.tab2Rec.collidepoint(x,y):
            self.gameMode = "TwoPlayerMode"
        elif self.tab3Rec.collidepoint(x,y):
            self.gameMode = "InstructionsScreen"
        elif self.tab4Rec.collidepoint(x,y):
            self.gameMode = "ThreePlayerMode"
    def getGameMode(self):
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode = "StartScreen"