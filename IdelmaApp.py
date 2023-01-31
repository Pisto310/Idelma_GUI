from PyQt5.QtWidgets import QApplication
from IdelmaGui import IdelmaGui
from BoardInfosQObject import BoardInfosQObject
from SerialHandler import SerialHandler
from UserEvents import UserEvents


class IdelmaApp(QApplication):
    """
    Class for the Idelma main App
    """
    def __init__(self, *args):
        super().__init__(*args)

        # instantiating necessary objects for app to operate
        self.arduino = BoardInfosQObject()
        self.ui = IdelmaGui()
        self.ser = SerialHandler()

        # connecting signals
        self.assigningSlots()
        # self.ui.fetchInfosButton.clicked.connect(self.fetchBoardInfos)

        self.ui.show()

    def assigningSlots(self):
        # Board infos signals
        self.arduino.connectSnSignal(self.ui.updtSnNumLabel)
        self.arduino.connectFwVerSignal(self.ui.updtFwVerLabel)
        self.arduino.connectSctsSignal(self.ui.updtSctsInfo)
        self.arduino.connectPxlsSignal(self.ui.updtPxlsInfo)

        # Fetch board infos button
        self.ui.fetchInfosButton.clicked.connect(self.fetchBrdInfos)

    def fetchBrdInfos(self):
        self.ser.getAllBrdInfos(self.arduino)

        # Enabling GUI buttons to add sections
        self.ui.sctAddButton.setEnabled(True)
