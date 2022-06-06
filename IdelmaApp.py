import sys
import time
from time import sleep
from SerialHandler import *
from BoardInfos import BoardInfos

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

from ColorDebugWin import ColorDebugWin
from SectionEditWin import SectionEditWin


def guiTutorial():

    clrPckr = QApplication(sys.argv)

    app = IdelmaApp()
    app.show()

    sys.exit(clrPckr.exec())


class IdelmaApp(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        # setting main window properties
        self.setWindowTitle('IDELMA')
        self.setFixedSize(300, 400)

        self._colorDebugWin = None
        self._sectionEditWin = None

        self.ser = SerialHandler()
        self.board = BoardInfos()
        self.fetchBrdInfos()

        # setting the central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # setting labels in the general layout
        self.setWelcomeMssg()
        self.setBrdInfosLabels()

        # # adding buttons
        # self.colorDebugBtn = QPushButton("Color Debug")
        # self.colorDebugBtn.clicked.connect(self.openColorDebugWin)
        #
        # self.sectionEditBtn = QPushButton("Sections Editor")
        # self.sectionEditBtn.clicked.connect(self.openSectionEditWin)
        #
        # buttonLayout = QGridLayout()
        # buttonLayout.addWidget(self.colorDebugBtn, 0, 0)
        # buttonLayout.addWidget(self.sectionEditBtn, 1, 0)
        # buttonLayout.setAlignment(Qt.AlignHCenter)

        # placing widgets on grid
        # self.generalLayout.addWidget(self.welcome)
        # self.generalLayout.addLayout(colorIndicatorLayout)
        # self.generalLayout.addLayout(userInputLayout)
        # self.generalLayout.addLayout(buttonLayout)
        # self.generalLayout.addLayout(sliderLayout)

        # self._createMenu()
        # self._createToolBar()
        # self._createStatusBar()

    def fetchBrdInfos(self):
        self.ser.getAllBrdInfos(self.board)

    def setWelcomeMssg(self):
        welcome = QLabel("Welcome to the app!", self._centralWidget)
        welcome.setAlignment(Qt.AlignHCenter)

        self.generalLayout.addWidget(welcome)

    def setBrdInfosLabels(self):
        labelLayout = QGridLayout()
        labelLayout.setAlignment(Qt.AlignCenter)

        serialNum = QLabel("Board Serial Number : " + self.board.serialNum, self._centralWidget)
        serialNum.setAlignment(Qt.AlignHCenter)
        fwVersion = QLabel("FW Version : " + self.board.fwVersion, self._centralWidget)
        fwVersion.setAlignment(Qt.AlignHCenter)

        labelLayout.addWidget(serialNum)
        labelLayout.addWidget(fwVersion)

        self.generalLayout.addLayout(labelLayout)

    # def openColorDebugWin(self):
    #     self._colorDebugWin = ColorDebugWin(self.ser)
    #     self._colorDebugWin.show()
    #
    # def openSectionEditWin(self):
    #     self._sectionEditWin = SectionEditWin(self.board, self.ser)
    #     self._sectionEditWin.show()
    #     # self.serHandlerObj.setupSctRqst()


    # def _createMenu(self):
    #     self.menu = self.menuBar().addMenu("&Menu")
    #     self.menu.addAction('&Exit', self.close)
    #
    # def _createToolBar(self):
    #     tools = QToolBar()
    #     self.addToolBar(tools)
    #     tools.addAction('Exit', self.close)
    #
    # def _createStatusBar(self):
    #     status = QStatusBar()
    #     status.showMessage("I'm the Status Bar")
    #     self.setStatusBar(status)