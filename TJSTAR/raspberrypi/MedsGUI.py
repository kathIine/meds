#main window class

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import  QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QHeaderView, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox, QComboBox, QCheckBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QDateTime
import SETUP
from onScreenKeyboard import OnScreenKeyboard as o_keyboard

#global main

class ClickableLineEdit(QLineEdit):
    clicked = QtCore.pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)

class Popup(QtWidgets.QWidget):
    def __init__(self, name, xSize, ySize, xLoc, yLoc, parent=None):
        super(Popup, self).__init__(parent)
        #set frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle(name)
        self.resize(xSize, ySize)
        self.move(int(xLoc), int(yLoc))
        #set background color
        self.setStyleSheet(SETUP.popupStyle)

        self.textFields = {}
        self.buttons = {}
        self.checkBoxes = {}
        self.dropDowns = {}

    def addLabel(self, text, xLoc, yLoc):
        label = QtWidgets.QLabel(self)
        label.setStyleSheet(SETUP.labelStyle)
        label.setText(text)
        label.move(xLoc, yLoc)
        label.show()

    def addCheckBox(self, id, text, xLoc, yLoc):
        checkBox = QtWidgets.QCheckBox(text, self)
        checkBox.setStyleSheet(SETUP.checkboxStyle)
        self.checkBoxes[id] = checkBox
        self.checkBoxes[id].move(xLoc, yLoc)
        self.checkBoxes[id].show()

    def showKeyboard(self):
        #show keyboard as a popup
        self.keyboard = o_keyboard(SETUP.keyboardX,SETUP.keyboardY,SETUP.keyboardWidth, SETUP.keyboardHeight, self.textFields["MedName"])
        self.keyboard.show()

    def hideKeyboard(self):
        try:
            self.keyboard.hide()
        except:
            pass

    def addTextField(self, id, xLoc, yLoc):
        text = ClickableLineEdit(self)#QtWidgets.QLineEdit(self)
        text.setStyleSheet(SETUP.lineEditStyle)
        self.textFields[id] = text
        self.textFields[id].move(xLoc, yLoc)
        self.textFields[id].show()
        #attach signal to when qlineedit is clicked. when it is clicked, show an onscreen keyboard, and when it is closed, set the text to the textfield
        self.textFields[id].clicked.connect(lambda: self.textFields[id].setText(self.showKeyboard()))

        return self.textFields[id]
    
    def addButton(self, id, text, size, xLoc, yLoc, func):
        button = QtWidgets.QPushButton(text, self)
        #set button style
        button.setStyleSheet(SETUP.buttonStyle)
        self.buttons[id] = button
        self.buttons[id].resize(size)
        self.buttons[id].move(xLoc, yLoc)
        self.buttons[id].clicked.connect(func)
        self.buttons[id].show()

    def addComboBox(self, id, xLoc, yLoc, items):
        combo = QtWidgets.QComboBox(self)
        combo.setStyleSheet(SETUP.dropDownStyle)
        self.dropDowns[id] = combo
        self.dropDowns[id].addItems(items)
        self.dropDowns[id].move(xLoc, yLoc)
        self.dropDowns[id].show()
        #return self.dropDowns[id]

    def addMed(self, dict):
        global main
        #global main
        #get med name from text field
        name = self.textFields["MedName"].text()
        #get tray number from text field
        tray = self.dropDowns["TrayNumber"].currentText()
        #get amount from text field
        amount = self.dropDowns["MedAmount"].currentText()
        #get time from text field
        hour = self.dropDowns["MedHour"].currentText()
        minute = self.dropDowns["MedMinute"].currentText()
        days = [checkBox.isChecked() for checkBox in self.checkBoxes.values()]
        wordDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        possibleDays = []
        for i in range(7):
            l = list(self.checkBoxes.values())
            if l[i].isChecked():
                possibleDays.append(wordDays[i])
        
        # define a custom string representation method
        def daysToStr(lst):
            return(f"[{','.join(map(str, lst))}]")

        #create med object
        #add med to list
        dict[name] = [name, tray, amount, hour, minute, daysToStr(days)]
        print(dict)
        #write to schedule.txt
        # format medication information as a string
        delim = SETUP.delimiter
        for day in possibleDays:
            med_info = f"{day}{delim}{hour}{delim}{minute}{delim}{tray}{delim}{amount}{delim}{name}"

            # open file in append mode and write medication information
            with open('schedule.txt', 'a') as f:
                # move the file pointer to the end of the last line in the file
                f.seek(0, 2)
                # check if the file pointer is at the beginning of the line
                if f.tell() != 0:
                    # if the file pointer is not at the beginning of the line, add a newline character
                    f.write('\n')
                # write the medication information to the file
                f.write(med_info)
            # close the file
            f.close()
        SETUP.updatedSchedule = True
        print("GUI side updated schedule")
        self.hideKeyboard()
        #close popup
        MainWindow.updateUpcoming(main)
        self.close()
        return dict

    def close(self):
        self.hide()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, xSize, ySize, xLoc, yLoc):
        super(MainWindow, self).__init__()
        #make it so it cant move
        self.setWindowFlags(Qt.FramelessWindowHint)
        #set background color
        self.setStyleSheet(SETUP.windowStyle)
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.xSize = xSize
        self.ySize = ySize
        #move window to top left corner
        self.move(self.xLoc, self.yLoc)
        self.resize(self.xSize, self.ySize)
        self.setWindowTitle("MainWindow")
        self.setFixedSize(self.size())
        self.popups = {}
        self.medInfo = {}

        #add 
        #self.layout = QGridLayout()

    def addClock(self):
        clockFont = QFont('Arial', 100, QFont.Bold)
        #set margins of font
        
        self.clock = QLabel(self)
        self.clock.setWordWrap(True)
        self.clock.setFont(clockFont)
        self.clock.move(0, 0)
        self.clock.resize(SETUP.windowWidth, 250)
        self.clock.setAlignment(Qt.AlignCenter)
        #set style
        #self.clock.setStyleSheet(SETUP.clockStyle)
        clockTimer = QTimer(self)
        clockTimer.timeout.connect(self.showTime)
        clockTimer.start(1000)
        #self.clock.setContentsMargins(0, 0, 0, 0)

        #self.clock.show()


    def addDate(self):
        dateFont = QFont('Arial', 40, QFont.Bold)

        self.date = QLabel(self)
        self.date.setWordWrap(True)
        self.date.setAlignment(Qt.AlignCenter)
        self.date.setFont(dateFont)
        self.date.move(0, 0)
        self.date.resize(SETUP.windowWidth, 600)

        dateTimer = QTimer(self)
        dateTimer.timeout.connect(self.showDate)
        dateTimer.start(1000)

        #bring clock infront of date label
        self.clock.raise_()
        #self.date.show()

    def updateUpcoming(self):
        self.upcomingTable = QTableWidget(self)
        #set size
        self.upcomingTable.resize(SETUP.windowWidth, SETUP.upcomingHeight)
        #set location
        self.upcomingTable.move(0, 400)
        #set style
        self.upcomingTable.setStyleSheet(SETUP.tableStyle)
        self.upcomingTable.setColumnCount(4) #date, time, name, amount
        self.upcomingTable.setHorizontalHeaderLabels(["Day", "Time", "Name", "Amount"])
        self.upcomingTable.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        #after every addmed save OR after a dispense, update upcoming meds for the next 48 hours.

        #read from schedule.txt; format of schedule.txt is [day],[hour],[minute],[tray number],[amount],[medication name]
        #get 48 hours from now as qdate time
        now = QDateTime.currentDateTime()

        #get current day as a string mon tues wed thurs fri sat or sun
        currentDay = now.date().toString("ddd")
        #print("current day",currentDay)
        validDays = []
        if currentDay == "Mon":
            validDays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        elif currentDay == "Tue": 
            validDays = ["Tue","Wed","Thu","Fri","Sat","Sun","Mon"]
        elif currentDay == "Wed":
            validDays = ["Wed","Thu","Fri","Sat","Sun","Mon","Tue"]
        elif currentDay == "Thu": 
            validDays = ["Thu","Fri","Sat","Sun","Mon","Tue","Wed"]
        elif currentDay == "Fri":
            validDays = ["Fri","Sat","Sun","Mon","Tue","Wed","Thu"]
        elif currentDay == "Sat":
            validDays = ["Sat","Sun","Mon","Tue","Wed","Thu","Fri"]
        elif currentDay == "Sun":
            validDays = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
        #read schedule.txt file
        file = open("schedule.txt", "r")
        lines = file.readlines()
        dayLimit = 4
        #for each line, convert day of the week into nearest date and the hour and minute info into a qdateTime object and check if it is within 2 days from now
        validMeds = []
        #validDays = []
        for line in lines:
            line = line.split(SETUP.delimiter)
            print(line)
            #convert day of the week into nearest date
            dayofweek = line[0]

            print(validDays[:dayLimit])
            if dayofweek in validDays[:dayLimit]: #means within 2 days
                validMeds.append(line)
        print("ValidDays",validDays[:dayLimit])
        print("VALID MEDS ARE", validMeds)

        for day in validDays[:dayLimit]:
            for line in validMeds:
                if day == line[0]:
                    #validMeds.remove(line)
                    #validMeds.insert(0, line)
                    #first find meds that have the closest day to now, so in valid days are index 0, then index 1, etc
                    hour = int(line[1])
                    minute = int(line[2])
                    #t = QTime(hour, minute)
                    #strip of newline char if there is one
                    medDay = line[0].strip()
                    self.addMedToUpcoming(medDay, str(hour)+":"+str(minute), line[5], line[4])


        #center items in table
        self.upcomingTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #center items in table
        self.upcomingTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        flags = Qt.ItemFlags(~Qt.ItemIsEditable)
        for row in range(self.upcomingTable.rowCount()):
            for col in range(self.upcomingTable.columnCount()):
                item = self.upcomingTable.item(row, col)
                if item:
                    item.setFlags(flags)
                    item.setTextAlignment(Qt.AlignCenter) # align text to center
        
        self.upcomingTable.show()



    def addMedToUpcoming(self, date, time, task, amount=1):
        row = self.upcomingTable.rowCount()
        self.upcomingTable.insertRow(row)
        self.upcomingTable.setItem(row, 0, QTableWidgetItem(date))
        self.upcomingTable.setItem(row, 1, QTableWidgetItem(time))
        self.upcomingTable.setItem(row, 2, QTableWidgetItem(task))
        self.upcomingTable.setItem(row, 3, QTableWidgetItem(amount))

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        #print(label_time)
        self.clock.setText(label_time)

    def showDate(self):
        current_date = QDate.currentDate()
        label_date = current_date.toString(Qt.DefaultLocaleLongDate)
        self.date.setText(label_date)


    def addPopup(self, name, xSize, ySize):
        #make popup in top center of main window
        self.popups[name] = Popup(name, xSize, ySize, self.xLoc + self.xSize/2 - (xSize/2), self.yLoc)
        self.popups[name].show()

    def addMedPopup(self, name, xSize, ySize):
        self.addPopup(name, xSize, ySize)

        self.popups[name].addLabel("Name", SETUP.margin, SETUP.addMedNameY)
        self.popups[name].addTextField("MedName", SETUP.margin, SETUP.addMedNameY + SETUP.labelHeight)

        #self.textFields["MedName"]
        self.popups[name].addLabel("Tray Number", SETUP.margin, SETUP.addMedTrayNumberY)
        #create dropdown menu
        self.popups[name].addComboBox("TrayNumber", SETUP.margin + 150,SETUP.addMedTrayNumberY, [str(i) for i in range(1,5)])#SETUP.margin + SETUP.labelHeight + SETUP.textFieldHeight + SETUP.labelHeight, [str(i) for i in range(1,5)])

        self.popups[name].addLabel("Amount", SETUP.margin,SETUP.addMedAmountY)
        #amount as a combo box
        self.popups[name].addComboBox("MedAmount", SETUP.margin + 100, SETUP.addMedAmountY, [str(i) for i in range(1,5)])
        
        #hours label
        self.popups[name].addLabel("Hour", SETUP.margin, SETUP.addMedHourY)
        #hours as a combo box
        self.popups[name].addComboBox("MedHour", SETUP.margin + 60,SETUP.addMedHourY, [str(i) for i in range(0,24)])
        
        #minutes label
        self.popups[name].addLabel("Minute", SETUP.margin + 150, SETUP.addMedMinuteY)
        #minutes as a combo box
        self.popups[name].addComboBox("MedMinute", SETUP.margin + 240,  SETUP.addMedMinuteY, [str(i) for i in range(0,60,1)])

        #days of the week as checkboxes
        self.popups[name].addLabel("Days", SETUP.margin, SETUP.addMedDaysY)
        self.popups[name].addCheckBox("Monday", "Mon", SETUP.margin + 25, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Tuesday", "Tue", SETUP.margin + 100, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Wednesday", "Wed", SETUP.margin + 175, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Thursday", "Thu", SETUP.margin + 250, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Friday", "Fri", SETUP.margin + 325, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Saturday", "Sat", SETUP.margin + 400, SETUP.addMedBoxesY)
        self.popups[name].addCheckBox("Sunday", "Sun", SETUP.margin + 475, SETUP.addMedBoxesY)

        self.popups[name].addButton("SaveID", "Save", QtCore.QSize(SETUP.addMedSaveWidth, 50), 10, SETUP.addMedSaveY, lambda: self.popups[name].addMed(self.medInfo))
        #center button in popup
        self.popups[name].buttons["SaveID"].move(int(xSize/2 - (self.popups[name].buttons["SaveID"].width()/2)), SETUP.addMedSaveY)
        self.popups[name].buttons["SaveID"].setStyleSheet(SETUP.buttonStyle)

    def editMedPopup(self, name, xSize, ySize):
        self.addPopup(name, xSize, ySize)
        self.popups[name].addLabel("Name", 10, 10)
        self.popups[name].addTextField("MedName", 10, 30)
        self.popups[name].addLabel("Tray Number", 10, 60)
        self.popups[name].addTextField("TrayNumber", 10, 80)
        self.popups[name].addLabel("Amount", 10, 110)
        self.popups[name].addTextField("MedAmount", 10, 130)
        self.popups[name].addLabel("Time", 10, 160) 
        self.popups[name].addTextField("MedTimes", 10, 180)
        self.popups[name].addButton("SaveID", "Save", QtCore.QSize(100, 50), 10, 210, lambda: self.popups[name].addMed(self.medInfo))
        #center button in popup
        self.popups[name].buttons["SaveID"].move(int(xSize/2 - (self.popups[name].buttons["SaveID"].width()/2)), 210)

    def settingsPopup(self, name, xSize, ySize):
        self.addPopup(name, xSize, ySize)
        self.popups[name].addLabel("Name", 10, 10)
        self.popups[name].addTextField("MedName", 10, 30)
        self.popups[name].addLabel("Tray Number", 10, 60)
        self.popups[name].addTextField("TrayNumber", 10, 80)
        self.popups[name].addLabel("Amount", 10, 110)
        self.popups[name].addTextField("MedAmount", 10, 130)
        self.popups[name].addLabel("Time", 10, 160)
        self.popups[name].addTextField("MedTimes", 10, 180)
        self.popups[name].addButton("SaveSettingsID", "Save", QtCore.QSize(100, 50), 10, 210, lambda: self.popups[name].saveSettings())
        #center button in popup
        self.popups[name].buttons["SaveID"].move(int(xSize/2 - (self.popups[name].buttons["SaveID"].width()/2)), 210)

    def addButton(self, text, size, xLoc, yLoc, func):
        button = QtWidgets.QPushButton(text, self)
        #set button style
        button.setStyleSheet(SETUP.buttonStyle)
        button.resize(size)
        button.move(xLoc, yLoc)
        button.clicked.connect(func)

        button.show()

def mainGUI():
    global main
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(SETUP.windowWidth, SETUP.windowHeight, SETUP.windowXLoc, SETUP.windowYLoc)

    main.addClock()
    main.addDate()
    #add qt label
    upcomingFont = QFont('Arial', 16, QFont.Bold)
    upcomingLabel = QtWidgets.QLabel("Upcoming Medications", main)
    upcomingLabel.resize(SETUP.windowWidth, SETUP.labelHeight)
    upcomingLabel.move(0, 360)
    upcomingLabel.setFont(upcomingFont)
    upcomingLabel.setAlignment(Qt.AlignCenter)

    main.updateUpcoming()
    main.addButton("Add Med", QtCore.QSize(SETUP.changePageButtonWidth, SETUP.changePageButtonHeight), SETUP.changePageButtonX, SETUP.changePageButtonY[2], lambda: main.addMedPopup("Add",SETUP.addMedPopupWidth, SETUP.addMedPopupHeight))
    #main.addButton("Edit Med", QtCore.QSize(SETUP.changePageButtonWidth, SETUP.changePageButtonHeight), SETUP.changePageButtonX, SETUP.changePageButtonY[1], lambda: main.editMedPopup("Edit",SETUP.editMedPopupWidth, SETUP.editMedPopupHeight))
    #main.addButton("Settings", QtCore.QSize(SETUP.changePageButtonWidth, SETUP.changePageButtonHeight), SETUP.changePageButtonX, SETUP.changePageButtonY[0], lambda: main.settingsPopup("Save",SETUP.settingsPopupWidth, SETUP.settingsPopupHeight))
    
    upcomingFont = QFont('Arial', 8, QFont.Bold)
    upcomingLabel = QtWidgets.QLabel("MEDS v3", main)
    upcomingLabel.resize(SETUP.windowWidth, SETUP.labelHeight)
    upcomingLabel.move(15, SETUP.windowHeight - SETUP.labelHeight)
    upcomingLabel.setFont(upcomingFont)
    #upcomingLabel.setAlignment(Qt.AlignCenter)
    
    main.show()

    

    sys.exit(app.exec_())

if __name__ == "__main__":
    mainGUI()