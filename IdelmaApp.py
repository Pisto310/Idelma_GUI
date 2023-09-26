from PyQt5.QtWidgets import (QApplication, QListWidgetItem)

import serial.serialutil
from serial.tools.list_ports_osx import comports
import os
import pty

from IdelmaGui import IdelmaGui
from IdelmaSctDialog import IdelmaSctDialog
from IdelmaSctDelDialog import IdelmaSctDelDialog
from IdelmaDuplicateNameDialog import IdelmaDuplicateNameDialog

from BoardInfosQObject import BoardInfosQObject
from MutableBrdInfo import MutableBrdInfo
from SctPropQListWidgetItem import SctPropQListWidgetItem
from ArduinoEmulator import ArduinoEmulator

from ListWidgetItemUserTypes import ListWidgetItemUserType

from SerialHandlerQObject import SerialHandlerQObject
from UserEvents import UserEvents


class IdelmaApp(QApplication):
    """
    Class for the Idelma main App
    """
    def __init__(self, *args):
        super().__init__(*args)

        # Opening a serial port
        self.serialPort = None
        self.arduinoEmu = None
        self.openSerialPort()

        # Instantiating Back-end objects
        self.board = BoardInfosQObject()
        self.ser = SerialHandlerQObject(self.serialPort)

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

    def openSerialPort(self):
        """
        From the list of COM ports available, method uses the 'device' attr.
        of the returned ListPortInfo obj. (port of for loop) to assign it to
        the serialPort attr. of the Idelma App. If an arduino COM port isn't
        found, a virtual one is created and used instead
        """
        try:
            for port in comports():
                if port.manufacturer == 'Arduino (www.arduino.cc)':
                    self.serialPort = port.device
            if self.serialPort is None:
                raise serial.serialutil.SerialException
        except serial.serialutil.SerialException:
            master, slave = pty.openpty()
            virtualPort = os.ttyname(slave)
            self.serialPort = virtualPort
            self.arduinoEmu = ArduinoEmulator(master)

    def assigningSlots(self):
        # Serial handler signals
        if self.arduinoEmu is not None:
            self.ser.connectNotifySignal(self.arduinoEmu.processSerialMssg)

        # Board infos signals
        self.board.connectSnSignal(self.ui.updtSnNumLabel)
        self.board.connectFwVerSignal(self.ui.updtFwVerLabel)
        self.board.connectSctsSignal(self.ui.updtSctsInfo)
        self.board.connectPxlsSignal(self.ui.updtPxlsInfo)

        # Fetch board infos button
        self.ui.fetchInfosButton.clicked.connect(self.fetchBrdInfosCmd)

        # ListWidget signals and buttons
        self.ui.sctAddButton.clicked.connect(self.newSectionDialog)
        self.ui.sctDeleteButton.clicked.connect(self.deleteSectionDialog)
        self.ui.sctEditButton.clicked.connect(self.editSectionDialog)
        self.ui.sectionsList.itemClicked.connect(self.ui.enableListWidgetBttns)

        # Board config and save buttons
        self.ui.configButton.clicked.connect(self.configBrdCmd)

    def fetchBrdInfosCmd(self):
        """
        Runs the board infos fetch protocol which includes:
        1. Reading all the board infos from the arduino
        2. Enabling/Disabling GUI buttons
        3. Creating a virtual board with the fetched infos
        """
        self.ser.getAllBrdInfos(self.board)

        self.ui.fetchInfosButton.setEnabled(False)
        self.ui.sctAddButton.setEnabled(True)

        self.instantiateVrtlBrd()

        self.fillingSctPropList()

    def configBrdCmd(self):
        """
        1. Extract index of each section
        3. Extract pxl number of each section
        4. Assemble info in a list
        5. Pass list to serial handler
        """
        sct_metadata = []
        for index, val in enumerate(self.sctPropList):
            if val is None:
                break
            else:
                sct_metadata.append(val.sctInfoTuple)
        self.ser.configBrdRqst(*sct_metadata)

    def instantiateVrtlBrd(self):
        """
        Instantiates a BoardInfosQObject object and fills
        all its attr with the ones recently fetched
        from the actual MCU, thus creating a virtual brd
        """
        self.virtualBoard = BoardInfosQObject()
        self.virtualBoard.serialNum = self.board.serialNum
        self.virtualBoard.fwVersion = self.board.fwVersion
        self.virtualBoard.sctsBrdMgmt = MutableBrdInfo(self.board.sctsBrdMgmt.capacity,
                                                       self.board.sctsBrdMgmt.remaining,
                                                       self.board.sctsBrdMgmt.assigned)
        self.virtualBoard.pxlsBrdMgmt = MutableBrdInfo(self.board.pxlsBrdMgmt.capacity,
                                                       self.board.pxlsBrdMgmt.remaining,
                                                       self.board.pxlsBrdMgmt.assigned)

    def fillingSctPropList(self):
        """
        Fills the sctPropList with as much 'None type obj'
        as the section capacity of fetched board
        """
        counter = 0
        while counter < self.board.sctsBrdMgmt.capacity:
            self.sctPropList.append(None)
            counter += 1

    def blockUsageUpdt(self, pixel_count, assignation: bool):
        """
        Method to be called when assigning or reallocating
        pixels and sections blocks.
        """
        if assignation:
            self.virtualBoard.sctsBrdMgmt.blockAssignation(1)
            self.virtualBoard.pxlsBrdMgmt.blockAssignation(pixel_count)
        else:
            self.virtualBoard.sctsBrdMgmt.blockReallocation(1)
            self.virtualBoard.pxlsBrdMgmt.blockReallocation(pixel_count)
        # SctPropQListWidgetItem.updtRemainingPxls(SctPropQListWidgetItem, self.virtualBoard.pxlsBrdMgmt.remaining)

    def resourcesAvailable(self):
        """
        Checks if there are remaining resources (sections & pixels)
        left for user assignation
        """
        if self.virtualBoard.sctsBrdMgmt.remaining and self.virtualBoard.pxlsBrdMgmt.remaining:
            return True
        else:
            return False

    def configBrdBttnStateTrig(self):
        """
        Compares virtual board with arduino to determine if
        necessary to enable or disable the 'config. board' bttn
        """
        if self.virtualBoard != self.board and not self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(True)
        elif self.virtualBoard == self.board and self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(False)

    def duplicateNameCheck(self, input_name):
        """
        Scans through all already created sections names and checks
        if the sct pending its creation is a duplicate
        """
        for index, section in enumerate(self.sctPropList[-1 * (self.virtualBoard.sctsBrdMgmt.remaining + 1)::-1]):
            if section.sctName == input_name:
                self.ui.sectionsList.setCurrentItem(section)
                return True
        return False

    def newSectionDialog(self):
        """
        Pop-up a dialog in which user has to enter the required
        info to create a new section. Once accepted by the user,
        a 'button check' is performed
        """
        addSctDialog = IdelmaSctDialog(self.virtualBoard.sctsBrdMgmt.assigned, self.virtualBoard.pxlsBrdMgmt.remaining)
        addSctDialog.connectAccepted(self.sectionCreation)
        addSctDialog.exec_()

        # Calling method to see if necessary to trig state of 'config. board' bttn
        self.configBrdBttnStateTrig()

        # Buttons check
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

    def deleteSectionDialog(self):
        """
        Pop-up a warning dialog of the involvement of deleting
        a section and prompts the user to decline or accept
        """
        deleteSctDialog = IdelmaSctDelDialog()
        deleteSctDialog.connectAccepted(self.sectionDeletion)
        deleteSctDialog.exec_()

    def editSectionDialog(self):
        """
        Basically calls the same Dialog than when creating a section,
        but blanks are filled with section's actual properties
        """
        sct_index = self.ui.sectionsList.currentRow()
        sct_name = self.sctPropList[sct_index].sctName
        pxl_count = self.sctPropList[sct_index].pxlCount
        editSctDialog = IdelmaSctDialog(sct_index, self.virtualBoard.pxlsBrdMgmt.remaining,
                                        sct_name, pxl_count)
        editSctDialog.connectAccepted(self.sectionEdit)
        editSctDialog.exec_()

        # Buttons check
        if self.resourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

    def duplicateNameDialog(self):
        """
        Func that calls the duplicate name Dialog window.
        Returns the dialog's results
        0: No
        1: Yes
        2: Keep Both
        """
        nameDuplicateDialog = IdelmaDuplicateNameDialog(self.ui.sectionsList.currentItem().sctName)
        nameDuplicateDialog.exec_()
        return nameDuplicateDialog.result()

    def sectionCreation(self, section_name: str, pixel_count: int, set_default_name: bool):
        """
        Method used to create a new section by first creating a ListWidgetItem
        and adding it to the UI ListWidget, and then updating the virtual brd
        Begins with a name duplicate check
        """
        if self.duplicateNameCheck(section_name):
            duplicate_res = self.duplicateNameDialog()
            if duplicate_res == 0:
                return self.newSectionDialog()
            elif duplicate_res == 1:
                return self.sectionReplacement(pixel_count)
            elif duplicate_res == 2:
                new_name = section_name + ' (1)'
                while self.duplicateNameCheck(new_name):
                    new_name = section_name + ' (' + str(int(new_name[-2]) + 1) + ')'
                section_name = new_name
        sctPropObj = SctPropQListWidgetItem(self.virtualBoard.sctsBrdMgmt.assigned, section_name, pixel_count,
                                            set_default_name, self.ui.sectionsList, self.sctPropItemType)
        self.sctPropList[self.virtualBoard.sctsBrdMgmt.assigned] = sctPropObj
        self.blockUsageUpdt(pixel_count, True)

    def sectionDeletion(self, *args):
        """
        Called after user has dealt with warning dialog. Signal slot
        for section delete button is changed to this method directly
        if checkbox was checked
        """
        if len(args):
            if args[0]:
                self.ui.sctDeleteButton.clicked.disconnect()
                self.ui.sctDeleteButton.clicked.connect(self.sectionDeletion)

        sct_index = self.ui.sectionsList.currentRow()
        pixels = self.sctPropList[sct_index].pxlCount

        while sct_index <= (self.virtualBoard.sctsBrdMgmt.assigned - 1):
            if self.sctPropList[sct_index + 1] is None:
                self.ui.sectionsList.takeItem(sct_index)
                del self.sctPropList[sct_index]
            else:
                if not (self.sctPropList[sct_index].setDefaultName and self.sctPropList[sct_index + 1].setDefaultName):
                    self.sctPropList[sct_index].sctName = self.sctPropList[sct_index + 1].sctName
                    if self.sctPropList[sct_index + 1].setDefaultName:
                        self.sctPropList[sct_index].setDefaultName = True
                        self.sctPropList[sct_index].decrDefaultName()
                    else:
                        self.sctPropList[sct_index].setDefaultName = False
                    self.sctPropList[sct_index].setText()
                self.sctPropList[sct_index].pxlCount = self.sctPropList[sct_index + 1].pxlCount
            sct_index += 1

        self.blockUsageUpdt(pixels, False)

        # Buttons check
        if self.resourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.ui.sectionsList.count():
            self.ui.disableListWidgetBttns()
        self.configBrdBttnStateTrig()

    def sectionEdit(self, new_section_name: str, new_pixel_count: int, new_set_default_name: bool):
        """
        Once section dialog is accepted by user, every necessary
        operations for mods are done in this method
        """
        sct_index = self.ui.sectionsList.currentRow()

        # Allocating or deallocating pixel resources
        edited_sct = self.ui.sectionsList.takeItem(sct_index)
        self.virtualBoard.pxlsBrdMgmt.blockAssignation(new_pixel_count - edited_sct.pxlCount)

        # Creating a new sctPropObj with updated attr and adding it to the ListWidget and the sctPropList
        new_sctPropObj = SctPropQListWidgetItem(new_section_name, new_pixel_count, new_set_default_name,
                                                None, self.sctPropItemType)
        self.ui.sectionsList.insertItem(sct_index, new_sctPropObj)
        self.sctPropList[sct_index] = new_sctPropObj

    def sectionReplacement(self, new_pixel_count: int):
        """
        Only called when user has accepted to overwrite an already
        existing section with another having the same name. So it's
        only necessary to change the pxl_count attribute of existing sct
        """
        pxl_updt = new_pixel_count - self.ui.sectionsList.currentItem().pxlCount
        if pxl_updt:
            self.sctPropList[self.ui.sectionsList.currentRow()].pxlCount = new_pixel_count
            if pxl_updt > 0:
                self.virtualBoard.pxlsBrdMgmt.blockAssignation(pxl_updt)
            elif pxl_updt < 0:
                self.virtualBoard.pxlsBrdMgmt.blockReallocation(pxl_updt)
