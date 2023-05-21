PATIENT_NAME = None

delimiter = ','
arduinoDelimiter = ' '
updatedSchedule = False
recentlyDispensed = False
onStartup = False
checkScheduleInterval = 60 #seconds

windowHeight = 1020
windowWidth = 600
windowXLoc = 0
windowYLoc = 0

margin = 25
changePageButtonWidth = windowWidth - margin*2
changePageButtonHeight = 50
changePageButtonX = margin
changePageButtonY = [windowHeight - (margin + changePageButtonHeight), windowHeight - ((changePageButtonHeight + margin)*2),windowHeight - ((changePageButtonHeight + margin)*3)]

addMedPopupWidth = windowWidth
addMedPopupHeight = windowHeight

editMedPopupWidth = addMedPopupWidth
editMedPopupHeight = addMedPopupHeight

settingsPopupWidth = windowWidth
settingsPopupHeight = windowHeight

addMedNameY = 25
addMedTrayNumberY = 90
addMedAmountY = 150
addMedHourY = 210
addMedMinuteY = 210
addMedDaysY = 270
addMedBoxesY = 310


addMedSaveY = 400
addMedSaveWidth = 200

keyboardWidth = 400
keyboardHeight = 400
keyboardX = 0 #int((windowWidth - keyboardWidth)/2) / 2
keyboardY = windowHeight - keyboardHeight

keyWidth = 52
keyHeight = 60
keyboardFontSize = 22

upcomingHeight = 250
labelHeight = 30
textFieldHeight = 25

lineEditStyle = "font-size: 16px;"
labelStyle = "font-size: 24px; color: #386641;"
dropDownStyle = "width: 30px; color: #386641; background-color: #ffffff; border: solid; border-radius: 5px; padding: 10px; font-size: 12px;"
#make checkbox bigger
checkboxStyle = "font-size: 20px" #"width: 5px; height: 5px;"

buttonStyle = "QPushButton {background-color: #386641; color: white; border: none; border-radius: 5px; padding: 10px; font-size: 16px; } QPushButton:hover {background-color: #6a994e; color: white; border: none; border-radius: 5px; padding: 10px; font-size: 16px; } QPushButton:pressed {background-color: #a7c957; color: white; border: none; border-radius: 5px; padding: 10px; font-size: 16px;}"
windowStyle = "background-color: #f7f2e3;"
tableStyle = "background-color: #ffffff; color: #386641; font-size: 16px; selection-background-color: #a7c957; selection-color: #386641;"
clockStyle = "background-color: #ffffff; color: #386641; font-size: 16px; selection-background-color: #a7c957; selection-color: #386641;"
#onclick color for table cell = #a7c957
#labelStyle = "color: #386641; font-size: 16px;"
#textFieldStyle = "background-color: #a7c957; color: #386641; border: none; border-radius: 5px; padding: 10px; font-size: 16px;"
popupStyle = "background-color: #f7f2e3;"

'''
blue 531CB3
black 170312
purple aa7BC3

'''


