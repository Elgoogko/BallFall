import pygame
import numpy as np
import os 
from tools.formatCLI import *

pygame.font.init()
pygame.mixer.init()

class Ball(pygame.sprite.Sprite):
    font = pygame.font.Font('freesansbold.ttf', 15)

    def __init__(self, initVelocity: list[float], color: pygame.Color, id: int, message: str = '',  displayMessage: bool = False, sound: str = '', soundVolume: float = 0.5, ballSize : list[int] =[15, 10], displayTrail: bool = True, trailLenght: int = 15, DISPLAY : pygame.Surface = None,  *groups):
        super().__init__(*groups)

        if (color[0] > 255 or color[1] > 255 or color[2] > 255
           or color[0] < 0 or color[1] < 0 or color[2] < 0):
            raise ValueError("Color invalid")

        if (displayMessage != None):
            self.displayMessage = displayMessage
        else:
            self.displayMessage = False

        if (soundVolume == None):
            self.soundVolume = 0
        elif (soundVolume > 1.0):
            self.soundVolume = 1.0
        elif (soundVolume < 0.0):
            raise ValueError("Sound can't be negative.")
        else:
            self.soundVolume = soundVolume
        
        if(sound == None):
            self.sound = ''
        else:
            if(os.path.exists(sound)):
                self.sound = sound
            else:
                self.sound = ''
                printWarning(f" sound not found for ball {id} : {sound}")
        
        self.position = (0, 0)
        self.velocity = initVelocity
        self.color = color
        self.lastPos = []
        self.display = DISPLAY
        self.score = 0
        self.message = message
        self.id = id
        self.displayTrail = displayTrail
        self.ballSize = [15,10]
        self.trailLenght = trailLenght

    def update(self, *args, **kwargs):
        if (self.displayTrail):
            if (len(self.lastPos) == self.trailLenght):
                self.lastPos.pop(0)
            self.lastPos.append(self.position)

            a = 255//len(self.lastPos)

            for i in range(len(self.lastPos)):
                temp_surface = pygame.Surface((self.ballSize[0] * 2, self.ballSize[0] * 2), pygame.SRCALPHA)

                temp_color = self.color
                temp_color.a = a*i

                pygame.draw.circle(
                    temp_surface, temp_color, (self.ballSize[0], self.ballSize[0]), self.ballSize[0])
                self.display.blit(temp_surface, (self.lastPos[i][0] - self.ballSize[0], self.lastPos[i][1] - self.ballSize[0]))

        self.velocity[1] += 0.3  # gravity effect
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(self.display, (255, 255, 255),
                           self.position, self.ballSize[0])
        pygame.draw.circle(self.display, self.color,
                           self.position, self.ballSize[1])

        if (self.displayMessage):
            text = Ball.font.render(
                str(self.score), True, (255, 255, 255), self.color)
            textRect = text.get_rect()
            textRect.center = self.position
            self.display.blit(text, textRect)

    def playSound(self):
        if (self.sound != ''):
            sound = pygame.mixer.Sound(self.sound)
            sound.set_volume(self.soundVolume)
            sound.play()

    def setDisplay(self, display: pygame.Surface):
        self.display = display
        self.position = display.get_rect().center

    def toStringSelf(self):
        print("\n" + bcolors.BOLD + bcolors.OKCYAN +
               "╔══════════════════════════════════════╗")
        print(f"║        Current Ball {self.id}        ║")
        print( "╠══════════════════════════════════════╣" + bcolors.ENDC)
        print(f"║ Initial Velocity : ({self.velocity[0]},{self.velocity[1]})")
        print(f"║ Color : ({self.color[0]},{self.color[1]},{self.color[2]})")
        print(f"║ Message : {self.message}")
        print(f"║ Display Message on Ball :  {self.displayMessage}")
        print(f"║ Sound Name : {self.sound}")
        print(f"║ Sound Volume : {100*self.soundVolume}%")
        print("╠══════════════════════════════════════╣")
        print(f"║ Ball Size : {self.ballSize}")
        print(f"║ Display Trail : {self.displayTrail}")
        print(f"║ Trail lenght : {self.trailLenght}")
        print("╚══════════════════════════════════════╝" + bcolors.ENDC)
    
    def toString(self):
        return f"Initial Velocity=({self.velocity[0]},{self.velocity[1]})"+", "+f"Color=({self.color[0]},{self.color[1]},{self.color[2]})"
