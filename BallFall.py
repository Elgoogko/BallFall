import pygame
from pygame.locals import *
import numpy as np
import time
import math as mt

# Game display properties
DISPLAY = pygame.display.set_mode((500, 800))
DISPLAY.fill(pygame.Color(0,0,0))

# Game engine properties
FPS = pygame.time.Clock()
FPS.tick(60)
TOTAL_FRAMES = 60 * 100

class Ball(pygame.sprite.Sprite):
    def __init__(self, initVelocity : list[float], color : tuple, *groups):
        super().__init__(*groups)
        self.position = DISPLAY.get_rect().center
        self.velocity = initVelocity
        self.color = color
        self.radius = [20, 15]
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, color, self.position, self.radius[1])

    def update(self, *args, **kwargs):
        self.velocity[1]+=0.3 #gravity effect
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, self.color, self.position, self.radius[1])

class Halo(pygame.sprite.Sprite):
    def __init__(self, radius : int, speed : int, *groups):
        super().__init__(*groups)
        self.position = [DISPLAY.get_rect().center[0],DISPLAY.get_rect().center[1]] 
        self.radius = radius
        self.speed = speed
        self.startAngle = 0
        self.endAngle = 270

    def update(self, *args, **kwargs):
        # Rotate the 3/4 circle (arc) by updating the start angle
        if not hasattr(self, 'angle'):
            self.angle = 0

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
            (255,255,255),
            rect,
            np.deg2rad(self.startAngle),
            np.deg2rad(self.endAngle),
            3
        )

    def isInside(self, angle : float) -> bool:
        if(self.startAngle > self.endAngle):
            return(angle > self.endAngle and angle < self.startAngle)
        else:
            if(angle > self.startAngle and angle < self.endAngle):
                return False        
            else:
                return((angle < self.startAngle and angle >= 0) or (angle > self.endAngle and angle <= 360))


ball = Ball([5, 0], (255,0,0))
haloList = [Halo(150, 3), Halo(180, 2), Halo(210, 1)]

downVector = np.array([DISPLAY.get_rect().centerx, int(DISPLAY.get_rect().centery*1.5)])

# Lauch pygame app
pygame.init()

end = time.time()+15

while time.time() < end:
    DISPLAY.fill(pygame.Color(0,0,0))

    ball.update()

    for halo in haloList:
        halo.update()

    # Distance entre centre de la balle et centre du cercle
    dist = np.subtract(ball.position, haloList[0].position)
    Vn = dist / np.linalg.norm(dist)  # vecteur normal unitaire

    # Si la balle dépasse le cercle (en tenant compte de son rayon externe)
    if(np.linalg.norm(dist) + ball.radius[0] >= haloList[0].radius):
        angle = mt.degrees(mt.atan2(-dist[1], dist[0])) % 360
        if(haloList[0].isInside(angle)):
            if(len(haloList) != 1):
                haloList.pop(0)
            else:
                break
        else:
            v = np.array(ball.velocity)
            ball.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion
        
            overlap = (np.linalg.norm(dist) + ball.radius[0]) - haloList[0].radius
            ball.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle

      
    pygame.draw.line(DISPLAY, (255,0,0), DISPLAY.get_rect().center, ball.position, 3)
    FPS.tick(60)
    pygame.display.update()

pygame.quit()
