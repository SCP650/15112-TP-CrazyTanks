# OBJ: TP1
    # Generate a hard coded maze
    # Shoot a bullet and it have it bounce around the maze
    # Two tanks can be controlled 

# MVP

    # Have a randomly maze
    # Powerups 
    # Live Count
    # Simple Computer AI
    # Clean User interface
    
import pygame
  
from pygamegame import PygameGame

class InstructionsScreen():
    
    
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.margin = 20
        self.bgColor = (255, 255, 255)
        self.image = pygame.image.load('images/ins.PNG').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (self.width,self.height//2))
        self.imaRec = self.image.get_rect(center=(self.width/2,self.height/2 + self.margin))
        self.gameMode = "InstructionsScreen"
       
        
        pygame.font.init() 
        self.headFont = pygame.font.SysFont('Comic Sans MS', self.width//12)
        self.startText = self.headFont.render('Crazy Tanks', False, (0, 0, 225))
        self.starRec = self.startText.get_rect(center=(self.width/2,self.margin))
        
        self.textFont = pygame.font.SysFont('Comic Sans MS', self.width//17)
        self.backText = self.textFont.render('← Back', False, (0, 0, 0))
        self.backRec = self.backText.get_rect(center=(self.width/20,self.margin))
       
    def redrawAll(self, screen):
        screen.blit(self.startText, (self.width//4, self.margin) )
        screen.blit(self.backText,(self.backRec))
        screen.blit(self.image,(self.imaRec))
 
    def mousePressed(self, x, y):
        if self.backRec.collidepoint(x,y):
            self.gameMode = "StartScreen"
        
    def keyPressed(self, code, mod):
        if code == pygame.K_ESCAPE:
            self.gameMode = "StartScreen"
            
    def getGameMode(self):
     
        return self.gameMode
        
    def resetGameMode(self):
        self.gameMode =  "InstructionsScreen"
         
    def timerFired(self, dt,isKeyPressed):
        pass