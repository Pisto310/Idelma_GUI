from math import floor

from IdelmaWarningDialog import IdelmaWarningDialog

from PyQt5.QtWidgets import (QApplication, QPushButton, QDialogButtonBox)
from PyQt5.QtCore import QCoreApplication


class IdelmaDuplicateNameDialog(IdelmaWarningDialog):
    """
    Warning dialog that pop-up when user tries to create
    a section with an already existing name
    """
    def __init__(self, existing_name):
        # self.confirmAction = "delete section"
        self.name = existing_name
        self.furtherInfo = "An existing section is already named \"{}\". " \
                           "Do you wish to replace it with the section you are " \
                           "currently creating?".format(self.name)
        super().__init__()
        self.removeWidgets()
        self.resizeMargins()

    def computeWinSizeY(self):
        """
        Sets the window Y size depending on length of name to display
        """
        chars_per_line = 30
        add_lines = floor(len(self.name) / chars_per_line)
        pxls_per_line = 14
        win_y_default = 150
        self.win_y = win_y_default + (pxls_per_line * add_lines)

    def winSize(self):
        self.win_x = 300
        self.computeWinSizeY()
        self.resize(self.win_x, self.win_y)

    def settingBttns(self):
        keepBttn = QPushButton("Keep both")
        self.buttonBox.addButton(keepBttn, QDialogButtonBox.ButtonRole.ApplyRole)
        self.buttonBox.addButton(QDialogButtonBox.No)
        self.buttonBox.addButton(QDialogButtonBox.Yes)
        # self.buttonBox.setStandardButtons(QDialogButtonBox.No | QDialogButtonBox.Yes)
        self.buttonBox.button(QDialogButtonBox.No).setDefault(True)

    def assigningSlots(self):
        self.buttonBox.accepted.connect(self.accept)
    #     self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Warning"))
        # self.warningTitle.setText(_translate("Dialog", "Are you sure you want to {}?".format(self.confirmAction)))
        self.warningMssg.setText(_translate("Dialog", self.furtherInfo))

    def removeWidgets(self):
        self.verticalLayout.removeWidget(self.warningTitle)
        self.verticalLayout.removeWidget(self.hideMssgCheckBox)
        del self.warningTitle
        del self.hideMssgCheckBox
        # self.warningTitle.deleteLater()
        # self.hideMssgCheckBox.deleteLater()

    def resizeMargins(self):
        self.verticalLayout.setContentsMargins(0, 20, 0, 0)
        self.warningMssg.setContentsMargins(7, 0, 7, 0)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaDuplicateNameDialog("Unnecessarily long name")
    # ui = IdelmaDuplicateNameDialog("Unnecessarily long name that does not make any sense whatsoever")
    # ui = IdelmaDuplicateNameDialog("Unnecessarily long name that does not make any sense whatsoever and that maybe keep on going until the end of time like the land before time")
    ui.show()
    sys.exit(app.exec_())
