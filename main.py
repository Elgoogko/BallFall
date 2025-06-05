import pygame
from pygame.locals import *
import numpy as np
import time
import math as mt
import random
from BallClass import Ball
from HaloClass import Halo

# Game display properties
DISPLAY = pygame.display.set_mode((500, 800))
DISPLAY.fill(pygame.Color(0,0,0))
end = time.time()+15
visibleHalo = 10
spacingHalo = 10
widthHalo = 5

# Game engine properties
FPS = pygame.time.Clock()
FPS.tick(60)

ball = Ball([-7.5, 0], pygame.Color(255,0,0), DISPLAY)
haloList =[]
r = 0

for i in range(250):
    haloList.append(Halo(150 + r, 1+(r/250), pygame.Color(0, 0, 0)))
    r += spacingHalo

for i in range(visibleHalo+1):
    haloList[i].color = pygame.Color(255,255,255)

downVector = np.array([DISPLAY.get_rect().centerx, int(DISPLAY.get_rect().centery*1.5)])

# Lauch pygame app
pygame.init()

while time.time() < end:
    DISPLAY.fill(pygame.Color(0,0,0))

    if(haloList[0].radius >= 150):
        for halo in haloList:
            halo.radius-= 1
            haloList[visibleHalo-1].speed = haloList[visibleHalo-2].speed + random.uniform(-0.01, 0.01)
    
    for i in range(len(haloList)):
        if(i <= visibleHalo):
            haloList[i].update(True)
        else:
            haloList[i].update(False)

    ball.update()

    # Distance entre centre de la balle et centre du cercle
    dist = np.subtract(ball.position, haloList[0].position)
    Vn = dist / np.linalg.norm(dist)  # vecteur normal unitaire

    # Si la balle dépasse le cercle (en tenant compte de son rayon externe)
    if(np.linalg.norm(dist) + ball.radius[0] >= haloList[0].radius):
        angle = mt.degrees(mt.atan2(-dist[1], dist[0])) % 360
        if(not haloList[0].isInside(angle)):            
            v = np.array(ball.velocity)
            ball.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion
        
            overlap = (np.linalg.norm(dist) + ball.radius[0]) - haloList[0].radius
            ball.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle
        else:
            if(len(haloList) == 1):
                break
            else:
                haloList.pop(0)
                if(len(haloList) >= visibleHalo):
                    haloList[visibleHalo-1].color = pygame.Color(255,255,255)

    FPS.tick(60)
    pygame.display.update()

pygame.quit()
