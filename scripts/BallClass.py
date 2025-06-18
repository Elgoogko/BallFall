import pygame
import numpy as np
import os
from tools.formatCLI import *

pygame.font.init()
pygame.mixer.init()


class Ball(pygame.sprite.Sprite):
    font = pygame.font.Font('freesansbold.ttf', 15)

    def __init__(self, initVelocity: list[float], color: pygame.Color, id: int, message: str = '',  displayMessage: bool = False, sound: str = '', soundVolume: float = 0.5, ballSize: list[int] = [15, 10], displayTrail: bool = True, trailLenght: int = 15, image: str = None, DISPLAY: pygame.Surface = None, *groups):
        super().__init__(*groups)
        self.ballSize = [15, 10]
        self.position = (0, 0)
        self.velocity = initVelocity
        self.color = color
        self.lastPos = []
        self.display = DISPLAY
        self.score = 0
        self.message = message
        self.id = id
        self.displayTrail = displayTrail
        self.trailLenght = trailLenght

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

        if (sound == None or sound == ''):
            self.sound = ''
        else:
            if (os.path.exists(sound)):
                self.sound = sound
                self.soundPlayer = pygame.mixer.Sound(self.sound)
                self.soundPlayer.set_volume(self.soundVolume)

            else:
                self.sound = ''
                self.soundPlayer = None
                printWarning(f" sound not found for ball {id} : {sound}")

        if (image == None):
            self.original_image = None
            self.image = None
            self.pathToImage = None
        else:
            if (os.path.exists(image)):
                self.pathToImage = image
                self.image = pygame.image.load(image)
                self.original_image = self.image.copy()
                self.image = pygame.transform.scale(self.image, (ballSize[0], ballSize[0]))

                self.displayMessage = False
            else:
                self.image = None

    def update(self, *args, **kwargs):
        if (self.displayTrail):
            if (len(self.lastPos) == self.trailLenght):
                self.lastPos.pop(0)
            self.lastPos.append(self.position)

            a = 255//len(self.lastPos)

            for i in range(len(self.lastPos)):
                temp_surface = pygame.Surface(
                    (self.ballSize[0] * 2, self.ballSize[0] * 2), pygame.SRCALPHA)

                temp_color = self.color
                temp_color.a = a*i

                pygame.draw.circle(
                    temp_surface, temp_color, (self.ballSize[0], self.ballSize[0]), self.ballSize[0])
                self.display.blit(
                    temp_surface, (self.lastPos[i][0] - self.ballSize[0], self.lastPos[i][1] - self.ballSize[0]))
        
        self.velocity[1] += 0.3  # gravity effect
        self.position = np.add(self.position, self.velocity)
     
        pygame.draw.circle(self.display, (255, 255, 255),
                           self.position, self.ballSize[0])
        pygame.draw.circle(self.display, self.color,
                           self.position, self.ballSize[1])

        if (self.image != None):
            imageRect = self.image.get_rect()
            imageRect.center = self.position
            self.display.blit(self.image, imageRect)
   
        if (self.displayMessage):
            text = Ball.font.render(
                str(self.score), True, (255, 255, 255), self.color)
            textRect = text.get_rect()
            textRect.center = self.position
            self.display.blit(text, textRect)

    def winUpdate(self):
        if self.position[0] != self.display.get_width()//2 or self.position[1] != self.display.get_height()//2:
            self.position = [
                self.position[0] - 1 if self.position[0] > self.display.get_width()//2 else self.position[0] +
                1 if self.position[0] < self.display.get_width(
                )//2 else self.display.get_width()//2,
                self.position[1] - 1 if self.position[1] > self.display.get_height()//2 else self.position[1] +
                1 if self.position[1] < self.display.get_height(
                )//2 else self.display.get_height()//2
            ]

        if (self.ballSize[0] != self.display.get_width()//4):
            self.ballSize = np.add(self.ballSize, 1)

        pygame.draw.circle(self.display, (255, 255, 255),
                           self.position, self.ballSize[0])
        pygame.draw.circle(self.display, self.color,
                           self.position, self.ballSize[1])
      
        if (self.image != None):
            self.image = pygame.transform.scale(self.original_image, (self.ballSize[0], self.ballSize[0]))
            imageRect = self.image.get_rect()
            imageRect.center = self.position
            self.display.blit(self.image, imageRect)

        if (self.displayMessage):
            text = Ball.font.render(
            str(self.score), True, (255, 255, 255), self.color)
            textRect = text.get_rect()
            textRect.center = self.position
            self.display.blit(text, textRect)  

    def setImage(self, image: str):
        self.original_image = None
        if (not os.path.exists(image)):
            printWarning(
                f" image is missing in path : {image}. Verify your path.")
            self.image = None
            self.pathToImage = ''
        else:
            if (not os.path.splitext(image)[1] in ['.png', '.jpg', '.jpeg']):
                raise TypeError(
                    " File is not valid for image. Image must be a .png, .jpg or .jpeg.")
            else:
                self.pathToImage = image
                self.image = pygame.image.load(image)
                self.original_image = self.image.copy()
                self.image = pygame.transform.scale(self.image, (self.ballSize[0], self.ballSize[0]))

    def setSound(self, sound: str):
        if(sound == '' or sound == None):
            self.sound = None
            self.soundPlayer = None
            return
        
        if (not os.path.exists(sound)):
            printWarning(
                f" sound not found at path {sound}. Verify your path.")
            self.sound = None
            self.soundPlayer = None
        else:
            if (not os.path.splitext(sound)[1] in ['.mp3', '.wav']):
                raise TypeError(
                    " File is not valid for sound. Sound must be a .mp3 or .wav.")
            self.sound = sound
            self.soundPlayer = pygame.mixer.Sound(self.sound)
            self.soundPlayer.set_volume(self.soundVolume)

    def playSound(self):
        if (self.sound != ''):
            self.soundPlayer.play()

    def setDisplay(self, display: pygame.Surface):
        self.display = display
        self.position = display.get_rect().center

    def collisionWithHalo(self, Vn: np.ndarray, dist: np.ndarray, HaloRadius: int):

        v = np.array(self.velocity)
        self.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion

        if (np.linalg.norm(self.velocity) <= 3.0):
            self.velocity = np.multiply(self.velocity, 1.5)

        overlap = (np.linalg.norm(dist) + self.ballSize[0]) - HaloRadius
        self.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle

    def ballScore(self, font: pygame.font, textPos: tuple):
        # Render both the score and the message
        score_surface = font.render(
            " " + str(self.score) + " ", True, (255, 255, 255), self.color)
        if (self.message != '' or self.message != None):
            message_surface = font.render(
                "  " + self.message + "  ", True, (255, 255, 255), self.color)

            # Combine both surfaces vertically into one
            width = max(score_surface.get_width(), message_surface.get_width())
            height = score_surface.get_height() + message_surface.get_height()
            combined_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            combined_surface.blit(
                score_surface, ((message_surface.get_width()-score_surface.get_width())//2, 0))
            combined_surface.blit(
                message_surface, (0, score_surface.get_height()))
        else:
            combined_surface = pygame.Surface(
                (score_surface.get_width(), score_surface.get_height()), pygame.SRCALPHA)
            combined_surface.blit(score_surface, (0, 0))

        textRect = combined_surface.get_rect()
        textRect.center = textPos
        self.display.blit(combined_surface, textRect)

    def toStringSelf(self):
        print("\n" + bcolors.BOLD + bcolors.OKCYAN +
              "╔══════════════════════════════════════╗")
        print(f"║           Current Ball {self.id}            ║")
        print("╠══════════════════════════════════════╣")
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
