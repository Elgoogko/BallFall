import sys
import os
import scripts.tools.UpdateInstall as UI

if(len(sys.argv) == 1):
    if(UI.checkModules()):
        os.system("python ./scripts/mainCLI.py")
    else:
        print("Execution aborted.")
        sys.exit(0)
else:
    if(sys.argv[1] == '-p'):
        os.system("python ./scripts/mainCLI.py")