import pygame
import numpy as np

class Ball(pygame.sprite.Sprite):
    def __init__(self, initVelocity : list[float], color : pygame.Color, DISPLAY: pygame.display, *groups):
        super().__init__(*groups)
        self.position = DISPLAY.get_rect().center
        self.velocity = initVelocity
        self.color = color
        self.radius = [15, 10]
        self.lastPos = []
        self.display = DISPLAY
        pygame.draw.circle(DISPLAY, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(DISPLAY, color, self.position, self.radius[1])

    def update(self, *args, **kwargs):
        if(len(self.lastPos) == 15):
            self.lastPos.pop(0)
        self.lastPos.append(self.position)
        
        a = 255//len(self.lastPos)
        for i in range(len(self.lastPos)):
            temp_surface = pygame.Surface((self.radius[0] * 2, self.radius[0] * 2), pygame.SRCALPHA)
            
            temp_color = self.color
            temp_color.a = 150
            
            pygame.draw.circle(temp_surface, temp_color, (self.radius[0], self.radius[0]), self.radius[0])
            self.display.blit(temp_surface, (self.lastPos[i][0] - self.radius[0], self.lastPos[i][1] - self.radius[0]))

        self.velocity[1]+=0.3 #gravity effect
        self.position = np.add(self.position, self.velocity)

        pygame.draw.circle(self.display, (255,255,255), self.position, self.radius[0])
        pygame.draw.circle(self.display, self.color, self.position, self.radius[1])
