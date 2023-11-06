from IdelmaSctConfigDialog import IdelmaSctConfigDialog
from NonSerSctMetaData import NonSerSctMetaData
from NonSerSctMetaDataQListWidgetItem import NonSerSctMetaDataQListWidgetItem
from SctMetaData import SctMetaData

from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import (pyqtSignal)


class IdelmaEditSctDialog(IdelmaSctConfigDialog):

    accepted = pyqtSignal(SctMetaData, NonSerSctMetaData, name='dialog_modified_user_inputs')

    def __init__(self, sct_metadata: SctMetaData, list_widget_item: NonSerSctMetaData,
                 pxls_remaining: int):
        """
        Dialog that pops-up when user asks to create a new section

        Parameters:
            sct_metadata (SctMetaData): SctMetaData class object containing info of section being edited
            list_widget_item (NonSerSctMetaDataQListWidgetItem): All non-serial info related to section being edited
            pxls_remaining (int): Remaining pixels available for assignment

        Return (a pyqt signal containing the following variables):
            SctSerialData_obj (SctMetaData);
            sct_name (str);
        """
        self.maxPxls = pxls_remaining
        self.sctMetaData = sct_metadata
        self.listWidgetItem = list_widget_item

        self.setMaxPxlCount
        super().__init__()

    def setMaxPxlCount(self):
        """
        Set the maximum possible pixel count that the user can enter in
        the pixel count spinbox field
        """
        if self.sctMetaData.singlePxlCtrl:
            self.maxPxls += self.sctMetaData.singlePxlCtrl
        else:
            self.maxPxls += self.sctMetaData.pixelCount

    def setWidgetsAttr(self):
        self.sctNameLineEdit.setText(self.listWidgetItem.sctName)
        self.pxlsSpinBox.setValue(self.sctMetaData.pixelCount)
        self.brightnessSlider.setSliderPosition(self.sctMetaData.brightness)
        self.singlePxlCheckBox.setChecked(self.sctMetaData.singlePxlCtrl)
        # self.pxlsSpinBox.setMaximum(self.maxPxls)

    def checkBoxStateChanged(self, new_state: int):
        if new_state:
            self.pxlsSpinBox.setMaximum(100)
        else:
            self.pxlsSpinBox.setMaximum(self.maxPxls)

    def accept(self):
        super().accept()
        if self.sctNameLineEdit.text() == "":
            edited_listWidgetItem = NonSerSctMetaData(self.listWidgetItem.sctName)
        else:
            edited_listWidgetItem = NonSerSctMetaData(self.sctNameLineEdit.text())
        edited_sctMetaData = SctMetaData(self.sctMetaData.sctIdx,
                                         self.pxlsSpinBox.value(),
                                         self.brightnessSlider.value(),
                                         int(self.singlePxlCheckBox.isChecked()))

        self.accepted.emit(edited_sctMetaData, edited_listWidgetItem)

    def connectAccepted(self, callback):
        self.accepted.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaEditSctDialog(0, 100)
    ui.show()
    sys.exit(app.exec_())
