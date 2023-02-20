import sys
import time
from time import sleep
from SerialHandler import SerialHandler
from BoardInfos import BoardInfos
from MutableBrdInfo import MutableBrdInfo

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGraphicsColorizeEffect
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QColorDialog

from PyQt5.QtWidgets import QSlider
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


class SectionEditWin(QMainWindow):
    """Section Edit Window"""
    def __init__(self, board: BoardInfos, serial_handler: SerialHandler, parent=None):
        """Initializer"""
        super().__init__(parent)
        # setting main window properties
        self.setWindowTitle('Sections Editor')
        self.setFixedSize(1280, 744)

        # creating a board and a serial attributes attached to the class
        self.board = board
        self.ser = serial_handler

        # setting the central widget and general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.AddSection = None

        # set a layout for each sections with each section's info displayed and an edit button
        # creating a layout to be included in the general layout to contain these sections layout
        self.sctsLayout = QHBoxLayout()
        self.sctsMinorLayouts = []
        self.sctsMinorBtns = []
        self.setSctsLayouts()

        # Adding buttons "Add Section", "Clear", "Save"
        self.setWinBtns()

        # Creating a list of buttons for all sections possible to instantiate on connected arduino board
        # Since 12 is the max number with arduino, the list will always be n = 12

    def setSctsLayouts(self):
        # Create as many layouts as there are sections according to the correct board inst attr
        for i in range(0, self.board.sctsBrdMgmt.capacity):
            layout = QGridLayout()

            btn = QPushButton("Edit")
            btn.setDisabled(True)

            layout.addWidget(btn)

            self.sctsMinorLayouts.append(layout)
            self.sctsMinorBtns.append(btn)
            self.sctsLayout.addLayout(layout)

        self.generalLayout.addLayout(self.sctsLayout)

    def setWinBtns(self):
        actionBtnsLayout = QGridLayout()

        addBtn = QPushButton("Add Section")
        addBtn.clicked.connect(self.sctSetupDialog)
        clearBtn = QPushButton("Clear All")
        saveBtn = QPushButton("Save")

        actionBtnsLayout.addWidget(addBtn, 0, 0)
        actionBtnsLayout.addWidget(clearBtn, 0, 1)
        actionBtnsLayout.addWidget(saveBtn, 0, 2)

        self.generalLayout.addLayout(actionBtnsLayout)

    def sctSetupDialog(self):
        leds, ok = QInputDialog.getInt(self, "Section set-up", "Number of LEDs :",
                                    1, 1, self.board.pxlsBrdMgmt.remaining)
        if ok:
            self.stripSinglePxl(leds)

    def stripSinglePxl(self, led_count):
        MESSAGE = "<p>Will the section you are creating be treated as a single " \
                  "pixel?</p>" \
                  "<p>In other words, if each LEDs of the section have to behave " \
                  "independently from one another, press No. If not, press Yes</p>"

        reply = QMessageBox.question(self, "QMessageBox.question()", MESSAGE,
                                     QMessageBox.No | QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            single_pxl = 1
            self.ser.sctSetupRqst(self.board, led_count, single_pxl)

        if reply == QMessageBox.No:
            single_pxl = 0
            self.ser.sctSetupRqst(self.board, led_count, single_pxl)

if __name__ == '__main__':
    ser = SerialHandler()
    board = BoardInfos()

    board.pxlsBrdMgmtMssgDecode([100, 100, 0])
    board.sctsBrdMgmtMssgDecode([12, 12, 0])

    app = QApplication(sys.argv)
    window = SectionEditWin(board, ser)
    window.show()
    sys.exit(app.exec())

        # self.AddSection = AddSectionWin(76)
        # self.AddSection.show()

    #     # setting instructions as a label in the central widget
    #     instruction = QLabel("Please write the number of pixels", self._centralWidget)
    #     instruction.setWordWrap(True)
    #     instruction.setAlignment(Qt.AlignHCenter)
    #
    #     # adding a text box for user to enter pixel number
    #     self.nbrOfPxls = QLineEdit()
    #     self.nbrOfPxls.setInputMask("DD")
    #
    #     userInputLayout = QFormLayout()
    #     userInputLayout.addRow("pixels :", self.nbrOfPxls)
    #     userInputLayout.setAlignment(Qt.AlignHCenter)
    #
    #     # adding a text for warning if info entered is not valid
    #     self.warning = QLabel()
    #
    #     # fetching remaining and pixels capacity for set-up
    #     availPixels = QLabel("pixels %s : %d" % (list(self.board.pxlsInfo.keys())[1],
    #                                              self.board.pxlsInfo.get("remaining")))
    #     boardPxlCapacity = QLabel("board pixels %s : %d" % (list(self.board.pxlsInfo.keys())[0],
    #                                              self.board.pxlsInfo.get("capacity")))
    #
    #     self.warning.setAlignment(Qt.AlignCenter)
    #     availPixels.setAlignment(Qt.AlignCenter)
    #     boardPxlCapacity.setAlignment(Qt.AlignCenter)
    #
    #     boardInfoLayout = QGridLayout()
    #     boardInfoLayout.addWidget(self.warning, 0, 0)
    #     boardInfoLayout.addWidget(boardPxlCapacity, 1, 0)
    #     boardInfoLayout.addWidget(availPixels, 2, 0)
    #     boardInfoLayout.setAlignment(Qt.AlignCenter)
    #
    #     # adding in buttons and taking care of the layout
    #     self.confirmBtn = QPushButton("Confirm")
    #     self.confirmBtn.clicked.connect(self.rqstSectionSetup)
    #
    #     self.cancelBtn = QPushButton("Cancel")
    #     self.cancelBtn.clicked.connect(self.close)
    #
    #     buttonLayout = QGridLayout()
    #     buttonLayout.addWidget(self.confirmBtn, 0, 0)
    #     buttonLayout.addWidget(self.cancelBtn, 0, 1)
    #     buttonLayout.setAlignment(Qt.AlignHCenter)
    #
    #     # placing individual layouts in central widget grid
    #     self.generalLayout.addWidget(instruction)
    #     self.generalLayout.addLayout(userInputLayout)
    #     self.generalLayout.addLayout(boardInfoLayout)
    #     self.generalLayout.addLayout(buttonLayout)
    #
    # def rqstSectionSetup(self):
    #     # Got to confirm if user input is ok
    #     enteredPxlNbr = int(self.nbrOfPxls.text())
    #     if self.userInputCheck(enteredPxlNbr):
    #         self.ser.setupSctRqst(enteredPxlNbr, self.board)
    #         self.close()
    #     elif not self.userInputCheck(enteredPxlNbr):
    #         self.warning.setText("Memory space does not allow to create %d pixels" % enteredPxlNbr)
    #
    # # Checks user input with actual board capacity and remaining space
    # # returns 'True' if user input checks out, 'False' otherwise
    # def userInputCheck(self, user_input_nbr):
    #     if user_input_nbr <= self.board.pxlsInfo.get("capacity") and \
    #             user_input_nbr <= self.board.pxlsInfo.get("remaining"):
    #         return True
    #     else:
    #         return False