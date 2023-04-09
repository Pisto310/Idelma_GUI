from PyQt5.QtWidgets import (QApplication, QListWidgetItem)

from IdelmaGui import IdelmaGui
from IdelmaSctDialog import IdelmaSctDialog
from IdelmaSctDelDialog import IdelmaSctDelDialog
from IdelmaSctEditDialog import IdelmaSctEditDialog

from BoardInfosQObject import BoardInfosQObject
from MutableBrdInfo import MutableBrdInfo
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

        # ListWidget signals and buttons
        self.ui.sctAddButton.clicked.connect(self.newSectionDialog)
        self.ui.sctDeleteButton.clicked.connect(self.sectionDeletion)
        self.ui.sctEditButton.clicked.connect(self.editSectionDialog)
        self.ui.sectionsList.itemClicked.connect(self.ui.enableListWidgetBttns)

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

        self.fillingSctPropList()

    def instantiateVrtlBrd(self):
        """
        Instantiates a BoardInfosQObject object and fills
        all its attr with the ones recently fetched
        from the actual MCU, thus creating a virtual brd
        """
        self.virtualBoard = BoardInfosQObject()
        self.virtualBoard.serialNum = self.arduino.serialNum
        self.virtualBoard.fwVersion = self.arduino.fwVersion
        self.virtualBoard.sctsBrdMgmt = MutableBrdInfo(self.arduino.sctsBrdMgmt.capacity,
                                                       self.arduino.sctsBrdMgmt.remaining,
                                                       self.arduino.sctsBrdMgmt.assigned)
        self.virtualBoard.pxlsBrdMgmt = MutableBrdInfo(self.arduino.pxlsBrdMgmt.capacity,
                                                       self.arduino.pxlsBrdMgmt.remaining,
                                                       self.arduino.pxlsBrdMgmt.assigned)

    def fillingSctPropList(self):
        """
        Fills the sctPropList with as much 'None type obj'
        as the section capacity of fetched board
        """
        counter = 0
        while counter < self.arduino.sctsBrdMgmt.capacity:
            self.sctPropList.append(None)
            counter += 1

    def ressourcesAvailable(self):
        """
        Checks if there are remaining resources (sections
        & pixels) left for user assignation
        Returns 'True' if there are sections AND pixels left
        Returns 'False' otherwise
        """
        if self.virtualBoard.sctsBrdMgmt.remaining and self.virtualBoard.pxlsBrdMgmt.remaining:
            return True
        else:
            return False

    def configBrdBttnStateTrig(self):
        """
        Compares virtual board with arduino. If they are
        equal, the 'config. board' bttn isn't disabled. If
        they aren't, the button is enabled
        """
        if self.virtualBoard != self.arduino and not self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(True)
        elif self.virtualBoard == self.arduino and self.ui.configButton.isEnabled():
            self.ui.configButton.setEnabled(False)

    def newSectionDialog(self):
        """
        Pop-up a dialog in which user has to enter the required
        info to create a new section. Once accepted by the user,
        there is a check on remaining board resources that decides
        if necessary to trigger the state of the 'Add sct' bttn
        """
        addSctDialog = IdelmaSctDialog(self.virtualBoard.sctsBrdMgmt.assigned, self.virtualBoard.pxlsBrdMgmt.remaining)
        addSctDialog.connectAccepted(self.sectionCreation)
        addSctDialog.exec_()

        # Calling method to see if necessary to trig state of 'config. board' bttn
        self.configBrdBttnStateTrig()

        # Buttons check
        if not self.ressourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

    def deleteSectionDialog(self):
        """
        Pop-up a warning dialog of the involvement of deleting
        a section and prompts the user to decline or accept
        """
        deleteSctDialog = IdelmaSctDelDialog()
        deleteSctDialog.connectAccepted(self.sectionDeletion)
        deleteSctDialog.exec_()

        # Buttons check
        if self.ressourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.ui.sectionsList.count():
            self.ui.disableListWidgetBttns()
        self.configBrdBttnStateTrig()

    def editSectionDialog(self):
        """
        TBD
        """
        sct_index = self.ui.sectionsList.currentRow()
        sct_name = self.sctPropList[sct_index].sctName
        pxl_count = self.sctPropList[sct_index].pxlCount
        editSctDialog = IdelmaSctDialog(sct_index, self.virtualBoard.pxlsBrdMgmt.remaining,
                                        sct_name, pxl_count)
        editSctDialog.connectAccepted(self.sectionEdit)
        editSctDialog.exec_()

        # Buttons check
        if self.ressourcesAvailable() and not self.ui.sctAddButton.isEnabled():
            self.ui.sctAddButton.setEnabled(True)
        if not self.ressourcesAvailable():
            self.ui.sctAddButton.setEnabled(False)

    def sectionCreation(self, section_name: str, pixel_count: int, set_default_name: bool):
        """
        Method used to create a new section by first creating a ListWidgetItem
        and adding it to the UI ListWidget, and then updating the virtual brd
        """
        sctPropObj = SctPropQListWidgetItem(section_name, pixel_count, set_default_name,
                                            self.ui.sectionsList, self.sctPropItemType)
        self.sctPropList[self.virtualBoard.sctsBrdMgmt.assigned] = sctPropObj
        self.virtualBoard.sctsBrdMgmt.blockAssignation(1)
        self.virtualBoard.pxlsBrdMgmt.blockAssignation(pixel_count)

    def sectionDeletion(self):
        """

        MAKE DESCRITPION SHORTER

        Method called when wanting to delete a created section.
        User is prompted with a warning pop-up to either accept
        or cancel action. Then, section is deleted and default
        named section are renamed according to their index in
        the sectionPropList which changes because of the del.
        Existing scts are shifted accordingly, so no blank spaces
        """
        sct_index = self.ui.sectionsList.currentRow()
        pixels = self.sctPropList[sct_index].pxlCount
        self.ui.sectionsList.takeItem(sct_index)

        while sct_index < self.virtualBoard.sctsBrdMgmt.assigned:
            self.sctPropList[sct_index] = self.sctPropList[sct_index + 1]
            if not self.sctPropList[sct_index] is None and self.sctPropList[sct_index].setDefaultName:
                self.sctPropList[sct_index].decrDefaultName()
                self.sctPropList[sct_index].setText()
            sct_index += 1

        self.virtualBoard.sctsBrdMgmt.blockReallocation(1)
        self.virtualBoard.pxlsBrdMgmt.blockReallocation(pixels)

    def sectionEdit(self, new_section_name: str, new_pixel_count: int, new_set_default_name: bool):
        """
        Method description here
        """
        sct_index = self.ui.sectionsList.currentRow()

        # Allocating or deallocating pixel ressources
        edited_sct = self.ui.sectionsList.takeItem(sct_index)
        self.virtualBoard.pxlsBrdMgmt.blockAssignation(new_pixel_count - edited_sct.pxlCount)

        # Creating a new sctPropObj with updated attr and adding it to the ListWidget and the sctPropList
        new_sctPropObj = SctPropQListWidgetItem(new_section_name, new_pixel_count, new_set_default_name,
                                                None, self.sctPropItemType)
        self.ui.sectionsList.insertItem(sct_index, new_sctPropObj)
        self.sctPropList[sct_index] = new_sctPropObj
