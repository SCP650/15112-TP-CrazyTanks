  
# This is the main function of the game it extends the PygameGame class in 112 website
#it will run the game by calling different modes.
 
import pygame

from pygamegame import PygameGame
from StartScreen import StartScreen
from SinglePlayerGame import SinglePlayerGame
from TwoPlayerGame import TwoPlayerGame
from ThreePlayerGame import ThreePlayerGame
from InstructionsScreen import InstructionsScreen
from RankScreen import RankScreen
from EasterMode import EasterMode
import random


class MainGame(PygameGame):
    
    
    def init(self):
        
        self.mode = "StartScreen"
        
        StartScreen.init()
        SinglePlayerGame.init()
        TwoPlayerGame.init()
        ThreePlayerGame.init()
        RankScreen.init()
        EasterMode.init()
        
        self.star = StartScreen(self.width,self.height)
        self.single = SinglePlayerGame(self.width,self.height)
        self.two = TwoPlayerGame(self.width,self.height)
        self.three = ThreePlayerGame(self.width,self.height)
        self.ins = InstructionsScreen(self.width,self.height)
        self.rank = RankScreen(self.width,self.height)
        self.easter = EasterMode(self.width,self.height)
        
        self.results = tuple()
        #the result from a wining game: winner, winner bullets num, winner twobullets num
    def redrawAll(self, screen):
        if self.mode == "StartScreen":
            self.star.redrawAll(screen)
            
        elif self.mode == "SinglePlayerMode":
            self.single.redrawAll(screen)
            
        elif self.mode == "TwoPlayerMode":
            self.two.redrawAll(screen)
        elif self.mode == "ThreePlayerMode":
            self.three.redrawAll(screen)
        elif self.mode == "InstructionsScreen":
            self.ins.redrawAll(screen)
        elif self.mode == "RankScreen":
            self.rank.redrawAll(screen)
        elif self.mode == "EasterMode":
            self.easter.redrawAll(screen)
         
    def mousePressed(self, x, y):
        if self.mode == "StartScreen":
            self.star.mousePressed(x,y)
        elif self.mode == "InstructionsScreen":
            self.ins.mousePressed(x,y)
        elif self.mode == "ThreePlayerMode":
            self.three.mousePressed(x,y)
        elif self.mode == "RankScreen":
            self.rank.mousePressed(x,y)
        elif self.mode == "SinglePlayerMode":
            self.single.mousePressed(x,y)
        elif self.mode == "EasterMode":
            self.easter.mousePressed(x,y)
    def keyPressed(self, code, mod):
        if self.mode == "SinglePlayerMode":
            self.single.keyPressed(code, mod)
        elif self.mode == "StartScreen":
            self.star.keyPressed(code,mod)
            
        elif self.mode == "TwoPlayerMode":
            self.two.keyPressed(code, mod)
        elif self.mode == "ThreePlayerMode":
            self.three.keyPressed(code, mod)
            
        elif self.mode == "InstructionsScreen":
            self.ins.keyPressed(code, mod)
        elif self.mode == "RankScreen":
            self.rank.keyPressed(code, mod)
        elif self.mode == "EasterMode":
            self.easter.keyPressed(code, mod)
    def timerFired(self, dt):
        
        if self.mode == "StartScreen":
            if self.star.getGameMode() != self.mode:
                self.mode = self.star.getGameMode()
                self.star.resetGameMode()
            else:
                if len(self.results) == 0 :
                    self.star.timerFired(dt,self.isKeyPressed)
                else:
                    self.star.timerFired(dt,self.isKeyPressed,self.results)
                
        elif self.mode == "InstructionsScreen":
            self.changeMode(self.ins,dt,self.results)
            
        elif self.mode == "SinglePlayerMode":
            self.changeMode(self.single,dt,self.results)
        elif self.mode == "TwoPlayerMode":
           self.changeMode(self.two,dt,self.results)
        elif self.mode == "ThreePlayerMode":
            self.changeMode(self.three,dt,self.results)
        elif self.mode == "RankScreen":
            self.changeMode(self.rank,dt,self.results)
        elif self.mode == "EasterMode":
            self.changeMode(self.easter,dt,self.results,)
            color = self.easter.getbgColor()
            if color:
                self.bgColor = color
    def changeMode(self,ob,dt,results):
        if ob.getGameMode() != self.mode:
            self.mode = ob.getGameMode()
            ob.resetGameMode()
            if self.mode != "RankScreen":
                self.init()
            else:
                self.results = ob.getResults()
        else:
            if len(results) == 0 :
                ob.timerFired(dt,self.isKeyPressed)
            else:
                ob.timerFired(dt,self.isKeyPressed,results)
                
MainGame(800,800).run()
