
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QSpacerItem, QLabel, QSizePolicy
import SETUP

class OnScreenKeyboard(QWidget):
    def __init__(self, x, y, width, height, lineEdit):
        super().__init__()
        #self.setWindowTitle('On-Screen Keyboard')
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        #set x and y of widget
        self.setGeometry(x, y, width, height)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.layout = QGridLayout()
        self.text_input = lineEdit#QLineEdit()
        #self.layout.addWidget(#self.text_input, 0, 0, 1, 5)

        #set button styles
        #self.setStyleSheet(SETUP.buttonStyle)
        #set window style
        self.setStyleSheet(SETUP.windowStyle)

        buttons = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ':', '.', '-']
        ]

        row = 1
        button_width = SETUP.keyWidth  # Width of each button in pixels
        button_height = SETUP.keyHeight  # Height of each button in pixels
        font_size = SETUP.keyboardFontSize # Font size of the button text

        for button_row in buttons:
            col = 0
            for button_text in button_row:
                button = QPushButton(button_text)
                button.setStyleSheet(SETUP.buttonStyle)
                button.setFixedSize(button_width, button_height)  # Set the size of the button
                button.setFont(QFont('Arial', font_size))  # Set the font size of the button text
                button.clicked.connect(lambda _, text=button_text: self.add_text(text))
                self.layout.addWidget(button, row, col)
                col += 1
            row += 1

        backspace_text = "Backspace"
        backspace_button = QPushButton(backspace_text)
        backspace_button.setStyleSheet(SETUP.buttonStyle)
        backspace_button.setFixedSize(button_width * 3, button_height)  # Set the size of the backspace button
        backspace_button.setFont(QFont('Arial', font_size))  # Set the font size of the button text
        backspace_button.clicked.connect(self.press_backspace)
        self.layout.addWidget(backspace_button, row, 0, 1, 3)

        space_text = "Space"
        space_button = QPushButton(space_text)
        space_button.setStyleSheet(SETUP.buttonStyle)
        space_button.setFixedSize(button_width * 4, button_height)  # Set the size of the space button
        space_button.setFont(QFont('Arial', font_size))  # Set the font size of the button text
        space_button.clicked.connect(self.add_space)
        self.layout.addWidget(space_button, row, 3, 1, 7)

        '''
        enter_text = "Enter"
        enter_button = QPushButton(enter_text)
        enter_button.setStyleSheet(SETUP.buttonStyle)
        enter_button.setFixedSize(button_width*2, button_height)  # Set the size of the enter button
        enter_button.setFont(QFont('Arial', font_size))  # Set the font size of the button text
        enter_button.clicked.connect(self.press_enter)
        self.layout.addWidget(enter_button, row, 7,1,8)
        '''
        self.setLayout(self.layout)

    def add_text(self, text):
        self.text_input.insert(text)

    def add_space(self):
        self.text_input.insert(" ")

    def press_backspace(self):
        self.text_input.backspace()

    def press_enter(self):
        self.text_input.insert("\n")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    keyboard = OnScreenKeyboard()
    keyboard.show()
    sys.exit(app.exec_())