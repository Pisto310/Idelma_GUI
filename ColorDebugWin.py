import sys
import time
from time import sleep
from SerialHandler import *

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsColorizeEffect
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar

from SerialHandler import SerialHandler

class ColorDebugWin(QMainWindow):
    """Real time color cast window"""

    def __init__(self, serial: SerialHandler, parent=None):
        """Initializer"""
        super().__init__(parent)
        # setting main window properties
        self.setWindowTitle('IDELMA')
        self.setFixedSize(300, 400)

        # creating serial handler object
        self.ser = serial

        # color attribute for debugging
        self.color = None
        self.white = None

        # setting the central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # setting a welcome message as a label in the central widget
        self.welcome = QLabel("Welcome to the app!", self._centralWidget)
        self.welcome.setAlignment(Qt.AlignHCenter)

        # adding a form layout for section and pixel number
        userInputLayout = QFormLayout()
        self.sct = QLineEdit()
        self.pxl = QLineEdit()
        self.whiteVal = QLineEdit()
        userInputLayout.addRow('Section:', self.sct)
        userInputLayout.addRow('Pixel:', self.pxl)
        userInputLayout.addRow('White Val.', self.whiteVal)
        userInputLayout.setAlignment(Qt.AlignHCenter)

        # adding label that shows the chosen color and a text label that show the hex value
        self.visualColor = QLabel()
        self.visualColor.setFixedSize(50, 50)
        self.visualColor.setStyleSheet("QLabel"
                                       "{"
                                       "border : 25px solid black;"
                                       "}")
        self.visualColor.setWordWrap(True)

        self.hexColor = QLabel()
        self.hexColor.setText("#000000")

        colorIndicatorLayout = QGridLayout()
        colorIndicatorLayout.addWidget(self.visualColor, 0, 0)
        colorIndicatorLayout.addWidget(self.hexColor, 1, 0)
        colorIndicatorLayout.setAlignment(Qt.AlignHCenter)

        # adding a button to open color picker and to send color
        self.colorPickerBtn = QPushButton("Open Color Picker")
        self.colorPickerBtn.clicked.connect(self.openColorDialogWin)
        self.serialSendBtn = QPushButton("Set Color")
        self.serialSendBtn.clicked.connect(self.sendColorOverSerial)
        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.colorPickerBtn, 0, 0)
        buttonLayout.addWidget(self.serialSendBtn, 1, 0)
        buttonLayout.setAlignment(Qt.AlignHCenter)

        # placing widgets on grid
        self.generalLayout.addWidget(self.welcome)
        self.generalLayout.addLayout(colorIndicatorLayout)
        self.generalLayout.addLayout(userInputLayout)
        self.generalLayout.addLayout(buttonLayout)

    def openColorDialogWin(self):
        # self.color = QColorDialog()
        # self.color.setOption(QColorDialog.NoButtons, on=True)
        #
        # self.color.currentColorChanged.connect(self.sendColorOverSerial)
        #
        # self.color.exec_()

        self.color = QColorDialog.getColor()
        graphic = QGraphicsColorizeEffect(self)

        if self.color.isValid():
            graphic.setColor(self.color)
            self.visualColor.setGraphicsEffect(graphic)
            self.hexColor.setText(self.color.name()[1::])

    def sendColorOverSerial(self):
        # If section and pixel aren't set, they are sent as space (0x20) char by default
        if not len(self.sct.displayText()):
            self.sct.setText('\0')
        if not len(self.pxl.displayText()):
            self.pxl.setText('\0')
        if int(self.whiteVal.displayText()) <= 15:
            tempString = str(hex(int(self.whiteVal.displayText())))
            whiteValHexString = tempString[:2] + "0" + tempString[2:]
        else:
            whiteValHexString = str(hex(int(self.whiteVal.displayText())))
        self.ser.ledColorChangeRqst(self.sct.displayText(), self.pxl.displayText(),
                                       self.hexColor.text()[1::], whiteValHexString[2::])

    def sendColorOverSerial_Continuous(self):
        # If section and pixel aren't set, they are sent as space (0x20) char by default
        if not len(self.sct.displayText()):
            self.sct.setText('\0')
        if not len(self.pxl.displayText()):
            self.pxl.setText('\0')
        self.ser.ledColorChangeRqst(self.sct.displayText(), self.pxl.displayText(), self.color.currentColor().name()[1::])

