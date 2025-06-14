import pygame
from pygame.locals import *
import numpy as np
import time
import math as mt
import random
from BallClass import Ball
from HaloClass import Halo
from tools.formatCLI import * 
from MusicClass import *

class gameProperties():
    def __init__(self):
        self.screenSize = [500,800]
        self.backgroundColor = (0,0,0)
        self.time = 15
        self.spacingHalo = 10
        self.widthHalo = 3
        self.ballList = []
        self.displayScore = True
        self.message = None
        self.minRadius = 150
        self.scoreMultiplier = 1
        self.ballSize = [15,10]
        self.displayTrails = True
        self.trailsLenght = 15
        self.midiFile = None
        self.haloColor = pygame.Color(255,255,255)

    def modifyAllBalls(self, param : str):
        """
        Modifies a specified attribute for all balls in the ballList.

        Args:
            param (str): The name of the attribute to modify. 
                Supported values are 'ballSize', 'displayTrail', and 'trailLenght'.

        Note:
            - If 'param' does not match any of the supported values, no changes are made.
            - 'trailLenght' appears to be a typo; consider renaming to 'trailLength' for consistency.
        """
        match param:
            case 'ballSize':
                for ball in self.ballList:
                    ball.ballSize = self.ballSize
            case 'displayTrail':
                for ball in self.ballList:
                    ball.displayTrail = self.displayTrails
            case 'trailLenght':
                for ball in self.ballList:
                    ball.trailLenght = self.trailsLenght
            
    def toString(self):
        props = [
        ("Message / Title", self.message),
        ("Song", self.midiFile),
        ("Screen Size", self.screenSize),
        ("Background Color", self.backgroundColor),
        ("Time", self.time),
        ("Spacing Halo", self.spacingHalo),
        ("Width Halo", self.widthHalo),
        ("Display Score", self.displayScore)
    ]

        max_len = max(len(name) for name, _ in props)
        header = f"{bcolors.BOLD}{bcolors.OKCYAN}┌{'─'*33} Game Properties {'─'*33}┐{bcolors.ENDC}"
        footer = f"{bcolors.BOLD}{bcolors.OKCYAN}└{'─'*84}┘{bcolors.ENDC}"
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
    
    def toStringAdvanced(self):
        props = [
        ("Message / Title", self.message),
        ("Song", self.midiFile),
        ("Screen Size", self.screenSize),
        ("Background Color", self.backgroundColor),
        ("Time", self.time),
        ("Spacing Halo", self.spacingHalo),
        ("Width Halo", self.widthHalo),
        ("Display Score", self.displayScore),
        (bcolors.WARNING+bcolors.BOLD+"Advanced Parameters"+bcolors.ENDC, None),
        ("Minimum Radius", self.minRadius),
        ("Score multiplier", self.scoreMultiplier),
        ("Ball Size", self.ballSize),
        ("Display Trails", self.displayTrails),
        ("Trails Lenght", self.trailsLenght),
        ("Halos Color", self.haloColor)
    ]

        max_len = max(len(name) for name, _ in props)
        header = f"{bcolors.BOLD}{bcolors.OKCYAN}┌{'─'*33} Game Properties {'─'*33}┐{bcolors.ENDC}"
        footer = f"{bcolors.BOLD}{bcolors.OKCYAN}└{'─'*84}┘{bcolors.ENDC}"
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
    pygame.mixer.init()
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    visibleHalo = 10
    
    #screenSize : tuple, backgroundColor : tuple, spaceHalo : int, widhtHalo : int, displayTime : int, ballList : list[Ball], displayScore : bool, message : str, minRadius : int, scoreMultiplier : int, midiFile : str
    def __init__(self, gameProperties : gameProperties):
        self.DISPLAY = pygame.display.set_mode(gameProperties.screenSize)
        self.DISPLAY.fill(gameProperties.backgroundColor)
        self.spacingHalo = gameProperties.spacingHalo
        self.widthHalo = gameProperties.widthHalo
        self.time = gameProperties.time
        self.displayScore = gameProperties.displayScore
        self.message = gameProperties.message
        self.scoreMultiplier = gameProperties.scoreMultiplier
        self.minRadius = gameProperties.minRadius
        self.musicController = musicController(gameProperties.midiFile)
        self.backgroundColor = gameProperties.backgroundColor

        if(gameProperties.ballList == []):
            self.ballList =  [
            Ball([-5, 0], pygame.Color(255, 0, 0), 0, '', False, './sounds/No.mp3', 1.0, [15,0], True, 15, self.DISPLAY),
            Ball([-7.0, 0], pygame.Color(0, 255, 0), 1, '', False, './sounds/Yes.mp3', 0.4, [15,0], True, 15,self.DISPLAY)
        ]
        else:
            for ball in gameProperties.ballList:
                ball.display = self.DISPLAY
            self.ballList = gameProperties.ballList
        
        self.startGame()

    def startGame(self):
        # Lauch pygame app
        pygame.init()

        # Game engine properties
        FPS = pygame.time.Clock()
        FPS.tick(60)

        # halo generation
        haloList = []
        r = 0
        
        for i in range(250):
            haloList.append(
                Halo(self.minRadius + r, 1 + (r / 250), self.backgroundColor, self.widthHalo, self.DISPLAY))
            r += self.spacingHalo

        for i in range(mainGame.visibleHalo + 1):
            haloList[i].color = pygame.Color(255, 255, 255)

        flag = True
        while flag:
            self.DISPLAY.fill(self.backgroundColor)
            text = mainGame.font.render("Press SPACE BAR to start", True, (0,0,0), (255,255,255))
            textRect = text.get_rect()
            textRect.center = self.DISPLAY.get_rect().center
            self.DISPLAY.blit(text, textRect)
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        flag = False
        
        # text placement
        temp = self.DISPLAY.get_width()//(len(self.ballList)+1)
        textPos = []
        for i in range(len(self.ballList)):
            textPos.append([temp*(i+1),150])
        
        
        n = 0 # note to play
        end = time.time() + self.time
        self.musicController.startTime = time.time()
        while time.time() < end:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            
            self.DISPLAY.fill(self.backgroundColor)

            if haloList[0].radius >= self.minRadius:
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

            for i in range(len(self.ballList)):
                ball = self.ballList[i]
                ball.update()

                # Distance entre centre de la balle et centre du cercle
                dist = np.subtract(ball.position, haloList[0].position)
                Vn = dist / np.linalg.norm(dist)  # vecteur normal unitaire

                # Si la balle dépasse le cercle (en tenant compte de son rayon externe)
                if np.linalg.norm(dist) + ball.ballSize[0] >= haloList[0].radius:

                    angle = mt.degrees(mt.atan2(-dist[1], dist[0])) % 360
                    if not haloList[0].isInside(angle):
                        self.musicController.playNote(n)
                        n+=1

                        v = np.array(ball.velocity)
                        ball.velocity = v - 2 * np.dot(v, Vn) * Vn  # réflexion

                        if(np.linalg.norm(ball.velocity) <=3.0):
                            ball.velocity = np.multiply(ball.velocity, 1.5)

                        overlap = (np.linalg.norm(dist) + ball.ballSize[0]) - haloList[0].radius
                        ball.position -= Vn * overlap  # on pousse la balle juste à l'intérieur du cercle
                    else:
                        if len(haloList) == 1:
                            break
                        else:
                            ball.score += self.scoreMultiplier
                            haloList.pop(0)
                            haloList.append(Halo(r+self.spacingHalo,1 + (r+self.spacingHalo / 250),pygame.Color(255,255,255),self.widthHalo, self.DISPLAY))
                            
                            if ball.sound is not None:
                                ball.playSound()

                            if len(haloList) >= mainGame.visibleHalo:
                                haloList[mainGame.visibleHalo - 1].color = pygame.Color(255, 255, 255)

                if(self.displayScore):
                    # Render both the score and the message
                    score_surface = mainGame.font.render(" " + str(ball.score) + " ", True, (255, 255, 255), ball.color)
                    if(ball.message != '' or ball.message != None):
                        message_surface = mainGame.font.render("  " + ball.message + "  ", True, (255, 255, 255), ball.color)

                        # Combine both surfaces vertically into one
                        width = max(score_surface.get_width(), message_surface.get_width())
                        height = score_surface.get_height() + message_surface.get_height()
                        combined_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        combined_surface.blit(score_surface, ((message_surface.get_width()-score_surface.get_width())//2, 0))
                        combined_surface.blit(message_surface, (0, score_surface.get_height()))
                    else:
                        combined_surface = pygame.Surface((score_surface.get_width(), score_surface.get_height()), pygame.SRCALPHA)
                        combined_surface.blit(score_surface, (0,0))

                    textRect = combined_surface.get_rect()
                    textRect.center = textPos[i]
                    self.DISPLAY.blit(combined_surface, textRect)
            
            if(self.message != None):
                text = mainGame.font.render(self.message, True, (0, 0, 0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = (self.DISPLAY.get_width()//2, 50)
                self.DISPLAY.blit(text, textRect)

            FPS.tick(60)
            pygame.display.update()
        
        winnerBall = self.ballList[0]
        for Ball in self.ballList:
            if Ball.score > winnerBall.score:
                winnerBall = Ball
        
        while time.time() < end + 10:
            self.DISPLAY.fill(self.backgroundColor)

            if(self.message != None):
                text = mainGame.font.render(self.message, True, (0, 0, 0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = (self.DISPLAY.get_width()//2, 50)
                self.DISPLAY.blit(text, textRect)
            
            if(winnerBall.message != '' or winnerBall.message != None):
                message_surface = mainGame.font.render("  " + winnerBall.message + "  ", True, (255, 255, 255), ball.color)

                # Combine both surfaces vertically into one
                width = max(score_surface.get_width(), message_surface.get_width())
                height = score_surface.get_height() + message_surface.get_height()
                combined_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                combined_surface.blit(score_surface, ((message_surface.get_width()-score_surface.get_width())//2, 0))
                combined_surface.blit(message_surface, (0, score_surface.get_height()))
            
            textRect = combined_surface.get_rect()
            textRect.center = [self.DISPLAY.get_width()//2,150]
            self.DISPLAY.blit(combined_surface, textRect)
            
            winnerBall.winUpdate()
            FPS.tick(60)
            pygame.display.update()
        pygame.quit()
        # self.musicController.export_audio(str(time.time())+".wav", self.time * 1000)