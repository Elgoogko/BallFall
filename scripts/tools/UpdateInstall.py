import sys
import subprocess
from .formatCLI import *

def install(package):
    """Install a specific package with the 'pip' command

    Args:
        package (str): package name
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def checkModules() -> bool:
    """check if all required modules are installed

    Returns:
        bool: when installation is finished
    """
    try:
        import pip
    except ImportError:
        printInvalidCommand(" Pip is not installed ! Install it manually.")
        sys.exit(0)
    
    with open("scripts\\tools\\requirements.txt") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    packagesToInstall = []
    for package in packages:
        try:
            __import__(package.split("==")[0])
        except ImportError:
            packagesToInstall.append(package)
    
    if len(packagesToInstall) == 0:
        return True
    
    printWarning(" some required packages are not installed on your system !")
    for package in packagesToInstall:
        print(bcolors.WARNING+f"\t-{package}")
    print("Do you want to install theses modules ? typing 'no' or 'n' will stop the script. [Y/n]")

    while True:
        command = input()
        if(command.lower() in ['yes', 'y']):
            printWarning("Installing packages")
            break
        else:
            print(bcolors.BOLD+"Goodbye !"+bcolors.ENDC)
            return False

    for package in packagesToInstall:
        install(packages)   

    printSuccess("Succesfully installed all required packages ! \n Thanks for your waiting !")
    return True