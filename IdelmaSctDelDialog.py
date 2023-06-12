from IdelmaWarningDialog import IdelmaWarningDialog

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (QCoreApplication, pyqtSignal)


class IdelmaSctDelDialog(IdelmaWarningDialog):
    """
    Pop-up dialog for when user wants
    to delete a created section
    """
    results = pyqtSignal(int, name='Dialog\'s widgets result')

    def __init__(self):
        self.confirmAction = "delete section"
        self.furtherInfo = "Doing so will shift position of further sections by one.  " \
                           "This will result in a renaming if using default names.  " \
                           "Indexing will also change to reflect the removal."
        super().__init__()

    def winSize(self):
        self.win_x = 300
        self.win_y = 250
        self.resize(self.win_x, self.win_y)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Warning"))
        self.warningTitle.setText(_translate("Dialog", "Are you sure you want to {}?".format(self.confirmAction)))
        self.warningMssg.setText(_translate("Dialog", self.furtherInfo))

    def accept(self):
        super().accept()
        self.results.emit(self.hideMssgCheckBox.isChecked())

    def connectAccepted(self, callback):
        self.results.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaSctDelDialog()
    ui.show()
    sys.exit(app.exec_())
