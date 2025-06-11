from main import *
from BallClass import Ball
import cmd
from tools.formatCLI import * 
from tools.FileController import *

class BallFallConsole(cmd.Cmd):
    prompt = '> '
    
    def do_saveGame(self, line : str):
        """Save current game configuration.

        Args:
            *File Path (str) : where to save file
            *File Name (str) : name of the file saved
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        
        args = line.split()
        if(len(args) == 2):
            if(args[0] == '.'):
                args[0] = None 
        
            if(args[1] == '.'):
                args[1] = None
            to_json(self.currentGame, args[0], args[1])
        else:
            to_json(self.currentGame, None, None)
    
    def do_loadGame(self, line:str):
        self.currentGame = to_game(line)
        self.gameInit = True
        printSuccess(" Game loaded succesfully.")
        self.currentGame.toStringAdvanced()

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.gameInit = False
        self.currentGame = None
        
    def default(self, line):
        printInvalidCommand(f"Unknown command: '{line}'")

    def do_initGame(self, line):
        """Initialize a new Game Recording

        Args:
            *screeSize (tuple(int)) : game screen size = (500,800)
            *backgroundColor (tuple(int)) : Color of the background = (0,0,0)
            *time (int) : Game spaning time in seconds
            *spacingHalo (int) : space between each Halo
            *widhtHalo (int) : widht of each Halo in pixels
            *displayScore (bool) : display Ball scores on screen
        """
        args = line.split()
        self.currentGame = gameProperties()
        self.gameInit = True
        
        printSuccess("Game initialized succesfully")

        if(len(args) == 0):
            printWarning(" game initialized with default values")
            self.currentGame.screenSize = [500, 800]
            self.currentGame.backgroundColor = (0,0,0)
            self.currentGame.spacingHalo = 10
            self.currentGame.time = 10
            self.currentGame.widthHalo = 3
            self.currentGame.displayScore = True
            self.currentGame.message = None
            self.currentGame.scoreMultiplier = 1
            self.currentGame.minRadius = 150
            self.currentGame.ballSize = [15,10]

        else:
            if(len(args) != 6):
                printInvalidCommand(" this function takes 0 or 7 positional arguments." \
                "Type 'iniGame' if you want to use the defaults values")
                return
            else:
                self.currentGame.screenSize = parse_to_int_list(args[0])
                self.currentGame.backgroundColor = parse_to_three_tuple(args[1])
                self.currentGame.time = int(args[2])
                self.currentGame.spacingHalo = int(args[3])
                self.currentGame.widthHalo = int(args[4])
                self.currentGame.displayScore = True
                self.currentGame.message = args[5]

                #Optional
                self.currentGame.scoreMultiplier = 1
                self.currentGame.minRadius = 150
                self.ballSize = [15,10]

    def do_setSong(self, line):
        """_summary_

        Args:
            line (_type_): _description_
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        if line == '':
            printInvalidCommand(" setSong command takes one positional argument.")
        else:
            if(fileTest(line)):
                self.currentGame.midiFile = line
            else:
                return
            
    def do_setMinRadius(self, line):
        """Advance option.
            Set the minimum radius (smallest Radius possible for a Halo) 

        Args:
            line (int): radius
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        try:
            new_radius = int(line)
            printSuccess(f" Minimum Radius changed : {self.currentGame.minRadius} -> {new_radius}")
            self.currentGame.minRadius = new_radius
        except ValueError:
            printInvalidCommand(" minimum Radius must be a int.")


    def do_setScoreMultiplier(self, line):
        """Set the score multiplier for the game.

        Args:
            line (int): score multiplier value
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        try:
            new_multiplier = int(line)
            printSuccess(f" Score Multiplier changed : {self.currentGame.scoreMultiplier} -> {new_multiplier}")
            self.currentGame.scoreMultiplier = new_multiplier
        except ValueError:
            printInvalidCommand(" scoreMultiplier must be a int.")

    def do_setDisplayScore(self,line):
        """Enalbe displaying of Balls score on screen

        Args:
            line (bool): True to enable, False to unable

        Exemple Usage:
            setDisplayScore True
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        if(line.lower() not in ['false', 'true']):
            printInvalidCommand("invalid argments : parameter must be a boolean")
            return
        else:
            printSuccess(f" Display score setted : {self.currentGame.displayScore} -> {line.lower()}")
            if(line.lower() == 'true'):
                self.currentGame.displayScore = True
            else:
                self.currentGame.displayScore = False

    def do_setBackgroundColor(self, line):
        """Change the background Color of the Game

        Args:
            line (tuple(int)): Color of the background

        Raises:
            ValueError: if input color is in a invalid format
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            printInvalidCommand(" backgroundColor setter function only takes one positional argument.")
            return
        try:
            temp = parse_to_three_tuple(line)
            if not (isinstance(temp, tuple) and len(temp) == 3 and all(isinstance(x, int) for x in temp)):
                raise ValueError
            old_value = self.currentGame.backgroundColor
            self.currentGame.backgroundColor = temp
            printSuccess(f"parameter backgroundColor changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            printInvalidCommand(" backgroundColor must be a tuple of three integers.")

    def do_setSpacingHalo(self, line):
        """Set spacing between Halos.
            This parameter may have an influence on Balls Velocity : if spacing is rising, it will create greater falls and Balls will accumulate much more velocity because of gravity.

        Args:
            line (int): spacing between each Halo
        
        Exemple Usage:
            setSpacingHalo 3
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            printInvalidCommand(" spacingHalo setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.spacingHalo
            self.currentGame.spacingHalo = temp
            printSuccess(f"parameter spacingHalo changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            printInvalidCommand(" spacingHalo must be an integer.")

    def do_setTime(self, line):
        """Change time of Game.
            This time is in seconds.

        Args:
            line (int): game Time
        
        Usage Exemple: 
            setTime time:float
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            printInvalidCommand(" time setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.time
            self.currentGame.time = temp
            printSuccess(f"parameter time changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            printInvalidCommand(" time must be an integer.")

    def do_setBallSize(self, line : str):
        """Change ball inner and outer size

        Args:
            ballSize (tuple(int)) : ball inner an outer size

        Exemple Usage:
            setBallSize (a,b)
            with : a = outer size
                   b = inner size

        """  
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        try:
            new_size = parse_to_int_list(line)
            if(new_size[0] < new_size[1]):
                printInvalidCommand("Inner size can't be greater than outer size")
                return
            printSuccess(f" Global Ball Size Changed succesfully {self.currentGame.ballSize} -> {new_size}")
            self.currentGame.ballSize
            self.modifyAllBalls('ballSize')
        except ValueError:
            printInvalidCommand(" ball size must be a list of int.")
    
    def do_setDisplayTrail(self, line: str):
        """Enable or disable the display of ball trails.

        Args:
            line (bool): True to enable, False to disable

        Exemple Usage:
            setDisplayTrail True
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        if line.lower() not in ['false', 'true']:
            printInvalidCommand("invalid arguments: parameter must be a boolean")
            return
        new_value = line.lower() == 'true'
        printSuccess(f" Display trail set: {getattr(self.currentGame, 'displayTrails', False)} -> {new_value}")
        self.currentGame.displayTrails = new_value
        self.modifyAllBalls('displayTrails')

    def do_setTrailLenght(self, line: str):
        """Set the length of the ball trail.

        Args:
            line (int): trail length

        Exemple Usage:
            setTrailLenght 15
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return
        try:
            new_length = int(line)
            printSuccess(f" Trail length changed: {getattr(self.currentGame, 'trailsLenght', None)} -> {new_length}")
            self.currentGame.trailsLenght = new_length
            self.modifyAllBalls('trailsLenght')
        except ValueError:
            printInvalidCommand(" trail length must be an integer.")

    def modifyAllBalls(self, paramName : str):
        print("Do you want to apply this parameter to all current Balls ? [Y/n]")
        command = input()
        if(command.lower() in ['y', 'yes', 'true']):
            self.currentGame.modifyAllBalls(paramName)
        else:
            print("Nothing has been Changed.")

    def do_setWidthHalo(self, line):
        """Change the widht of every Halo in the game.

        Args:
            line (float): width of each Halo

        Usage Exemple:
            setWidthHalo width:float
        """
        if not self.gameInit:
            printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            printInvalidCommand(" widthHalo setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.widthHalo
            self.currentGame.widthHalo = temp
            printSuccess(f"parameter widthHalo changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            printInvalidCommand(" widthHalo must be an integer.")
    
    def do_createBall(self, line):
        """create a ball for the currentGame.

        Args:
            velocity (tuple(int,int))  : initial velocity of the ball
            color (tuple(int,int,int)) : Color of the Ball
            *message (str)             : Description of the ball or message displayed on screen for score
            *display Message (bool)    : Display the message on the ball
            *sound  (str)              : path to mp3 sounds to the format ./path/to/sounds.mp3 (dot represent the current location of the project, you can write absolute path)
            *volume (float)            : sound effect volume, each time the ball escape a Halo, it will play this sound
            *ballSize (tuple(int,int)) : ball inner and outer size
            *displayTrail (bool)       : display trail of the ball, can affect performances
            *trailLenght (int)         : trail Lenght, be sure to have displayTrail = True, otherwise chnaging this parameter will be useless
        
        Usage Exemple:
            - minimum requirement: createBall (-10,0) (255,0,0)
            - maximum arguments : createBall (-10,0) (255,0,0) No False ./sounds/No.mp3 1.0 [15,10] True 15
        """
        if(not self.gameInit):
            printInvalidCommand("Can not execute command 'createBall'.\n You must initialize a game by using command 'initGame'")
            return
        args = line.split()
        if(len(args) < 2):
            printInvalidCommand("ball creation takes atleast 2 arguments.")
            return
        
        else:
            for i in range(9-len(args)):
                args.append(None)
            
            try:
                if(args[3] != None):
                    args[3] = bool(args[3])
                
                if(args[5] != None):
                    args[5] = float(args[5])
                
                if(args[6] != None):
                    args[6] = parse_to_int_list(args[6])
                    if(args[6] < args[6]): 
                        printInvalidCommand("Inner size can't be greater than outer size")
                        raise ValueError("Ball size invalid")
                else:
                    args[6] = self.currentGame.ballSize

                if(args[7] != None):
                    if(not args[7].lower() in ['true', 'false', '0', '1']):
                        raise ValueError(" display Trail can only be a boolean value")
                    else:
                        args[7] = args[7].lower() in ['true', '1']
                        
                else:
                    args[7] = self.currentGame.displayTrails

                if(args[8] != None):
                    if(not args[7]):
                        printWarning(" Trail is not enable.")
                    else:
                        args[8] = int(args[8])
                else:
                    args[8] = self.currentGame.trailsLenght
                
                temp_color = parse_to_three_tuple(args[1]) # cast str to tuple, then convert it into a pygame.Color object while creating Ball

                ball = Ball(parse_to_int_list(args[0]), 
                        pygame.Color(temp_color[0],temp_color[1],temp_color[2]),
                        len(self.currentGame.ballList),
                        args[2],
                        args[3],
                        args[4],
                        args[5], 
                        args[6],
                        args[7],
                        args[8]
                        )

                self.currentGame.ballList.append(ball)
                self.currentGame.toString()

            except ValueError as v:
                printInvalidCommand(f" can't create ball : {v}")

    def do_deleteBall(self, line):
        """Delete a ball in the current Game

        Args:
            line (int): id of the ball to delete
        """
        if(not self.gameInit):
            printInvalidCommand("Can not execute command 'createBall'.\n You must initialize a game by using command 'initGame'")
            return
        
        id = int(line)
        for i in range(len(self.currentGame.ballList)):
            if(self.currentGame.ballList[i].id == id):
                self.currentGame.ballList.pop(i)
                printSuccess(f" ball {id} has been succesfully deleted.")
                return
        printInvalidCommand(f" No ball with id {id}")

    def do_alterBall(self, line):
        """Open the sub menu to modify a specific Ball

        Args:
            line (int): ball ID

        Returns:
            None : Error in command
        
        Usage Exemple:
            alterBall 0
        """
        if not self.gameInit:
            printInvalidCommand("No game has been initialized.")
            return

        args = line.split()
        if len(args) != 1:
            printInvalidCommand("alterBall takes exactly one argument: the ball id.")
            return

        try:
            ball_id = int(args[0])
        except ValueError:
            printInvalidCommand("Ball id must be an integer.")
            return

        ball = None
        for b in self.currentGame.ballList:
            if b.id == ball_id:
                ball = b
                break

        if not ball:
            printInvalidCommand(f"No ball with ID {ball_id}")
            return

        while True:
            printModifyBallMenu(ball)
            choice = input(bcolors.BOLD + "> Parameter number: " + bcolors.ENDC).strip()

            if choice.lower() == 'exit':
                break
            if choice not in {'1', '2', '3', '4', '5', '6', '7', '8'}:
                printInvalidCommand("Invalid selection.")
                continue

            param_map = {
                '1': 'velocity',
                '2': 'color',
                '3': 'message',
                '4': 'displayMessage',
                '5': 'sound',
                '6': 'volume',
                '7': 'ballSize',
                '8': 'deleteBall'
            }
            param = param_map[choice]
            
            if(param == 'deleteBall'):
                new_value = input(bcolors.BOLD+bcolors.WARNING+f" Are you sure you want to delete ball {ball_id} ?"+bcolors.ENDC)
                if(new_value.lower() in ['yes', 'y']):
                    self.currentGame.ballList.pop(ball_id)
                    printSuccess(" Ball deleted from game.")
                    break
                else:
                    continue

            new_value = input(f"Enter new value for {param}: ").strip()
            
            try:
                match param:
                    case 'velocity':
                        ball.velocity = parse_to_int_list(new_value)
                    case 'color':
                        ball.color = parse_to_three_tuple(new_value)
                    case 'message':
                        ball.message = new_value
                    case 'displayMessage':
                            ball.displayMessage = new_value.lower() in ['true', '1', 'yes']
                    case 'sound':
                        ball.sound = new_value
                    case 'volume':
                        ball.volume = float(new_value)
                    case 'ballSize':
                        new_size = parse_to_int_list(new_value)
                        if(new_size[0] < new_size[1]):
                            printInvalidCommand("Inner size can't be greater than outer size")
                            return
                        printWarning(" you modified only THIS ball size, change global parameters to set all ball Size.\n" \
                        "Several ball on the screen without the same size can occurs in error while running game.")                        
                printSuccess(f"{param} updated successfully.")
            except Exception:
                printInvalidCommand(f"Invalid value for {param}.")

    def do_displayBall(self, id : int):
        """Display a specific ball with it's ID.

        Args:
            id (int): id of the ball, this ID is frozen and unique for each ball in the game
        Return:
            Ball informations or Error if the ball does'nt exists
        """
        for ball in self.currentGame.ballList:
            if(ball.id == int(id)):
                ball.toStringSelf()
                return
        printInvalidCommand(f"No ball with ID {id}")

    def do_setScreenSize(self, line):
        """Change game screen size
            You must initialize a game before changing it's screen screen or this function will return an error.
        Args:
            line (_type_): New screen size in a form of a tuple of int : (x: int, y: int) 

        Usage Exemple : 
            setScreenSize (x: int,y: int)
        """
        if(not self.gameInit):
            printInvalidCommand(" no game has been initialized.")
            return
        
        args = line.split()
        if(len(args) > 1):
            printInvalidCommand(" screen Size setter function only takes one positional argument.")
            return
        
        if(len(args) == 0):
            printInvalidCommand(" screen Size setter function takes one positional argument.")
            return
        
        temp = parse_to_int_list(line)
        printSuccess(f" Paramater Updated : {self.currentGame.screenSize} -> {temp}")
        self.currentGame.screenSize = temp

    def do_setTitle(self, line : str):
        """Set a messsage / title on top of the screen.
            Write 'None' to display Nothing

        Args:
            line (str): Title / message
    
        """
        if(not self.gameInit):
            printInvalidCommand(" no game has been initialized.")
            return

        printSuccess(f" Title of Game changed : {self.currentGame.message} -> {line}")
        if(line == 'None'):
            self.currentGame.message = None
        else:
            self.currentGame.message = line

    def do_displayGame(self, line):
        """Display current game informations
        No arguments are required for this function

        Args:
            line (str): display all or nothing
        
        Exemple Usage:
            displayGame -> display game informations
            displayGame All -> display all game informartions
        """
        if(not self.gameInit):
            printInvalidCommand(" no game has been initialized.")
            return

        if(line == 'All'):
            self.currentGame.toStringAdvanced()
        else:
            self.currentGame.toString()
        
    def do_startGame(self, line):
        """Start the game with the current parameters

        Args:
            line (None): None
        
        Warning : can display a warning if no Ball were created by the user. 
                  You can use the default Balls or cancel.
        """
        if(not self.gameInit):
            printInvalidCommand(" no game has been initialized.")
            return
        
        if(len(self.currentGame.ballList) == 0):
            printWarning(" current Game have no ball instantiated !")
            print("do you want to proceed anyways with default parameters ? [Y/n]")
            while True:
                command = input()

                if command.lower() in ['y', "yes", '1']:
                    break
                else:
                    return
        
        self.currentGame.toString()
        print("When Game will start, you won't be able to modify any parameters until the end of the Game.")
        print("Are you sure you want to proceed ? [Y/n]")
        while True:
            command = input()
            if command.lower() in ['y', "yes", '1']:
                break
            else:
                return
        
        self.do_saveGame("./cache currentGame")
        mainGame(self.currentGame)
        self.do_loadGame("./cache/currentGame.json")
        
    def do_qs(self, line):
        """Quickstart with defaults parameters, used for test or demo.

        Args:
            line (None): None
        """
        self.currentGame = to_game('test\\default_game.json')
        self.gameInit = True
        
        self.do_saveGame("./cache currentGame")
        mainGame(self.currentGame)
        self.do_loadGame("./cache/currentGame.json")
        
    def do_exit(self, line):
        """quit program

        Args:
            line (None): unused

        Returns:
            bool: Exit the program
        """
        print("Goodbye !")
        return True

    def do_EOF(self, line):
        """qui console / program
        Args:
            line (None): None

        Returns:
            bool: Exit the console / program
        """
        print("Console Exit.")
        return True
    
    @staticmethod
    def entryPoint():
        print(bcolors.HEADER+bcolors.BOLD+bcolors.UNDERLINE+" "*50+bcolors.ENDC+bcolors.HEADER+bcolors.BOLD)
        print(
        "    ____          __ __   ______        __ __"
        +"\n   / __ ) ____ _ / // /  / ____/____ _ / // /"
        +"\n  / __  |/ __ `// // /  / /_   / __ `// // / "
        +"\n / /_/ // /_/ // // /  / __/  / /_/ // // /  "
        +"\n/_____/ \__,_//_//_/  /_/     \__,_//_//_/")
        print("─"*50+bcolors.ENDC)
        print("\n")
        print(bcolors.OKCYAN+"─"*20+" Main Menu "+"─"*20+bcolors.ENDC)
        print("\t-Type 'initGame' to create a new recording !")
        print("\t-Type 'help' or '?' for help")

        console = BallFallConsole()
        console.cmdloop()

BallFallConsole.entryPoint()