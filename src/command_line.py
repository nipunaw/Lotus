import src.lotusCore
import os

def main():
    xlaunch_location = os.path.abspath(os.path.dirname( __file__ ))
    os.chdir(xlaunch_location)
    #os.system('cmd.exe /C taskkill /IM lotus.xlaunch /F') lotus.xlaunch not found - - more research reqd
    os.system('cmd.exe /C lotus.xlaunch')
    src.lotusCore.main()

if __name__ == '__main__':
    main()