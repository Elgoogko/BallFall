import pygame
import numpy as np
from formatCLI import * 

pygame.font.init()
pygame.mixer.init()

class Ball(pygame.sprite.Sprite):
    radius = [15, 10]
    font = pygame.font.Font('freesansbold.ttf', 15)

    def __init__(self, initVelocity : list[float], color : pygame.Color, id : int, message = '',  displayMessage = False, sound = '', soundVolume = 0.5, *groups):
        super().__init__(*groups)

        if(color[0]>255 or color[1]>255 or color[2]>255
           or color[0]<0 or color[1]<0 or color[2]<0):
            raise ValueError("Color invalid")

        if(displayMessage != None):
            self.displayMessage = displayMessage
        else: 
            self.displayMessage = ''

        if(soundVolume == None):
            self.soundVolume = 0
        elif(soundVolume > 1.0):
            self.soundVolume = 1.0
        elif(soundVolume < 0.0):
            raise ValueError("Sound can't be negative.")
        else:
            self.soundVolume
      
        self.position = (0,0)
        self.velocity = initVelocity
        self.color = color
        self.lastPos = []
        self.display = None
        self.score = 0  
        self.message = message
        self.sound = sound
        self.id = id

    def update(self, *args, **kwargs):
        if(len(self.lastPos) == 15):
            self.lastPos.pop(0)
        self.lastPos.append(self.position)
        
        a = 255//len(self.lastPos)
        for i in range(len(self.lastPos)):
            temp_surface = pygame.Surface((self.radius[0] * 2, Ball.radius[0] * 2), pygame.SRCALPHA)
            
            temp_color = self.color
            temp_color.a = 150
            
            pygame.draw.circle(temp_surface, temp_color, (Ball.radius[0], Ball.radius[0]), Ball.radius[0])
            self.display.blit(temp_surface, (self.lastPos[i][0] - Ball.radius[0], self.lastPos[i][1] - Ball.radius[0]))

        self.velocity[1]+=0.3 #gravity effect
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(self.display, (255,255,255), self.position, Ball.radius[0])
        pygame.draw.circle(self.display, self.color, self.position, self.radius[1])

        if(self.displayMessage):
            text = Ball.font.render(str(self.score), True, (255,255,255), self.color)
            textRect = text.get_rect()
            textRect.center = self.position
            self.display.blit(text, textRect)
    
    def playSound(self):
        if(self.sound != ''):
            sound = pygame.mixer.Sound(self.sound)
            sound.set_volume(self.soundVolume)
            sound.play()
    
    def setDisplay(self, display : pygame.display):
        self.display = display
        self.position = display.get_rect().center

    def toStringSelf(self):
        print(bcolors.BOLD+"_"*25+f"Ball {self.id}"+"_"*25+bcolors.ENDC)
        print(f"Initial Velocity : ({self.velocity[0]},{self.velocity[1]})")
        print(f"Color : ({self.color[0]},{self.color[1]},{self.color[2]})")
        print(f"Message : {self.message}")
        print(f"Display Message on Ball :  {self.displayMessage}")
        print(f"Sound Name : {self.sound}")
        print(f"Sound Volume : {100*self.soundVolume}%")
        print(bcolors.BOLD+"_"*60+bcolors.ENDC)

    def toString(self):
        return f"Initial Velocity=({self.velocity[0]},{self.velocity[1]})"+", "+f"Color=({self.color[0]},{self.color[1]},{self.color[2]})"
