from IdelmaSctConfigDialog import IdelmaSctConfigDialog
from NonSerSctMetaData import NonSerSctMetaData
from SctMetaData import SctMetaData

from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import (pyqtSignal)


class IdelmaNewSctDialog(IdelmaSctConfigDialog):

    accepted = pyqtSignal(SctMetaData, NonSerSctMetaData, name='dialog_accepted_user_inputs')

    def __init__(self, sct_index: int, pxls_remaining: int):
        """
        Dialog that pops-up when user asks to create a new section

        Parameters:
            sct_index (int): The ID of the section being created
            pxls_remaining (int): Remaining pixels available for assignment

        Return (a pyqt signal containing the following variables):
            SctSerialData_obj (SctMetaData);
            NonSerSctMetaData_obj (NonSerSctMetaData);
        """
        self.maxPxls = pxls_remaining
        self.sctMetaData = SctMetaData(sct_index)
        self.nonSerSctMetaData = NonSerSctMetaData.instWithDefaultName(sct_index)

        super().__init__()

    def setWidgetsAttr(self):
        self.sctNameLineEdit.setPlaceholderText(self.nonSerSctMetaData.sctName)
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
            self.nonSerSctMetaData.sctName = self.sctNameLineEdit.text()
        self.sctMetaData.pixelCount = self.pxlsSpinBox.value()
        self.sctMetaData.brightness = self.brightnessSlider.value()
        self.sctMetaData.singlePxlCtrl = int(self.singlePxlCheckBox.isChecked())

        self.accepted.emit(self.sctMetaData, self.nonSerSctMetaData)

    def connectAccepted(self, callback):
        self.accepted.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaNewSctDialog(0, 100)
    ui.show()
    sys.exit(app.exec_())
