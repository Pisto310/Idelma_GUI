from PyQt5.QtWidgets import (QApplication, QListWidgetItem, QDialog)

import serial.serialutil
from serial.tools.list_ports_osx import comports
import os
import pty

from IdelmaGui import IdelmaGui
from IdelmaNewSctDialog import IdelmaNewSctDialog
from IdelmaSctDelDialog import IdelmaSctDelDialog
from IdelmaEditSctDialog import IdelmaEditSctDialog
from IdelmaDuplicateNameDialog import IdelmaDuplicateNameDialog

from BoardMetaDatas import BoardMetaDatas
from BoardMetaDatasQObject import BoardMetaDatasQObject
from BrdMgmtMetaData import BrdMgmtMetaData
from NonSerSctMetaData import NonSerSctMetaData
from NonSerSctMetaDataQListWidgetItem import NonSerSctMetaDataQListWidgetItem
from ArduinoSerialEmulator import ArduinoSerialEmulator
from SctMetaData import SctMetaData

from ListWidgetItemUserTypes import ListWidgetItemUserType

from SerialHandlerQObject import SerialHandlerQObject


class IdelmaApp(QApplication):
    """
    Class for the Idelma main App
    """
    def __init__(self, *args):
        super().__init__(*args)

        # Opening a serial port
        self.serialPort = None
        self.arduinoSerEmu = None
        self.openSerialPort()

        # Instantiating Back-end objects
        self.mcu = BoardMetaDatasQObject()
        self.ser = SerialHandlerQObject(self.serialPort)

        # Declaring another virtual arduino acting as a standard for comparison of unpushed changes
        self.mcuModsRef = BoardMetaDatas()

        # Instantiating and Declaring UI objects
        self.ui = IdelmaGui()

        # Creating an ItemType for QListWidgetItems that are non-serial sections metadatas
        self.NonSerSctMetaDataItemType = ListWidgetItemUserType.newUserType('Section Properties Type')

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
            self.arduinoSerEmu = ArduinoSerialEmulator(master)

    def assigningSlots(self):
        # Serial handler signals
        if self.arduinoSerEmu is not None:
            self.ser.connectNotifySignal(self.arduinoSerEmu.processSerialMssg)

        # Board metadatas signals
        self.mcu.connectSnSignal(self.ui.updtSnNumLabel)
        self.mcu.connectFwVerSignal(self.ui.updtFwVerLabel)
        self.mcu.connectSctsMgmtSignal(self.ui.updtSctsInfo)
        self.mcu.connectPxlsMgmtSignal(self.ui.updtPxlsInfo)

        # Fetch mcu infos button
        self.ui.fetchInfosButton.clicked.connect(self.fetchBrdMetaDatasCmd)

        # ListWidget signals and buttons
        self.ui.sctAddButton.clicked.connect(self.newSectionDialog)
        self.ui.sctDeleteButton.clicked.connect(self.deleteSectionDialog)
        self.ui.sctEditButton.clicked.connect(self.editSectionDialog)
        self.ui.sectionsList.itemClicked.connect(self.ui.enableListWidgetBttns)

        # Board config and save buttons
        self.ui.configButton.clicked.connect(self.configBrdCmd)
        self.ui.saveButton.clicked.connect(self.saveSettingsCmd)

        # Menu actions
        self.ui.actionReset_EEPROM.triggered.connect(self.resetEeprom)
        self.ui.actionAll_OFF.triggered.connect(self.allOff)

    def fetchBrdMetaDatasCmd(self):
        """
        Fetch all the metadata contained in the MCU and assign it to the mcu obj
        """
        # Board metadatas
        self.ser.serRqst(self.ser.serialRqsts.get("serial_num"), self.mcu.serialNumUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("fw_version"), self.mcu.fwVersionUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("scts_mgmt_metadata"), self.mcu.sctsMgmtUpdt)
        self.ser.serRqst(self.ser.serialRqsts.get("pxls_mgmt_metadata"), self.mcu.pxlsMgmtUpdt)

        # Other metadatas
        self.ser.serRqst(self.ser.serialRqsts.get("scts_metadata"), self.mcu.sctsMetaDataListUpdt)

        self.updtMcuModsRef()
        self.setMcuSavedConfig()

        self.ui.fetchInfosButton.setEnabled(False)
        self.ui.sctAddButton.setEnabled(True)

    def configBrdCmd(self):
        """
        Passes all the necessary info (metadata of each sections) to the serial Handler
        """
        self.ser.serRqst(self.ser.serialRqsts.get("config_board"), self.mcu.configBrd,
                         *self.metaDataCompare())

        self.configBrdBttnStateTrig()

        if not self.ui.saveButton.isEnabled():
            self.ui.saveButton.setEnabled(True)

    def saveSettingsCmd(self):
        """
        Save the last sent configuration in the MCU's EEPROM memory
        """
        self.ser.serRqst(self.ser.serialRqsts.get("save_settings"), self.mcu.ackConfirmed)

        self.ui.saveButton.setEnabled(False)

    def updtMcuModsRef(self):
        """
        Update the attr. of the virtual MCU used as mods reference
        """
        self.mcuModsRef.serialNum = self.mcu.serialNum
        self.mcuModsRef.fwVersion = self.mcu.fwVersion
        self.mcuModsRef.sctsMgmtMetaData = BrdMgmtMetaData(self.mcu.sctsMgmtMetaData.capacity,
                                                           self.mcu.sctsMgmtMetaData.remaining,
                                                           self.mcu.sctsMgmtMetaData.assigned)
        self.mcuModsRef.pxlsMgmtMetaData = BrdMgmtMetaData(self.mcu.pxlsMgmtMetaData.capacity,
                                                           self.mcu.pxlsMgmtMetaData.remaining,
                                                           self.mcu.pxlsMgmtMetaData.assigned)

    def setMcuSavedConfig(self):
        """
        Set the saved config of the physical MCU in the app
        by updating all necessary objs., objs's attr. & widgets
        """
        self.setAppSctsMetaData()

    def setAppSctsMetaData(self):
        """
        Update all that is related to the sections metadata
        in the app and its dependencies
        (sctsMetaDataList of mcuModsRef & QListWidget)
        """
        self.mcuModsRef.sctsMetaDataList = self.mcu.sctsMetaDataList.copy()
        for idx in range(0, self.mcuModsRef.sctsMgmtMetaData.assigned):
            NonSerSctMetaDataQListWidgetItem(NonSerSctMetaData.instWithDefaultName(idx).sctName,
                                             self.ui.sectionsList, self.NonSerSctMetaDataItemType)

    def resourcesAvailable(self):
        """
        Checks if there are remaining resources (sections & pixels)
        left for user assignation
        """
        if self.mcuModsRef.sctsMgmtMetaData.remaining and self.mcuModsRef.pxlsMgmtMetaData.remaining:
            return True
        else:
            return False

    def configBrdBttnStateTrig(self):
        """
        Compares virtual mcu with arduino to determine if
        necessary to enable or disable the 'config. mcu' bttn
        """
        if self.mcuModsRef != self.mcu and not self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(True)
        elif self.mcuModsRef == self.mcu and self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(False)

    def duplicateNameHandler(self, sct_metadata: SctMetaData, list_widget_item: NonSerSctMetaData):
        """
        Handle the action to take if a section to be created has been given a name that already exists

        Parameters:
            sct_metadata (SctMetaData): SctMetaData class object containing infos of previously dialog
            list_widget_item (NonSerSctMetaData): Contains all non-serial info related to section
        """
        if not list_widget_item.defaultNameCheck(sct_metadata.sctIdx) \
                and self.duplicateNameCheck(sct_metadata.sctIdx, list_widget_item.sctName):
            duplicate_res = self.duplicateNameDialog()
            if duplicate_res == 0:
                return self.newSectionDialog()
            elif duplicate_res == 1:
                sct_metadata.sctIdx = self.ui.sectionsList.currentRow()
                return self.sectionEdit(sct_metadata, list_widget_item)
            elif duplicate_res == 2:
                new_name = list_widget_item.sctName + ' (1)'
                while self.duplicateNameCheck(sct_metadata.sctIdx, new_name):
                    new_name = list_widget_item.sctName + ' (' + str(int(new_name[-2]) + 1) + ')'
                list_widget_item.sctName = new_name
        if self.ui.sectionsList.item(sct_metadata.sctIdx) is None:
            self.sectionCreation(sct_metadata, list_widget_item)
        else:
            self.sectionEdit(sct_metadata, list_widget_item)

    def duplicateNameCheck(self, check_sct_idx: int, check_sct_name: str):
        """
        Scan the existing sections and compares their name to the one whose name was
        passed as input argument

        Parameters:
            check_sct_idx (int): Section index of the section for which to pass the name check
                                 (to not compare it with itself in case of editing)
            check_sct_name (str): Name to compare with already assigned ones

        Return:
            A boolean indicating if a section with the same name already exists (True) or not (False)
        """
        list_widget_idx = 0
        while list_widget_idx < self.mcuModsRef.sctsMgmtMetaData.assigned:
            if list_widget_idx != check_sct_idx and \
                    self.ui.sectionsList.item(list_widget_idx).sctName == check_sct_name:
                self.ui.sectionsList.setCurrentRow(list_widget_idx)
                return True
            list_widget_idx += 1
        return False

    def metaDataCompare(self):
        """
        Compares the metadata of mcu obj and mcuModsRef obj to choose action accordingly
        """
        container = []
        for idx, sctMetaData_obj in enumerate(self.mcuModsRef.sctsMetaDataList[::-1]):
            try:
                if sctMetaData_obj != self.mcu.sctsMetaDataList[sctMetaData_obj.sctIdx]:
                    if not sctMetaData_obj.pixelCount:
                        container.append((self.mcu.configBrdSubCmdsKeys.index('delete_sct'),
                                          self.mcuModsRef.sctMetaDataTupleFormat(sctMetaData_obj.sctIdx)))
                        self.mcuModsRef.sctsMetaDataList.remove(sctMetaData_obj)
                    else:
                        container.append((self.mcu.configBrdSubCmdsKeys.index('edit_sct'),
                                          self.mcuModsRef.sctMetaDataTupleFormat(sctMetaData_obj.sctIdx)))
            except IndexError:
                container.append((self.mcu.configBrdSubCmdsKeys.index('create_sct'),
                                  self.mcuModsRef.sctMetaDataTupleFormat(sctMetaData_obj.sctIdx)))
        return container[::-1]

    def newSectionDialog(self):
        """
        Open the 'Section Configuration' dialog for user to create
        a new section
        """
        addSctDialog = IdelmaNewSctDialog(self.mcuModsRef.sctsMgmtMetaData.assigned,
                                          self.mcuModsRef.pxlsMgmtMetaData.remaining)
        addSctDialog.connectAccepted(self.duplicateNameHandler)
        addSctDialog.exec_()

    def editSectionDialog(self):
        """
        Open the 'Section Configuration' dialog w/ blanks filled w/
        infos of the selected section to be edited
        """
        edit_sct_idx = self.ui.sectionsList.currentRow()
        editSctDialog = IdelmaEditSctDialog(self.mcuModsRef.sctsMetaDataList[edit_sct_idx],
                                            self.ui.sectionsList.item(edit_sct_idx),
                                            self.mcuModsRef.pxlsMgmtMetaData.remaining)
        editSctDialog.connectAccepted(self.duplicateNameHandler)
        editSctDialog.exec_()

    def deleteSectionDialog(self):
        """
        Pop-up a warning dialog of the involvement of deleting
        a section and prompts the user to decline or accept
        """
        deleteSctDialog = IdelmaSctDelDialog()
        deleteSctDialog.connectAccepted(self.sectionDeletion)
        deleteSctDialog.exec_()

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

    def sectionCreation(self, sct_metadata: SctMetaData, list_widget_item: NonSerSctMetaData):
        """
        Handle the creation of a new section by updating applicable attributes and objects

        Parameters:
            sct_metadata (SctMetaData): SctMetaData class object containing info of previously accepted newSectionDialog
            list_widget_item (NonSerSctMetaData): Contains all non-serial info related to section
        """
        NonSerSctMetaDataQListWidgetItem(list_widget_item.sctName, self.ui.sectionsList, self.NonSerSctMetaDataItemType)
        self.mcuModsRef.addingSection(sct_metadata)

        # Buttons check
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

        self.configBrdBttnStateTrig()

    def sectionEdit(self, edit_sct_metadata: SctMetaData, edit_list_widget_item: NonSerSctMetaData):
        """
        Update the attributes of an edited section (if changes were made by the user)

        Parameters:
            edit_sct_metadata (SctMetaData): SctMetaData class object w/ infos of the previously accepted edit dialog
            edit_list_widget_item (NonSerSctMetaData): All non-serial info related to edited section
        """
        if edit_sct_metadata != self.mcuModsRef.sctsMetaDataList[edit_sct_metadata.sctIdx]:
            self.mcuModsRef.editingSection(edit_sct_metadata)
        if edit_list_widget_item != self.ui.sectionsList.currentItem():
            self.ui.sectionsList.takeItem(edit_sct_metadata.sctIdx)
            self.ui.sectionsList.insertItem(edit_sct_metadata.sctIdx,
                                            NonSerSctMetaDataQListWidgetItem(edit_list_widget_item.sctName, None,
                                                                             self.NonSerSctMetaDataItemType))

        # Buttons check
        if self.resourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.resourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

        self.configBrdBttnStateTrig()

    def sectionDeletion(self, dialog_check_state: bool = False):
        """
        Delete a user-chosen section after warning dialog has been accepted.
        Basically, every scts attr. coming after the deleted one are shifted.
        In practice, nothing is really deleted, only attributes are changed.

        Parameters:
            dialog_check_state (bool): State of the checkbox of the Warning Dialog
        """
        if dialog_check_state:
            self.ui.sctDeleteButton.clicked.disconnect()
            self.ui.sctDeleteButton.clicked.connect(self.sectionDeletion)

        sct_idx_iter = self.mcuModsRef.sctsMetaDataList[self.ui.sectionsList.currentRow()].sctIdx
        self.mcuModsRef.deletingSection(self.mcuModsRef.sctsMetaDataList[sct_idx_iter])

        while sct_idx_iter < self.mcuModsRef.sctsMgmtMetaData.assigned:
            if self.ui.sectionsList.item(sct_idx_iter + 1).defaultNameCheck(sct_idx_iter + 1):
                self.ui.sectionsList.item(sct_idx_iter).defaultNameSet(sct_idx_iter)
            else:
                self.ui.sectionsList.item(sct_idx_iter).sctName = \
                    self.ui.sectionsList.item(sct_idx_iter + 1).sctName
            self.ui.sectionsList.item(sct_idx_iter).setText()
            self.mcuModsRef.shiftSection(sct_idx_iter)
            sct_idx_iter += 1
        self.ui.sectionsList.takeItem(sct_idx_iter)

        if len(self.mcuModsRef.sctsMetaDataList) == len(self.mcu.sctsMetaDataList):
            self.mcuModsRef.clearSection(sct_idx_iter)
        else:
            self.mcuModsRef.sctsMetaDataList.pop(sct_idx_iter)

        # Buttons check
        if self.resourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.ui.sectionsList.count():
            self.ui.disableListWidgetBttns()
        self.configBrdBttnStateTrig()

    # // ** ** ** ** ** ** ** ** ** ** ** ** ** **  DEBUG  ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** //
    def resetEeprom(self):
        """
        Resets the EEPROM memory of the arduino (debug purposes)
        """
        self.ser.serRqst(self.ser.serialRqsts.get("reset_eeprom"), self.mcu.ackConfirmed)
        print('eeprom reset')

    def allOff(self):
        """
        Turn all pixels OFF
        """
        self.ser.serRqst(self.ser.serialRqsts.get("all_pixels_off"), self.mcu.ackConfirmed)
        print('All OFF')
    # // ** ** ** ** ** ** ** ** ** ** ** ** ** **  DEBUG  ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** //
