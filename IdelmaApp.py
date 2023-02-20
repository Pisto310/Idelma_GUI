from PyQt5.QtWidgets import (QApplication, QListWidgetItem)

from IdelmaGui import IdelmaGui
from IdelmaNewSct import IdelmaNewSct

from BoardInfos import BoardInfos
from BoardInfosQObject import BoardInfosQObject
from SctPropQListWidgetItem import SctPropQListWidgetItem

from ListWidgetItemUserTypes import ListWidgetItemUserType

from SerialHandler import SerialHandler
from UserEvents import UserEvents


class IdelmaApp(QApplication):
    """
    Class for the Idelma main App
    """
    def __init__(self, *args):
        super().__init__(*args)

        # Instantiating Back-end objects
        self.arduino = BoardInfosQObject()
        self.ser = SerialHandler()

        # Declaring a virtual arduino board for all changes not pushed to the actual MCU
        self.virtualBoard = None

        # Instantiating and Declaring UI objects
        self.ui = IdelmaGui()

        # Section property objects list and creating an ItemType for QListWidgetItems that are Section Properties obj
        self.sctPropList = []
        self.sctPropItemType = ListWidgetItemUserType.newUserType('Section Properties Type')

        # Connecting signals
        self.assigningSlots()

        # Show the widget (window)
        self.ui.show()

    def assigningSlots(self):
        # Board infos signals
        self.arduino.connectSnSignal(self.ui.updtSnNumLabel)
        self.arduino.connectFwVerSignal(self.ui.updtFwVerLabel)
        self.arduino.connectSctsSignal(self.ui.updtSctsInfo)
        self.arduino.connectPxlsSignal(self.ui.updtPxlsInfo)

        # Fetch board infos button
        self.ui.fetchInfosButton.clicked.connect(self.fetchBrdInfos)

        # Add/create section
        self.ui.sctAddButton.clicked.connect(self.newSectionDialog)

        # ListWidget signals
        self.ui.sectionsList.itemClicked.connect(self.enableListWidgetBttns)

    def fetchBrdInfos(self):
        """
        Runs the board infos fetch protocol which includes:
        1. Reading all the board infos from the arduino
        2. Enabling/Disabling GUI buttons
        3. Creating a virtual board with the fetched infos
        """
        self.ser.getAllBrdInfos(self.arduino)

        self.ui.fetchInfosButton.setEnabled(False)
        self.ui.sctAddButton.setEnabled(True)

        self.instantiateVrtlBrd()

    def enableListWidgetBttns(self, item: QListWidgetItem):
        self.ui.sctDeleteButton.setEnabled(True)
        self.ui.sctEditButton.setEnabled(True)

    def instantiateVrtlBrd(self):
        """
        Instantiates a BoardInfos object and fills
        all its attr with the ones recently fetched
        from the actual MCU
        """
        self.virtualBoard = BoardInfos()
        self.virtualBoard.serialNum = self.arduino.serialNum
        self.virtualBoard.fwVersion = self.arduino.fwVersion
        self.virtualBoard.sctsBrdMgmt = self.arduino.sctsBrdMgmt
        self.virtualBoard.pxlsBrdMgmt = self.arduino.pxlsBrdMgmt

    def newSectionDialog(self):
        """
        1. User enters the new section info (name & pixel count)
        2. Once he presses 'OK', the info is available to use
        3. Create a 'SectionProperties object' to be stored in a list'
        4. Show the newly created section in the List Widget (named sectionList of the ui object)
        5. Update the infos of the virtual board
        """
        addSctDialog = IdelmaNewSct(self.virtualBoard.sctsBrdMgmt.assigned,
                                    self.virtualBoard.pxlsBrdMgmt.remaining)
        addSctDialog.connectAccepted(self.sectionCreation)
        addSctDialog.exec_()

    def sectionCreation(self, section_name, pixel_count):
        # Creating new Section Properties object with user input in dialog
        sctPropObj = SctPropQListWidgetItem(section_name, pixel_count, self.ui.sectionsList, self.sctPropItemType)
        self.sctPropList.append(sctPropObj)
        self.virtualBoard.sctsBrdMgmt.blockAssignation(1)
        self.virtualBoard.pxlsBrdMgmt.blockAssignation(pixel_count)

        # Enabling the 'config board' button
        if not self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(True)
