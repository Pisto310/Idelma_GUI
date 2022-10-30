import sys
import time
from time import sleep
from SerialHandler import SerialHandler
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
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


class AddSectionWin(QDialog):
    """Section Edit Window"""
    def __init__(self, available_pxls):
        """Initializer"""
        super().__init__()
        # setting main window properties
        self.setWindowTitle('Section Setup')
        self.setFixedSize(200, 200)

        self.generalLayout = QVBoxLayout()
        # self.centralWidget = QWidget()
        # self.setCentralWidget(self.centralWidget)

        self.pixels = available_pxls

        self.setLedNbr()

        # self.usrInput = QSpinBox()
        #
        # self.pxlsSpace = QLabel("Remaining pixels : " + str(available_pxls))
        # self.pxlsSpace.setWordWrap(True)
        # self.pxlsSpace.setAlignment(Qt.AlignCenter)
        # self.warningMssg = QLabel()
        # self.warningMssg.setWordWrap(True)
        # self.warningMssg.setAlignment(Qt.AlignCenter)
        #
        # self.btnsBox = QDialogButtonBox()
        #
        # self.createFormLayout()
        # self.createTextLayout()
        # self.createBtnBox()

        # Setting general layout as last action in init
        self.setLayout(self.generalLayout)

    def createFormLayout(self):
        # Using a FormLayout to place a simple SpinBox
        layout = QFormLayout()
        layout.addRow(" Nbr of pixels : ", self.usrInput)
        self.generalLayout.addLayout(layout)

    def createTextLayout(self):
        # Adding text labels here, notably remaining number of pixel space and warning for user input
        layout = QVBoxLayout()
        layout.addWidget(self.pxlsSpace)
        layout.addWidget(self.warningMssg)
        self.generalLayout.addLayout(layout)

    def createBtnBox(self):
        self.btnsBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnsBox.accepted.connect(self.accept)
        self.btnsBox.rejected.connect(self.reject)

        self.generalLayout.addWidget(self.btnsBox)

    def setLedNbr(self):
        i, ok = QInputDialog.getInt(self, "QInputDialog.getInt()", "Crotte", 1, 1, 87)
        if ok:
            print(i)
            print(ok)
