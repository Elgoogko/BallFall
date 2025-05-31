import pygame
from pygame.locals import *
import time
import numpy as np

# Game display properties
DISPLAY = pygame.display.set_mode((500, 800))
DISPLAY.fill(pygame.Color(0,0,0))

# Game engine properties
FPS = pygame.time.Clock()
FPS.tick(60)
TOTAL_FRAMES = 60 * 100

class Ball(pygame.sprite.Sprite):
    def __init__(self, initVelocity : list[float], *groups):
        super().__init__(*groups)
        self.position = DISPLAY.get_rect().center
        self.velocity = initVelocity
        self.radius = [25, 20]
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, (255,0,0), self.position, self.radius[1])

    def update(self, *args, **kwargs):
        self.velocity[1]+=0.3
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, (255,0,0), self.position, self.radius[1])

class Halo(pygame.sprite.Sprite):
    def __init__(self, radius : int, speed : int, *groups):
        super().__init__(*groups)
        self.position = [DISPLAY.get_rect().center[0],DISPLAY.get_rect().center[1]] 
        self.radius = radius
        self.speed = speed
        
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius, 3, False, False, False, True)

    def update(self, *args, **kwargs):
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius, 3, False)

ball = Ball([-0.3,0])
halo = Halo(250, 10)

# Lauch pygame app
pygame.init()

while pygame.time.get_ticks() < TOTAL_FRAMES:
    DISPLAY.fill(pygame.Color(0,0,0))
    dist = np.sqrt((ball.position[0] - DISPLAY.get_rect().center[0])**2 + (ball.position[1] - DISPLAY.get_rect().center[1])**2)+ball.radius[0]
    if(dist > halo.radius):
        ball.velocity[1] = -ball.velocity[1]
    ball.update()
    halo.update()
    pygame.time.delay(10)
    pygame.display.update()

pygame.quit()