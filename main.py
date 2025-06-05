import pygame
from pygame.locals import *
import numpy as np
import time
import math as mt
import random
from BallClass import Ball
from HaloClass import Halo
from formatCLI import * 

class gameProperties():
    def __init__(self):
        self.screenSize = None
        self.backgroundColor = None
        self.time = None
        self.spacingHalo = None
        self.widthHalo = None
        self.ballList = []

    def toString(self):
        props = [
        ("Screen Size", self.screenSize),
        ("Background Color", self.backgroundColor),
        ("Time", self.time),
        ("Spacing Halo", self.spacingHalo),
        ("Width Halo", self.widthHalo)
    ]

        max_len = max(len(name) for name, _ in props)
        header = f"{bcolors.BOLD}{bcolors.OKCYAN}┌{'─'*30} Game Properties {'─'*30}┐{bcolors.ENDC}"
        footer = f"{bcolors.BOLD}{bcolors.OKCYAN}└{'─'*75}┘{bcolors.ENDC}"
        lines = [header]

        for i, (label, value) in enumerate(props):
            label_fmt = f"{label:<{max_len}}"
            if i < len(self.ballList):
                ball = self.ballList[i].toString()
                lines.append(f"{bcolors.OKCYAN}│ {bcolors.ENDC}{label_fmt} : {bcolors.OKGREEN}{value}{bcolors.ENDC} │ Ball {i}: {bcolors.WARNING}{ball}{bcolors.ENDC}")
            else:
                lines.append(f"{bcolors.OKCYAN}│ {bcolors.ENDC}{label_fmt} : {bcolors.OKGREEN}{value}{bcolors.ENDC}")

        # Afficher les balles restantes si plus que les propriétés
        if len(self.ballList) > len(props):
            for i in range(len(props), len(self.ballList)):
                ball = self.ballList[i].toString()
                lines.append(f"{bcolors.OKCYAN}│ {' '*max_len}   {bcolors.ENDC}│ Ball {i}: {bcolors.WARNING}{ball}{bcolors.ENDC}")

        lines.append(footer)
        print("\n".join(lines))
        
class mainGame():

    DISPLAY = None
    visibleHalo = 10
    spacingHalo = 10
    widthHalo = 5
    end = 0
    ballList = []
    font = None
    
    def __init__(self):
        # Game display properties
        DISPLAY = pygame.display.set_mode((500, 800))
        DISPLAY.fill(pygame.Color(0, 0, 0))
        end = time.time() + 15
        pygame.font.init()
        font = pygame.font.Font('freesansbold.ttf', 32)

        # ball and Halo initialisation
        ballList = [
        Ball([-7.5, 0], pygame.Color(255, 0, 0), DISPLAY, '', False, './sounds/No.mp3', 3),
        Ball([-7.0, 0], pygame.Color(0, 255, 0), DISPLAY, '', False, './sounds/Yes.mp3', 0.4)
        ]

    @staticmethod
    def startGame():
        # Game engine properties
        FPS = pygame.time.Clock()
        FPS.tick(60)

        haloList = []
        r = 0

        for i in range(250):
            haloList.append(
                Halo(150 + r, 1 + (r / 250), pygame.Color(0, 0, 0), mainGame.widthHalo, mainGame.DISPLAY)
            )
            r += mainGame.spacingHalo

        for i in range(mainGame.visibleHalo + 1):
            haloList[i].color = pygame.Color(255, 255, 255)

        # misc
        textPos = [(150, 50), (350, 50)]
        # Lauch pygame app
        pygame.init()

        while time.time() < mainGame.end:
            mainGame.DISPLAY.fill(pygame.Color(0, 0, 0))

            if haloList[0].radius >= 150:
                for halo in haloList:
                    halo.radius -= 1
                    haloList[mainGame.visibleHalo - 1].speed = (
                        haloList[mainGame.visibleHalo - 2].speed + random.uniform(-0.01, 0.01)
                    )

            for i in range(len(haloList)):
                if i <= mainGame.visibleHalo:
                    haloList[i].update(True)
                else:
                    haloList[i].update(False)

            for i in range(len(mainGame.ballList)):
                ball = mainGame.ballList[i]
                ball.update()

                # Distance entre centre de la balle et centre du cercle
                dist = np.subtract(ball.position, haloList[0].position)
                Vn = dist / np.linalg.norm(dist)  # vecteur normal unitaire

                # Si la balle dépasse le cercle (en tenant compte de son rayon externe)
                if np.linalg.norm(dist) + ball.radius[0] >= haloList[0].radius:
                    angle = mt.degrees(mt.atan2(-dist[1], dist[0])) % 360
                    if not haloList[0].isInside(angle):
                        v = np.array(ball.velocity)
                        ball.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion

                        overlap = (np.linalg.norm(dist) + ball.radius[0]) - haloList[0].radius
                        ball.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle
                    else:
                        if len(haloList) == 1:
                            break
                        else:
                            ball.score += 1
                            haloList.pop(0)
                            if ball.sound is not None:
                                ball.playSound()

                            if len(haloList) >= mainGame.visibleHalo:
                                haloList[mainGame.visibleHalo - 1].color = pygame.Color(255, 255, 255)

                text = mainGame.font.render(str(ball.score), True, (0, 0, 0), (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = textPos[i]
                mainGame.DISPLAY.blit(text, textRect)

            FPS.tick(60)
            pygame.display.update()

        pygame.quit()