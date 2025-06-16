import json
import inspect
import os
import time 

from main import gameProperties
from BallClass import *
from .formatCLI import *


def to_json(currentGame: gameProperties, pathToFile: str, FileName: str):
    all_attrs = {name: value for name, value in inspect.getmembers(currentGame, lambda a: not (inspect.isroutine(a)))
                 if not (name.startswith('__') and name.endswith('__'))}

    newList = []
    for ball in all_attrs['ballList']:
        temp = {name: value for name, value in inspect.getmembers(ball, lambda a: not (inspect.isroutine(a)))
                if not (name.startswith('__') and name.endswith('__'))}
        temp.pop('font')
        temp.pop('_Sprite__g')
        temp.pop('lastPos')
        temp.pop('position')
        temp.pop('display')
        temp.pop('score')
        temp['color'] = (temp['color'][0], temp['color'][1], temp['color'][2])

        newList.append(temp)
    
    all_attrs['ballList'] = newList
    convertedFile = json.dumps(all_attrs)

    if (FileName == None):
        FileName = str(abs(convertedFile.__hash__()))+".json"
    else:
        FileName += ".json"

    if (pathToFile == None):
        pathToFile = './'

    try:
        File = open(pathToFile+'/'+FileName, "x")
        File.write(convertedFile)
    except FileExistsError:
        if(FileName == 'currentGame.json'):
            os.remove(os.path.join(pathToFile, FileName))    
            File = open(pathToFile+'/'+str(time.time())+FileName, "x")
            File.write(convertedFile)
        else:
            File = open(pathToFile+'/'+str(time.time())+FileName, "x")
            File.write(convertedFile)

    printSuccess("File saved as "+pathToFile+FileName)


def to_game(pathToFile: str):
    with open(pathToFile, "r") as File:
        Data = json.loads(File.read())

    game = gameProperties()

    game.screenSize = Data['screenSize']
    game.ballSize = Data['ballSize']
    game.backgroundColor = Data['backgroundColor']
    game.displayScore = Data['displayScore']
    game.minRadius = Data['minRadius']
    game.time = Data['time']
    game.spacingHalo = Data['spacingHalo']
    game.widthHalo = Data['widthHalo']
    game.message = Data['message']
    game.scoreMultiplier = Data['scoreMultiplier']
    game.displayTrails = Data['displayTrails']
    game.trailsLenght = Data['trailsLenght']
    game.midiFile = Data['midiFile']
    game.haloColor = Data['haloColor']
    game.messageEmojie = Data['messageEmojie']
    game.showTimer = Data['showTimer']
    game.haloSpeed = Data['haloSpeed']
    ballList = Data['ballList']
    ballListObject = []

    for ball in ballList:
        ballListObject.append(
            Ball(
                ball['velocity'],
                pygame.Color(tuple(ball['color'])),
                ball['id'],
                ball['message'],
                ball['displayMessage'],
                ball['sound'],
                ball['soundVolume'],
                tuple(ball['ballSize']),
                ball['displayTrail'],
                ball['trailLenght'],
            )
        )
    game.ballList = ballListObject
    return game


def fileTest(fileName: str) -> bool:
    if (os.path.exists(fileName)):
        return True
    else:
        printWarning(
            f"File : {fileName} doe's not exists. Check path or FileName.")
        return False
