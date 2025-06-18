class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_to_int_list(s: str) -> list[float]:
    try:
        # Retire les parenthèses et les espaces
        s_clean = s.strip().strip("()").replace(" ", "")
        # Sépare les valeurs par la virgule
        parts = s_clean.split(",")
        # Convertit chaque élément en int
        return [float(part) for part in parts]
    except (ValueError, AttributeError):
        raise ValueError(f"Format invalide : '{s}' (attendu : '(x, y)')")


def parse_to_three_tuple(s: str) -> tuple[int]:
    try:
        # Retire les parenthèses et les espaces
        s_clean = s.strip().strip("()").replace(" ", "")
        # Sépare les valeurs par la virgule
        parts = s_clean.split(",")
        # Convertit chaque élément en int
        return [int(part) for part in parts]
    except (ValueError, AttributeError):
        raise ValueError(f"Format invalide : '{s}' (attendu : '(r, g, b)')")


def printWarning(message: str):
    print(bcolors.BOLD+bcolors.WARNING+"WARNING : " +
          bcolors.ENDC+bcolors.WARNING+message+bcolors.ENDC)


def printSuccess(message):
    print(bcolors.BOLD+bcolors.OKGREEN+"SUCCESS : " +
          bcolors.ENDC+bcolors.OKGREEN+message+bcolors.ENDC)


def printInvalidCommand(errorMessage: str = "Invalid command"):
    """
    Prints an error message to the console in a formatted style using color codes.

    Args:
        errorMessage (str): The error message to be displayed.

    This function uses the bcolors class to format and highlight error messages for better visibility in the CLI.
    """
    print(bcolors.BOLD+bcolors.FAIL+"ERROR : " +
          bcolors.ENDC+bcolors.FAIL+errorMessage+bcolors.ENDC)


def printModifyBallMenu(ball: any) -> None:
    print("\n" + bcolors.BOLD + bcolors.OKCYAN +
          "╔══════════════════════════════╗")
    print("║        Current Ball          ║")
    print("╚══════════════════════════════╝" + bcolors.ENDC)

    ball.toStringSelf()

    print("\n" + bcolors.BOLD + bcolors.OKCYAN +
          "╔═══════════════════════════════════════════════════╗")
    print("║             Select parameter to modify            ║")
    print("╠═══════════════════════════════════════════════════╣")
    print(
        f"║ 1. Velocity                ({bcolors.ENDC}float list ex: (x, y){bcolors.OKCYAN})║")
    print(
        f"║ 2. Color                   ({bcolors.ENDC}r,g,b{bcolors.OKCYAN})                ║")
    print(
        f"║ 3. Message                 ({bcolors.ENDC}string{bcolors.OKCYAN})               ║")
    print(
        f"║ 4. Display message on Ball ({bcolors.ENDC}True/False{bcolors.OKCYAN})           ║")
    print(
        f"║ 5. Sound effect            ({bcolors.ENDC}path to .mp3{bcolors.OKCYAN})         ║")
    print(
        f"║ 6. Sound volume            ({bcolors.ENDC}0.0 to 1.0{bcolors.OKCYAN})           ║")
    print(
        f"║ 7. Self Ball Size            ({bcolors.ENDC}ex : [int,int]{bcolors.OKCYAN})     ║")

    print(
        f"║ 8. Image                   ({bcolors.ENDC}Path to image{bcolors.OKCYAN})        ║")
    print(
        f"║ 9. {bcolors.FAIL}Delete Ball{bcolors.OKCYAN}                                                                 ║")
    print("╠═══════════════════════════════════════════════════╣")
    print("║         Type 'exit' to return to main menu        ║")
    print("╚═══════════════════════════════════════════════════╝" + bcolors.ENDC)
