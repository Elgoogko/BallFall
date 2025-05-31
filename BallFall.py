import pygame
from pygame.locals import *
import time
import math

# Game display properties
DISPLAY = pygame.display.set_mode((500, 800))

# Game engine properties
FPS = pygame.time.Clock()
FPS.tick(60)

# Lauch pygame app
pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.radius = 25
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(self.image, (255,255,255), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (255,0,0), (self.radius, self.radius), self.radius-5)
        self.rect = self.image.get_rect()
        self.velocity = 1
        surface_rect = DISPLAY.get_rect()
        self.rect.center = surface_rect.center
        DISPLAY.blit(self.image, self.rect)


    def update(self, *args, **kwargs):
         self.rect.y += self.velocity
         if self.rect.bottom > DISPLAY.get_height():
             self.rect.bottom = DISPLAY.get_height()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class halo(pygame.sprite.Sprite):
    def __init__(self, radius, speed, *groups):
        super().__init__(*groups)
        self.radius = radius
        self.speed = speed
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        pygame.draw.arc(self.image, (255,255,255), rect, 0, math.radians(180), 5)
        self.rect = self.image.get_rect()
        surface_rect = DISPLAY.get_rect()
        self.rect.center = surface_rect.center
        DISPLAY.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        self.image = pygame.transform.rotate(self.image, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

ball = Ball()
halo1 = halo(100, 0)

while True:
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break
        if(pressed_keys[K_KP_ENTER]):
            ball = Ball()
            print("ball Spawn")

    DISPLAY.fill(pygame.Color(0,0,0))

    ball.update()
    #halo1.update()

    ball.draw(DISPLAY)
    halo1.draw(DISPLAY)
    
    pygame.display.update()