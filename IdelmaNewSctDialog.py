from IdelmaSctConfigDialog import IdelmaSctConfigDialog
from NonSerSctMetaDataQListWidgetItem import NonSerSctMetaDataQListWidgetItem
from SctMetaData import SctMetaData

from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import (pyqtSignal)


class IdelmaNewSctDialog(IdelmaSctConfigDialog):

    accepted = pyqtSignal(SctMetaData, NonSerSctMetaDataQListWidgetItem, name='dialog_accepted_user_inputs')

    def __init__(self, sct_index: int, pxls_remaining: int):
        """
        Dialog that pops-up when user asks to create a new section

        Parameters:
            sct_index (int): The ID of the section being created
            pxls_remaining (int): Remaining pixels available for assignment

        Return (a pyqt signal containing the following variables):
            SctSerialData_obj (SctMetaData)
            NonSerSctMetaDataQListWidgetItem_obj (NonSerSctMetaDataQListWidgetItem)
        """
        self.maxPxls = pxls_remaining
        self.sctMetaData = SctMetaData(sct_index)
        self.listWidgetItem = NonSerSctMetaDataQListWidgetItem.instWithDefaultName(sct_index)

        super().__init__()

    def setWidgetsAttr(self):
        self.sctNameLineEdit.setPlaceholderText(self.listWidgetItem.sctName)
        self.brightnessSlider.setSliderPosition(self.sctMetaData.brightness)
        self.pxlsSpinBox.setMaximum(self.maxPxls)

    def checkBoxStateChanged(self, new_state: int):
        if new_state:
            self.pxlsSpinBox.setMaximum(100)
        else:
            self.pxlsSpinBox.setMaximum(self.maxPxls)

    def accept(self):
        super().accept()
        if self.sctNameLineEdit.text() != "":
            self.listWidgetItem.sctName = self.sctNameLineEdit.text()
        self.sctMetaData = SctMetaData(self.sctMetaData.sctIdx,
                                       self.pxlsSpinBox.value(),
                                       self.brightnessSlider.value(),
                                       int(self.singlePxlCheckBox.isChecked()))
        self.listWidgetItem.updtPxlsMetaDataList(self.sctMetaData.pxlHeapBlocksCount())

        self.accepted.emit(self.sctMetaData, self.listWidgetItem)

    def connectAccepted(self, callback):
        self.accepted.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaNewSctDialog(0, 100)
    ui.show()
    sys.exit(app.exec_())
