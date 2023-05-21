#cd G:/My Drive/12/Senior Research/code/final
import time
import serial
from arduinoSender import sendToArduino, configureSerial
import SETUP

def mainArduinoComms():
    writeToArduino = True
    encodingType = 'utf-8'

    # initialize lines from schedule.txt file
    file = open("schedule.txt", "r")
    lines = file.readlines()
    file.close()
    init = True
    previousMinute = None
    dispensedInMinute = set()  # keep track of medications dispensed in current minute

    if writeToArduino:
        configureSerial()
        time.sleep(5)
        print("configured serial")
        #pass
        # open serial port
        #serialChannel = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        #serialChannel = serial.Serial("COM3", 9600, timeout=1)
        #serialChannel.reset_input_buffer()
        #serialChannel.reset_output_buffer()

    while True:
        #check the current day on the raspberry pi's system clock
        currentDay = time.strftime("%a") #would display as Mon, Tues, Wed, Thurs, Fri, Sat, or Sun
        currentHour = time.strftime("%H") #would display as 00, 01, 02, ..., 23
        #print(currentHour)
        currentMinute = time.strftime("%M") #would display as 00, 01, 02, ..., 59
        if init:
            previousMinute = currentMinute
            init = False

        #every 30 secs, check schedule.txt file to see if there are any meds to be taken
        #if there are, send the data to the Arduino to be dispensed (note, since Arduino's ring buffer is 16 bytes, only 4 meds can be dispensed at once)
        #if there are not, wait 30 seconds and check again

        #read schedule.txt file if values have been updated
        if(SETUP.updatedSchedule == True):
            file = open("schedule.txt", "r")
            lines = file.readlines()
            file.close()
            print("Arduino side updated SCHEDULE!")
            SETUP.updatedSchedule = False

        #schedule.txt structure: day(Mon Tues Wed Thurs Fri Sat Sun)\thour(0-23)\tminute(0-59)\ttray number\tamount to dispense\tmedication name
        #example: Mon 12 30 1 1 Tylenol
        #split each line into a list of strings and comp

        for line in lines:
            line = line.split(SETUP.delimiter)
            if line[0] == currentDay and int(line[1]) == int(currentHour) and int(line[2]) == int(currentMinute):
                #send data to Arduino as tray number\tamount to dispense
                med_key = (line[5], line[3], line[4])  # medication name, tray number, amount to dispense
                if med_key not in dispensedInMinute:
                    data = str(line[3]) + str(SETUP.arduinoDelimiter) + str(line[4])
                    print("Data sent to arduino:", data)
                    if writeToArduino:
                        sendToArduino(data)
                        time.sleep(2)

                    print("Dispensing " + line[5] + " from tray " + line[3] + " for " + line[4] + " pills")
                    dispensedInMinute.add(med_key)  # add medication to set of dispensed medications for current minute

        # reset dispensedInMinute at the beginning of a new minute
        if previousMinute != currentMinute:
            dispensedInMinute.clear()

        #wait 10 seconds before checking again
        time.sleep(SETUP.checkScheduleInterval)
        previousMinute = currentMinute