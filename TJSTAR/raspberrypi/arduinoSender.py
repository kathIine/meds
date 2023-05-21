
#send info to arduino
import serial
import time


def configureSerial():
    global serialChannel
    serialChannel = serial.Serial("COM3", 9600, timeout=1)
    serialChannel.reset_input_buffer()
    serialChannel.reset_output_buffer()

def sendToArduino(data):
    global serialChannel
    #while True:
    #data = input("Enter data to send to Arduino: ")
    data = data + "\n"
    serialChannel.write(data.encode('utf-8'))
    print(data.encode('utf-8'))
    time.sleep(1)

if __name__ == "__main__":
    configureSerial()
    time.sleep(5)
    sendToArduino("2 1")