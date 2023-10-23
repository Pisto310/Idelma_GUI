from PyQt5.QtWidgets import (QApplication, QListWidgetItem)

import serial.serialutil
from serial.tools.list_ports_osx import comports
import os
import pty

from IdelmaGui import IdelmaGui
from IdelmaSctDialog import IdelmaSctDialog
from IdelmaSctDelDialog import IdelmaSctDelDialog
from IdelmaDuplicateNameDialog import IdelmaDuplicateNameDialog

from BoardInfos import BoardInfos
from BoardInfosQObject import BoardInfosQObject
from MutableMetaData import MutableMetaData
from SctProp import SctProp
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
        self.ui.saveButton.clicked.connect(self.saveSettingsCmd)

    def fetchBrdInfosCmd(self):
        """
        Runs the board infos fetch protocol which includes:
        1. Reading all the board infos from the arduino
        2. Enabling/Disabling GUI buttons
        3. Creating a virtual board with the fetched infos
        """

        self.ser.serRqst(self.ser.serialRqsts.get("serial_num"), self.board.serialNumUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("fw_version"), self.board.fwVersionUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("scts_metadata"), self.board.sctsMetaDataUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("pxls_metadata"), self.board.pxlsMetaDataUpdt)

        self.ui.fetchInfosButton.setEnabled(False)
        self.ui.sctAddButton.setEnabled(True)

        self.instantiateVrtlBrd()

        self.fillingSctPropList()

    def configBrdCmd(self):
        """
        Passes all the necessary info (metadata of each sections) to the serial Handler
        """
        self.ser.serRqst(self.ser.serialRqsts.get("config_board"), self.board.configBrdAttrUpdt, *self.metaDataCompare())

        self.configBrdBttnStateTrig()

        if not self.ui.saveButton.isEnabled():
            self.ui.saveButton.setEnabled(True)

    def saveSettingsCmd(self):
        """
        Save the last sent configuration in the MCU's EEPROM memory
        """
        self.ser.serRqst(self.ser.serialRqsts.get("save_settings"), self.board.ackConfirmed)

        self.ui.saveButton.setEnabled(False)

    def instantiateVrtlBrd(self):
        """
        Instantiates a BoardInfosQObject object and fills
        all its attr with the ones recently fetched
        from the actual MCU, thus creating a virtual brd
        """
        self.virtualBoard = BoardInfos()
        self.virtualBoard.serialNum = self.board.serialNum
        self.virtualBoard.fwVersion = self.board.fwVersion
        self.virtualBoard.sctsMetaData = MutableMetaData(self.board.sctsMetaData.capacity,
                                                        self.board.sctsMetaData.remaining,
                                                        self.board.sctsMetaData.assigned)
        self.virtualBoard.pxlsMetaData = MutableMetaData(self.board.pxlsMetaData.capacity,
                                                        self.board.pxlsMetaData.remaining,
                                                        self.board.pxlsMetaData.assigned)

    def fillingSctPropList(self):
        """
        Fills the sctPropList with as much 'None type obj'
        as the section capacity of fetched board
        """
        counter = 0
        while counter < self.board.sctsMetaData.capacity:
            self.sctPropList.append(None)
            counter += 1

    def resourcesAvailable(self):
        """
        Checks if there are remaining resources (sections & pixels)
        left for user assignation
        """
        if self.virtualBoard.sctsMetaData.remaining and self.virtualBoard.pxlsMetaData.remaining:
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
        for index, section in enumerate(self.sctPropList[-1 * (self.virtualBoard.sctsMetaData.remaining + 1)::-1]):
            if section.sctName == input_name:
                self.ui.sectionsList.setCurrentItem(section)
                return True
        return False

    def metaDataCompare(self):
        """
        Compares the metadata of board obj and virtualBoard obj to choose action accordingly
        """
        if len(self.board.sctsInfoTuple) == 0:
            return self.virtualBoard.sctsInfoTuple
        else:
            container = []
            for i, val in enumerate(self.virtualBoard.sctsInfoTuple):
                try:
                    if val != self.board.sctsInfoTuple[i]:
                        container.append(val)
                        if not val[SctProp.infoTupleIndexes.get('pixelCount_index')]:
                            self.virtualBoard.sctsInfoTuple.pop(i)
                except IndexError:
                    if val[SctProp.infoTupleIndexes.get('pixelCount_index')]:
                        container.append(val)
            return container

    def newSectionDialog(self):
        """
        Pop-up a dialog in which user has to enter the required
        info to create a new section. Once accepted by the user,
        a 'button check' is performed
        """
        addSctDialog = IdelmaSctDialog(self.virtualBoard.sctsMetaData.assigned, self.virtualBoard.pxlsMetaData.remaining)
        addSctDialog.connectAccepted(self.sectionCreation)
        addSctDialog.exec_()

        # Buttons check
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

        self.configBrdBttnStateTrig()

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
        editSctDialog = IdelmaSctDialog(sct_index, self.virtualBoard.pxlsMetaData.remaining,
                                        sct_name, pxl_count)
        editSctDialog.connectAccepted(self.sectionEdit)
        editSctDialog.exec_()

        # Buttons check
        if self.resourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

        self.configBrdBttnStateTrig()

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
        Called everytime a new section is created by the user

        Parameters:
            section_name (str): name of the created section
            pixel_count (int): number of pixels to be contained in the section
            set_default_name (bool): a bool indicating if the name is set to default
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

        sctPropObj = SctPropQListWidgetItem(self.virtualBoard.sctsMetaData.assigned, pixel_count, section_name,
                                            set_default_name, self.ui.sectionsList, self.sctPropItemType)
        self.sctPropList[self.virtualBoard.sctsMetaData.assigned] = sctPropObj
        self.virtualBoard.sctsInfoTuple.append(sctPropObj.sctInfoTuple)
        self.virtualBoard.sctsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.sctsMetaData.capacity,
                                                                  self.virtualBoard.sctsMetaData.remaining,
                                                                  self.virtualBoard.sctsMetaData.assigned,
                                                                  1)
        self.virtualBoard.pxlsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.pxlsMetaData.capacity,
                                                                  self.virtualBoard.pxlsMetaData.remaining,
                                                                  self.virtualBoard.pxlsMetaData.assigned,
                                                                  pixel_count)

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
        pixel_count = self.sctPropList[sct_index].pxlCount

        while sct_index <= (self.virtualBoard.sctsMetaData.assigned - 1):
            if self.sctPropList[sct_index + 1] is None:
                self.ui.sectionsList.takeItem(sct_index)
                del self.sctPropList[sct_index]
                self.virtualBoard.sctsInfoTuple[sct_index] = (sct_index, 0)
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
                self.virtualBoard.sctsInfoTuple[sct_index] = self.sctPropList[sct_index].sctInfoTuple
            sct_index += 1

        self.virtualBoard.sctsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.sctsMetaData.capacity,
                                                                 self.virtualBoard.sctsMetaData.remaining,
                                                                 self.virtualBoard.sctsMetaData.assigned,
                                                                 -1)
        self.virtualBoard.pxlsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.pxlsMetaData.capacity,
                                                                 self.virtualBoard.pxlsMetaData.remaining,
                                                                 self.virtualBoard.pxlsMetaData.assigned,
                                                                 -abs(pixel_count))

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
        new_sctPropObj = SctPropQListWidgetItem(sct_index, new_pixel_count, new_section_name, new_set_default_name,
                                                None, self.sctPropItemType)

        if self.sctPropList[sct_index] != new_sctPropObj:
            # Allocating or deallocating pixel resources
            edited_sct = self.ui.sectionsList.takeItem(sct_index)
            self.virtualBoard.pxlsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.pxlsMetaData.capacity,
                                                                     self.virtualBoard.pxlsMetaData.remaining,
                                                                     self.virtualBoard.pxlsMetaData.assigned,
                                                                     new_pixel_count - edited_sct.pxlCount)
            self.ui.sectionsList.insertItem(sct_index, new_sctPropObj)
            self.sctPropList[sct_index] = new_sctPropObj
            self.virtualBoard.sctsInfoTuple[sct_index] = self.sctPropList[sct_index].sctInfoTuple
        else:
            del new_sctPropObj

    def sectionReplacement(self, new_pixel_count: int):
        """
        Only called when user has accepted to overwrite an already
        existing section with another having the same name. So it's
        only necessary to change the pxl_count attribute of existing sct
        """
        pxl_updt = new_pixel_count - self.ui.sectionsList.currentItem().pxlCount
        if pxl_updt:
            self.sctPropList[self.ui.sectionsList.currentRow()].pxlCount = new_pixel_count
            self.virtualBoard.pxlsMetaData = MutableMetaData.blockUpdt(self.virtualBoard.pxlsMetaData.capacity,
                                                                     self.virtualBoard.pxlsMetaData.remaining,
                                                                     self.virtualBoard.pxlsMetaData.assigned,
                                                                     pxl_updt)
            self.virtualBoard.sctsMetaData[self.ui.sectionsList.currentRow()] = (self.ui.sectionsList.currentRow(),
                                                                                 new_pixel_count)
