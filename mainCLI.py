from main import *
from BallClass import Ball
import cmd
from formatCLI import * 

class BallFallConsole(cmd.Cmd):
    prompt = '> '

    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.gameInit = False
        self.currentGame = None
    

    @staticmethod
    def printMainMenu():
        """
        Displays the main menu options to the user in the command-line interface.

        This function prints a formatted main menu with options for creating a new record,
        loading parameters, and accessing help. It uses the bcolors class for text formatting.
        """
        print(bcolors.UNDERLINE+"-"*10+" Main Menu "+"-"*10+bcolors.ENDC)
        print("Type 'initGame' to create a new recording !")
        print("2. Load parameters")
        print("Type 'help' or '?' for help")

    @staticmethod
    def printInvalidCommand(errorMessage : str = "Invalid command"):
        """
        Prints an error message to the console in a formatted style using color codes.

        Args:
            errorMessage (str): The error message to be displayed.

        # This function uses the bcolors class to format and highlight error messages for better visibility in the CLI.
        """
        print(bcolors.BOLD+bcolors.FAIL+"ERROR : "+bcolors.ENDC+bcolors.FAIL+errorMessage+bcolors.ENDC)

        
    def default(self, line):
        self.printInvalidCommand(f"Unknown command: '{line}'")

    def printWarning(self, message: str):
        print(bcolors.BOLD+bcolors.WARNING+"WARNING : "+bcolors.ENDC+bcolors.WARNING+message)

    def printSuccess(self, message):
        print(bcolors.BOLD+bcolors.OKGREEN+"SUCCESS : "+bcolors.ENDC+bcolors.OKGREEN+message)

    def do_initGame(self, line):
        """Initialize a new game Recording
        """
        args = line.split()
        self.currentGame = gameProperties()
        self.gameInit = True
        
        self.printSuccess("Game initialized succesfully")

        if(len(args) == 0):
            self.printWarning(" game initialized with default values")
            self.currentGame.screenSize = [500, 800]
            self.currentGame.backgroundColor = (0,0,0)
            self.currentGame.spacingHalo = 10
            self.currentGame.time = 10
            self.currentGame.widthHalo = 3
        else:
            if(len(args) != 5):
                self.printInvalidCommand(" this function takes 0 or 5 positional arguments." \
                "Type 'iniGame' if you want to use the defaults values")
                return
            else:
                self.currentGame.screenSize = parse_to_int_list(args[0])
                self.currentGame.backgroundColor = parse_to_three_tuple(args[1])
                self.currentGame.time = int(args[2])
                self.currentGame.spacingHalo = int(args[3])
                self.currentGame.widthHalo = int(args[4])
    
    def do_setBackgroundColor(self, line):
        if not self.gameInit:
            self.printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            self.printInvalidCommand(" backgroundColor setter function only takes one positional argument.")
            return
        try:
            temp = parse_to_three_tuple(line)
            if not (isinstance(temp, tuple) and len(temp) == 3 and all(isinstance(x, int) for x in temp)):
                raise ValueError
            old_value = self.currentGame.backgroundColor
            self.currentGame.backgroundColor = temp
            self.printSuccess(f"parameter backgroundColor changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            self.printInvalidCommand(" backgroundColor must be a tuple of three integers.")

    def do_setSpacingHalo(self, line):
        if not self.gameInit:
            self.printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            self.printInvalidCommand(" spacingHalo setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.spacingHalo
            self.currentGame.spacingHalo = temp
            self.printSuccess(f"parameter spacingHalo changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            self.printInvalidCommand(" spacingHalo must be an integer.")

    def do_setTime(self, line):
        if not self.gameInit:
            self.printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            self.printInvalidCommand(" time setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.time
            self.currentGame.time = temp
            self.printSuccess(f"parameter time changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            self.printInvalidCommand(" time must be an integer.")

    def do_setWidthHalo(self, line):
        if not self.gameInit:
            self.printInvalidCommand(" no game has been initialized.")
            return

        args = line.split()
        if len(args) > 1:
            self.printInvalidCommand(" widthHalo setter function only takes one positional argument.")
            return
        try:
            temp = int(line)
            old_value = self.currentGame.widthHalo
            self.currentGame.widthHalo = temp
            self.printSuccess(f"parameter widthHalo changed, old value -> {old_value}, new Value -> {temp}")
        except Exception:
            self.printInvalidCommand(" widthHalo must be an integer.")
    
    def do_createBall(self, line):
        """_summary_

        Args:
            line (_type_): _description_
        """
        if(not self.gameInit):
            self.printInvalidCommand("Can not execute command 'createBall'.\n You must initialize a game by using command 'initGame'")
            return
        args = line.split()
        if(len(args) < 2):
            self.printInvalidCommand("ball creation takes atleast 2 arguments.")
            return
        else:
            for i in range(8-len(args)):
                args.append(None)
            
            try:
                if(args[3] != None):
                    args[3] = bool(args[3])
                
                if(args[5] != None):
                    args[5] = float(args[5])

                ball = Ball(parse_to_int_list(args[0]), 
                        parse_to_three_tuple(args[1]),
                        len(self.currentGame.ballList),
                        args[2],
                        args[3],
                        args[4],
                        args[5])
                
                self.currentGame.ballList.append(ball)
                self.currentGame.toString()

            except ValueError as v:
                self.printInvalidCommand(" can't create ball : ", v)

    def do_alterBall(self, line):
        if not self.gameInit:
            self.printInvalidCommand("No game has been initialized.")
            return

        args = line.split()
        if len(args) != 1:
            self.printInvalidCommand("alterBall takes exactly one argument: the ball id.")
            return

        try:
            ball_id = int(args[0])
        except ValueError:
            self.printInvalidCommand("Ball id must be an integer.")
            return

        ball = None
        for b in self.currentGame.ballList:
            if b.id == ball_id:
                ball = b
                break

        if not ball:
            self.printInvalidCommand(f"No ball with ID {ball_id}")
            return

        while True:
            print("\nCurrent Ball:")
            ball.toStringSelf()
            print("\nSelect parameter to modify:")
            print("1. position")
            print("2. color")
            print("3. name")
            print("4. isActive")
            print("5. type")
            print("6. speed")
            print("Type 'exit' to return to main menu.")
            choice = input("Parameter number: ").strip()
            if choice.lower() == 'exit':
                break
            if choice not in {'1', '2', '3', '4', '5', '6'}:
                self.printInvalidCommand("Invalid selection.")
                continue

            param_map = {
                '1': 'position',
                '2': 'color',
                '3': 'name',
                '4': 'isActive',
                '5': 'type',
                '6': 'speed'
            }
            param = param_map[choice]
            new_value = input(f"Enter new value for {param}: ").strip()
            try:
                if param == 'position':
                    ball.position = parse_to_int_list(new_value)
                elif param == 'color':
                    ball.color = parse_to_three_tuple(new_value)
                elif param == 'name':
                    ball.name = new_value
                elif param == 'isActive':
                    ball.isActive = new_value.lower() in ['true', '1', 'yes']
                elif param == 'type':
                    ball.type = new_value
                elif param == 'speed':
                    ball.speed = float(new_value)
                self.printSuccess(f"{param} updated successfully.")
            except Exception:
                self.printInvalidCommand(f"Invalid value for {param}.")
    def do_displayBall(self, id : int):
        for ball in self.currentGame.ballList:
            if(ball.id == int(id)):
                ball.toStringSelf()
                return
        self.printInvalidCommand(f"No ball with ID {id}")

    def do_setScreenSize(self, line):
        if(not self.gameInit):
            self.printInvalidCommand(" no game has been initialized.")
            return
        
        args = line.split()
        if(len(args) > 1):
            self.printInvalidCommand(" screen Size setter function only takes one positional argument.")
            return
        temp = parse_to_int_list(line)
        self.currentGame.screenSize = temp

    def do_displayGame(self, line):
        self.currentGame.toString()

    def do_exit(self, line):
        """Quitter la console"""
        print("Au revoir !")
        return True

    def do_EOF(self, line):
        """Quitter en tapant Ctrl+D"""
        print("Fin de la console.")
        return True
    
    @staticmethod
    def entryPoint():
        print( bcolors.HEADER+bcolors.BOLD+"_"*50)
        print(
        "    ____          __ __   ______        __ __"
        +"\n   / __ ) ____ _ / // /  / ____/____ _ / // /"
        +"\n  / __  |/ __ `// // /  / /_   / __ `// // / "
        +"\n / /_/ // /_/ // // /  / __/  / /_/ // // /  "
        +"\n/_____/ \__,_//_//_/  /_/     \__,_//_//_/")
        print(bcolors.BOLD+"_"*50+bcolors.ENDC)
        console = BallFallConsole()
        console.printMainMenu()
        console.cmdloop()

BallFallConsole.entryPoint()