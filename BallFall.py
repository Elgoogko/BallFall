import pygame
from pygame.locals import *
import numpy as np
import time
import math as mt

# Game display properties
DISPLAY = pygame.display.set_mode((500, 800))
DISPLAY.fill(pygame.Color(0,0,0))
numberHaloVisible = 13

# Game engine properties
FPS = pygame.time.Clock()
FPS.tick(60)
speedFactor = 75
end = time.time()+15
haloSpacing = 8
haloWidth = 5
haloHoleAngle = 90

class Ball(pygame.sprite.Sprite):
    def __init__(self, initVelocity : list[float], color : pygame.Color, *groups):
        super().__init__(*groups)
        self.position = DISPLAY.get_rect().center
        self.velocity = initVelocity
        self.score = 0
        self.color = color
        self.radius = [15, 13]
        self.lastPos = []
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, color, self.position, self.radius[1])

    def update(self, *args, **kwargs):
        if(len(self.lastPos) == 10):
            self.lastPos.pop(0)
        self.lastPos.append(self.position)

        a = 255//len(self.lastPos)
        for i in range(len(self.lastPos)):
            temp_surface = pygame.Surface((self.radius[0]*2, self.radius[0]*2), pygame.SRCALPHA)
            temp_color = self.color
            temp_color.a = a*i 
            
            pygame.draw.circle(temp_surface, self.color, (self.radius[0],self.radius[0]), self.radius[0])
    
            # Blitter la surface temporaire sur la surface principale avec transparence
            DISPLAY.blit(temp_surface, (self.lastPos[i][0] - self.radius[0], self.lastPos[i][1] - self.radius[0]))

        self.velocity[1]+=0.3 #gravity effect
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, self.color, self.position, self.radius[1])

class Halo(pygame.sprite.Sprite):
    def __init__(self, radius : int, speed : int, color : pygame.Color, *groups):
        super().__init__(*groups)
        self.position = [DISPLAY.get_rect().center[0],DISPLAY.get_rect().center[1]] 
        self.radius = radius
        self.speed = speed
        self.startAngle = 0
        self.endAngle = 360-haloHoleAngle
        self.color = color

    def update(self, *args, **kwargs):
        # Draw a 3/4 arc (270 degrees) that rotates
        rect = pygame.Rect(
            self.position[0] - self.radius,
            self.position[1] - self.radius,
            self.radius * 2,
            self.radius * 2
        )

        self.startAngle = (self.startAngle+self.speed) % 360
        self.endAngle = (self.endAngle+self.speed) % 360

        pygame.draw.arc(
            DISPLAY,
            self.color,
            rect,
            np.deg2rad(self.startAngle),
            np.deg2rad(self.endAngle),
            haloWidth
        )

    def isInside(self, angle : float) -> bool:
        if(self.startAngle > self.endAngle):
            return(angle > self.endAngle and angle < self.startAngle)
        else:
            if(angle > self.startAngle and angle < self.endAngle):
                return False        
            else:
                return((angle < self.startAngle and angle >= 0) or (angle > self.endAngle and angle <= 360))


Redball = Ball([-5, 0], pygame.Color(255,0,0,0))
Greenball = Ball([-5, 0], pygame.Color(0,255,0,0))
haloList=[]
r = 0

for i in range(100):
    haloList.append(Halo(150+r, (i/speedFactor), pygame.Color(0,0,0)))
    r+=haloSpacing

for i in range(numberHaloVisible):
    haloList[i].color = pygame.Color(255,255,255)

downVector = np.array([DISPLAY.get_rect().centerx, int(DISPLAY.get_rect().centery*1.5)])

# Lauch pygame app
pygame.init()

while time.time() < end:
    DISPLAY.fill(pygame.Color(0,0,0))

    if(not (haloList[0].radius < 150)):
        for halo in haloList:
            halo.radius = halo.radius-2

    for halo in haloList:
        halo.update()

    Redball.update()


    # Distance entre centre de la balle et centre du cercle
    dist = np.subtract(Redball.position, haloList[0].position)
    Vn = dist / np.linalg.norm(dist)  # vecteur normal unitaire

    # Si la balle dépasse le cercle (en tenant compte de son rayon externe)
    if(np.linalg.norm(dist) + Redball.radius[0] >= haloList[0].radius):
        angle = mt.degrees(mt.atan2(-dist[1], dist[0])) % 360
        if(haloList[0].isInside(angle)):
            if(len(haloList) != 1):
                haloList.pop(0)
                if(len(haloList) >= numberHaloVisible):
                    haloList[numberHaloVisible-1].color = (255,255,255)
            else:
                break
        else:
            v = np.array(Redball.velocity)
            Redball.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion
        
            overlap = (np.linalg.norm(dist) + Redball.radius[0]) - haloList[0].radius
            Redball.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle

    FPS.tick(60)
    pygame.display.update()

pygame.quit()
