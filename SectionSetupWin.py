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


class SectionSetupWin(QMainWindow):
    """Section Setup Window"""
    def __init__(self, board_info_instance, serial_handler_obj, parent=None):
        """Initializer"""
        super().__init__(parent)
        # setting main window properties
        self.setWindowTitle('Section Setup')
        self.setFixedSize(400, 200)

        # creating a board and a serial attributes attached to the class
        self.board = board_info_instance
        self.ser = serial_handler_obj

        # setting the central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # setting instructions as a label in the central widget
        instruction = QLabel("Please write the number of pixels", self._centralWidget)
        instruction.setWordWrap(True)
        instruction.setAlignment(Qt.AlignHCenter)

        # adding a text box for user to enter pixel number
        self.nbrOfPxls = QLineEdit()
        self.nbrOfPxls.setInputMask("DD")

        userInputLayout = QFormLayout()
        userInputLayout.addRow("pixels :", self.nbrOfPxls)
        userInputLayout.setAlignment(Qt.AlignHCenter)

        # adding a text for warning if info entered is not valid
        self.warning = QLabel()

        # fetching remaining and pixels capacity for set-up
        availPixels = QLabel("pixels %s : %d" % (list(self.board.pxlsInfo.keys())[1],
                                                 self.board.pxlsInfo.get("remaining")))
        boardPxlCapacity = QLabel("board pixels %s : %d" % (list(self.board.pxlsInfo.keys())[0],
                                                 self.board.pxlsInfo.get("capacity")))

        self.warning.setAlignment(Qt.AlignCenter)
        availPixels.setAlignment(Qt.AlignCenter)
        boardPxlCapacity.setAlignment(Qt.AlignCenter)

        boardInfoLayout = QGridLayout()
        boardInfoLayout.addWidget(self.warning, 0, 0)
        boardInfoLayout.addWidget(boardPxlCapacity, 1, 0)
        boardInfoLayout.addWidget(availPixels, 2, 0)
        boardInfoLayout.setAlignment(Qt.AlignCenter)

        # adding in buttons and taking care of the layout
        self.confirmBtn = QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.rqstSectionSetup)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.close)

        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.confirmBtn, 0, 0)
        buttonLayout.addWidget(self.cancelBtn, 0, 1)
        buttonLayout.setAlignment(Qt.AlignHCenter)

        # placing individual layouts in central widget grid
        self.generalLayout.addWidget(instruction)
        self.generalLayout.addLayout(userInputLayout)
        self.generalLayout.addLayout(boardInfoLayout)
        self.generalLayout.addLayout(buttonLayout)

    def rqstSectionSetup(self):
        # Got to confirm if user input is ok
        enteredPxlNbr = int(self.nbrOfPxls.text())
        if self.userInputCheck(enteredPxlNbr):
            self.ser.setupSctRqst(enteredPxlNbr, self.board)
            self.close()
        elif not self.userInputCheck(enteredPxlNbr):
            self.warning.setText("Memory space does not allow to create %d pixels" % enteredPxlNbr)

    # Checks user input with actual board capacity and remaining space
    # returns 'True' if user input checks out, 'False' otherwise
    def userInputCheck(self, user_input_nbr):
        if user_input_nbr <= self.board.pxlsInfo.get("capacity") and \
                user_input_nbr <= self.board.pxlsInfo.get("remaining"):
            return True
        else:
            return False
