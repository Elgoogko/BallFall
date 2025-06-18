import json
import inspect
import os
import time 

from main import gameProperties
from BallClass import *
from .formatCLI import *

version = 2.1
ignoredBallData = ['original_image','font', '_Sprite__g', 'lastPos', 'position', 'display', 'score', 'image', 'soundPlayer']

def to_json(currentGame: gameProperties, pathToFile: str, FileName: str):
    all_attrs = {name: value for name, value in inspect.getmembers(currentGame, lambda a: not (inspect.isroutine(a)))
                 if not (name.startswith('__') and name.endswith('__'))}

    newList = []
    for ball in all_attrs['ballList']:
        temp = {name: value for name, value in inspect.getmembers(ball, lambda a: not (inspect.isroutine(a)))
                if not (name.startswith('__') and name.endswith('__'))}
        for data in ignoredBallData:
            temp.pop(data)
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

def gameCompatibility(Data : dict) -> list[str]:
    """ Check all missing data in save file

    Args:
        Data (dict): data loaded

    Returns:
        list[str]: missing data
    """
    tempGame = gameProperties()
    properties = [key for key in {name: value for name, value in inspect.getmembers(tempGame, lambda a: not (inspect.isroutine(a)))
                 if not (name.startswith('__') and name.endswith('__'))}]
    missingData = []
    for key in Data.keys():
        if not key in properties and key != 'version':
            missingData.append(key)
    return missingData

def ballCompatibility(BallData : dict):
    tempBall =  Ball([0,0], pygame.Color(0,0,0), 0)
    temp = [key for key in {name: value for name, value in inspect.getmembers(tempBall, lambda a: not (inspect.isroutine(a)))
                if not (name.startswith('__') and name.endswith('__'))}]

    ignoredData = ['_Sprite__g', 'lastPos', 'position', 'display','score','image','soundPlayer','font']
    missingData = []
    for key in BallData.keys():
        if not key in temp and not key in ignoredData:
            missingData.append(key)
    return missingData

def to_game(pathToFile: str):
    with open(pathToFile, "r") as File:
        Data = json.loads(File.read())
    
    game = gameProperties()
    if(Data['version'] != version):
        printWarning(f" File is from an older version of the program. \n missing attributes will be setted to defaults values.")
        GmsDatas = gameCompatibility(Data)
        print(bcolors.WARNING+bcolors.HEADER+"----List of missing Data----"+bcolors.ENDC+bcolors.WARNING)
        
        if(len(GmsDatas) != 0):
            print("Missing properties in Game"+bcolors.UNDERLINE)
            for GmsData in GmsDatas:
                print("\t- "+GmsData)

        if(len(Data['ballList']) != 0):
            BmsDatas = ballCompatibility(Data['ballList'][0])
            print(bcolors.ENDC+bcolors.WARNING+"Missing properties in Ball :"+bcolors.UNDERLINE)
            for BmsData in BmsDatas:
                print("\t- "+BmsData)
        print(bcolors.ENDC)

    for key in Data:
        if(key != 'ballList'):
            setattr(game, key, Data[key])
    
    ballList = Data['ballList']
    ballListObject = []

    for ball in ballList:
        tempBall = Ball([0,0], pygame.Color(0,0,0), 0)
        for key in ball.keys():
            if(key == 'color'):
                tempColor = ball['color']
                setattr(tempBall, key, pygame.Color(tempColor[0],tempColor[1],tempColor[2]))
            elif(key == 'sound'):
                tempBall.setSound(ball[key])
            elif(key == 'pathToImage'):
                tempBall.setImage(ball[key])
            else:
                setattr(tempBall, key, ball[key])

        ballListObject.append(tempBall)
    game.ballList = ballListObject
    return game


def fileTest(fileName: str) -> bool:
    if (os.path.exists(fileName)):
        return True
    else:
        printWarning(
            f"File : {fileName} doe's not exists. Check path or FileName.")
        return False
