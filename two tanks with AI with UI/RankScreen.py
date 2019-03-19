# This class is called at the end of the game when one reach more than 10 points
#It allows winner to input his or her name, and present the top 10 scores 
import pygame

from GameObjects.tank import *
from GameObjects.tank2 import *
from GameObjects.bullets import*
from GameObjects.Map import Map
from pygamegame import PygameGame
import random
class RankScreen():
    def init():
        RankScreen.tank1Score = 0
        RankScreen.tank2Score = 0
      
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.margin = 20
        self.bgColor = (255, 255, 255)
        self.gameMode = "RankScreen"
        self.isPaused = False 
        self.isAI = False
        self.resultMode = False 
        self.pastScores = []
        self.rank = 0
        self.isEaster = False
        #is it is in easter egg mode
        
        self.winner = 0
        self.scores = list()
        self.name = ""
        self.num = 0
        
        pygame.font.init() 
      
        self.headFont = pygame.font.SysFont('Comic Sans MS', self.width//12)
        self.startText = self.headFont.render('Crazy Tanks', False, (0, 0, 225))
        self.starRec = self.startText.get_rect(center=(self.width/2,self.margin))
        self.textFont = pygame.font.SysFont('Comic Sans MS', self.width//20)
        self.backText = self.textFont.render('← Back', False, (0, 0, 0))
        self.backRec = self.backText.get_rect(center=(self.width/20,self.margin))
        
    def redrawAll(self, screen):
       
        screen.blit(self.startText, self.starRec)
     
        screen.blit(self.backText,(self.backRec))
        
        
        if self.resultMode == False:
            if len(self.scores) == 0:
                return None
            if self.winner == -1:
                self.name = "AI"
                self.isAI = True
                self.num = self.scores[2]
            elif self.name == "":
                self.name = self.winner
                self.num = self.scores[self.winner]
            if self.isEaster:
                self.s = " Points"
                #if in easter mode, don't say won
                won = " finished the game"
            else:
                self.s = " Bullets"
                won = " won!!"
            self.tabText1 = self.textFont.render('Player '+ str(self.name)+won, False, (0, 0, 0))
            self.tab1Rec = self.tabText1.get_rect(center=(self.width/2,2*self.height/9))
            self.tabText2 = self.textFont.render("With "+str(self.num)+self.s, False, (0, 0, 0))
            self.tab2Rec = self.tabText2.get_rect(center=(self.width/2,3*self.height/9))
            if self.isAI == False:
                self.tabText3 = self.textFont.render("Please enter your name with keyboard", False, (0, 0, 0))
                self.tab3Rec = self.tabText3.get_rect(center=(self.width/2,4.5*self.height/9))
                screen.blit(self.tabText3,(self.tab3Rec))
                
            self.endText = self.headFont.render('View Results', False, (0, 0, 100))
            self.endRec = self.endText.get_rect(center=(self.width/2,7*self.height/9 ))
                
            screen.blit(self.endText,self.endRec)
            screen.blit(self.tabText1,(self.tab1Rec))
            screen.blit(self.tabText2,(self.tab2Rec))
            
            
        elif self.resultMode:
            for i in range(len(self.pastScores)):
                tabText0 = self.textFont.render("No."+str(i+1)+"    "+ str(self.pastScores[i][0]), False, (0, 0, 0))         
                tabText00 = self.textFont.render(str(self.pastScores[i][1])+self.s,False,(0, 0, 0) )
                screen.blit(tabText00,(3*self.width/5, (i+1)*40+self.height/5 - self.margin) )
                screen.blit(tabText0,(self.width/4, (i+1)*40+self.height/5 - self.margin) )
            screen.blit(self.rankText,(self.rankRect))
            
    def keyPressed(self, code, mod):
        
        letter = chr(code)
      
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
            
        
                
        if letter.isalpha() and self.isAI == False:
            if isinstance(self.name,int):
                self.name = letter
            else:
                self.name += letter
           
        if code ==pygame.K_BACKSPACE and self.isAI == False and isinstance(self.name,str):
            self.name = self.name[:-1]
            
            
        
    def timerFired(self, dt, isKeyPressed,results):
        
        if (self.isPaused):
            return None
        if results[-1] == True:
            self.isEaster = results[3]
        else:
            self.isEaster = False 
        self.scores = results 
        self.winner = results[0]
        
            
            
                
    def mousePressed(self, x, y):
        if self.backRec.collidepoint(x,y):
            self.gameMode = "StartScreen"
        if self.endRec.collidepoint(x,y) and self.resultMode == False:
            self.resultMode = True
            if self.getResults():
                self.rankText = self.headFont.render(str(self.name)+" ranked No." + str(self.rank)+" !!", False, (0, 0, 0))
               
            else:
                self.rankText = self.headFont.render("Nice Try", False, (0, 0, 0))
            self.rankRect = self.rankText.get_rect(center=(self.width/2,6*self.height/7))
        
          
    def getResults(self):
        if self.isEaster == False:
            filePath = "pastScores.txt"
        else:
            filePath = "easterScores.txt"
            
        with open(filePath,"rt") as f: 
        #CITATION the "with" statement is from 112 course website
            for line in f.read().split("/n"):
                one = line.split(",")
                self.pastScores.append(one)
        self.pastScores.pop()
       
        if self.pastScores == []:
            self.pastScores.insert(0, [self.name,self.num])
            self.rank =  1
            
            self.writeFiles()
            return True
        for i in range(len(self.pastScores)):
            if self.isEaster == False:
                if self.num < int(self.pastScores[i][1]):
                    self.pastScores.insert(i, [self.name,self.num])
                    self.rank = i + 1
                    self.pastScores.pop()
                    self.writeFiles()
                    return True
            else:
                if self.num > int(self.pastScores[i][1]):
                    self.pastScores.insert(i, [self.name,self.num])
                    self.rank = i + 1
                    self.pastScores.pop()
                    self.writeFiles()
                    return True
        return False
    
            
            
    def writeFiles(self):
        if self.isEaster == False:
            filePath = "pastScores.txt"
        else:
            filePath = "easterScores.txt"
        contents = ""
        for i in range(len(self.pastScores)):
            contents += str(self.pastScores[i][0]) + ","+ str(self.pastScores[i][1])+ "/n"
        
        with open(filePath, "wt") as f:
            #CITATION the "with" statement is from 112 course website
            f.write(contents)
    
    def getGameMode(self):
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode = "RankScreen"