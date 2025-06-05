import pygame
import numpy as np
class Halo(pygame.sprite.Sprite):
    def __init__(self, radius : int, speed : int, color : pygame.Color, widhtHalo : int, DISPLAY : pygame.display, *groups):
        super().__init__(*groups)
        self.position = [DISPLAY.get_rect().center[0],DISPLAY.get_rect().center[1]] 
        self.radius = radius
        self.speed = speed
        self.startAngle =80
        self.endAngle = 350
        self.color = color
        self.width = widhtHalo
        self.display = DISPLAY

    def update(self, display : bool, *args, **kwargs):
        # Rotate the 3/4 circle (arc) by updating the start angle
        if not hasattr(self, 'angle'):
            self.angle = 0
        
        self.startAngle = (self.startAngle+self.speed) % 360
        self.endAngle = (self.endAngle+self.speed) % 360

        if(display):
            # Draw a 3/4 arc (270 degrees) that rotates
            rect = pygame.Rect(
            self.position[0] - self.radius,
            self.position[1] - self.radius,
            self.radius * 2,
            self.radius * 2
        )

            pygame.draw.arc(
            self.display,
            self.color,
            rect,
            np.deg2rad(self.startAngle),
            np.deg2rad(self.endAngle),
            self.width
        )

    def isInside(self, angle : float) -> bool:
        if(self.startAngle > self.endAngle):
            return(angle > self.endAngle and angle < self.startAngle)
        else:
            if(angle > self.startAngle and angle < self.endAngle):
                return False        
            else:
                return((angle < self.startAngle and angle >= 0) or (angle > self.endAngle and angle <= 360))
