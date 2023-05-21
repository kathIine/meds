import ArduinoComms
import MedsGUI

import threading
import time
import signal
import sys
import SETUP
running  = True

# create two threads
guiThread = threading.Thread(target=MedsGUI.mainGUI, daemon=True)
arduinoThread = threading.Thread(target=ArduinoComms.mainArduinoComms, daemon=True)

def signal_handler(sig, frame):
    print("Exiting...")
    
    # stop the threads
    guiThread.stop()
    arduinoThread.stop()

    # exit the program
    sys.exit(0)

if __name__ == "__main__":
    SETUP.onStartup = True
    guiThread.start()
    arduinoThread.start()

    signal.signal(signal.SIGINT, signal_handler)

    # wait for the threads to finish
    while True:
        time.sleep(1)