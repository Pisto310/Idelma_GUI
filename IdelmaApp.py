import sys
import time
from time import sleep
from SerialHandler import *
from BoardInfos import *

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
from SectionSetupWin import SectionSetupWin


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
        self._sectionSetupWin = None

        self.ser = SerialHandler()
        self.board = BoardInfos()

        # setting the central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # setting a welcome message as a label in the central widget
        self.welcome = QLabel("Welcome to the app!", self._centralWidget)
        self.welcome.setAlignment(Qt.AlignHCenter)

        # adding buttons
        self.colorDebugBtn = QPushButton("Open Color Debug")
        self.colorDebugBtn.clicked.connect(self.openColorDebugWin)

        self.addSectionBtn = QPushButton("Add Section")
        self.addSectionBtn.clicked.connect(self.rqstCreateSection)

        self.saveConfigBtn = QPushButton("Save Config")
        #self.saveConfigBtn.clicked.connect()

        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.colorDebugBtn, 0, 0)
        buttonLayout.addWidget(self.addSectionBtn, 1, 0)
        buttonLayout.setAlignment(Qt.AlignHCenter)


        # # adding slider for choosing white value
        # self.whiteSlider = QSlider(Qt.Vertical)
        # self.whiteSlider.setMinimum(0)
        # self.whiteSlider.setMaximum(255)
        # self.whiteSlider.setSingleStep(1)
        # self.whiteSlider.TicksLeft

        # sliderLayout = QGridLayout()
        # sliderLayout.addWidget(self.whiteSlider)

        # placing widgets on grid
        self.generalLayout.addWidget(self.welcome)
        # self.generalLayout.addLayout(colorIndicatorLayout)
        # self.generalLayout.addLayout(userInputLayout)
        self.generalLayout.addLayout(buttonLayout)
        # self.generalLayout.addLayout(sliderLayout)

        self.rqstBoardInfos()

        # self._createMenu()
        # self._createToolBar()
        # self._createStatusBar()

    def openColorDebugWin(self):
        self._colorDebugWin = ColorDebugWin(self.serHandlerObj)
        self._colorDebugWin.show()

    def rqstBoardInfos(self):
        self.ser.boardInfosRqst(self.board)

    def rqstCreateSection(self):
        self._sectionSetupWin = SectionSetupWin(self.board, self.serHandlerObj)
        self._sectionSetupWin.show()
        #self.serHandlerObj.setupSctRqst()

    def rqstSaveConfig(self):
        self.ser.saveSctsConfig()


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