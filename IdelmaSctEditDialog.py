from IdelmaSctDialog import IdelmaSctDialog

from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLayout, QLabel, QLineEdit, QSpinBox, QDialogButtonBox,
                             QApplication, QDialog, QWidget, QSizePolicy)
from PyQt5.QtCore import (Qt, QRect, QSize, QCoreApplication, pyqtSignal, QMetaObject)


class IdelmaSctEditDialog(IdelmaSctDialog):
    """
    Dialog that pops-up when user wants to edit existing section
    Same dialog as when creating, but fields are filled with actual attr
    Inputs:
        - sct_name: Name of the section according
        - pxl_count: Number of pixels assigned to the section
        - sct_index: Index of the section (in the sctPropList of App class)
        - pxls_remaining: Remaining available pixel to map

    Outputs (as an emitted signal to connect to a slot):
        A DICT containing only the attr. that have changed
        Appearing in the following order:
            - str: Section name given by the user
            - int: Number of pixels in section
            - bool: Indicates if default name is set
    """

    acceptMods = pyqtSignal(object, name='Section Edit Dialog Infos')

    def __init__(self, sct_name: str, pxl_count: int, sct_index: int, pxls_remaining: int):
        super().__init__(sct_index=sct_index, pxls_remaining=pxls_remaining)

        self.sctName = sct_name
        self.pxlCount = pxl_count
        self.sctIndex = sct_index

        self.modifiedAttr = {}

        self.updateUserWidgets()
        self.slotConnect()

    def updateUserWidgets(self):
        """
        Just displaying actual attributes values in
        the Dialog's widgets
        """
        self.sctNameLineEdit.setText(self.sctName)
        self.pxlsSpinBox.setValue(self.pxlCount)

    def slotConnect(self):
        super().slotConnect()
        self.sctNameLineEdit.editingFinished.connect(self.updateName)
        self.pxlsSpinBox.valueChanged.connect(self.updateCount)

    def updateName(self):
        self.sctName = self.sctNameLineEdit.text()

    def updateCount(self, new_count):
        self.pxlCount = new_count

    def accept(self):
        super().accept()
        self.acceptMods.emit(self)

    def connectAcceptChanges(self, callback):
        self.acceptMods.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaSctEditDialog("Test", 5, 0, 95)
    ui.show()
    sys.exit(app.exec_())
