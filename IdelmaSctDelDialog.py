from IdelmaWarningDialog import IdelmaWarningDialog

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication


class IdelmaSctDelDialog(IdelmaWarningDialog):
    """
    Pop-up dialog for when user wants
    to delete a created section
    """

    def __init__(self):
        self.confirmAction = "delete section"
        self.furtherInfo = "Doing so will shift position of further sections by one.  " \
                           "This will result in a renaming if using default name.  " \
                           "Indexing will also change to reflect the removal."
        super().__init__()

    def winSize(self):
        self.win_x = 300
        self.win_y = 210
        self.resize(self.win_x, self.win_y)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Warning"))
        self.warningTitle.setText(_translate("Dialog", "Are you sure you want to {}?".format(self.confirmAction)))
        self.warningMssg.setText(_translate("Dialog", self.furtherInfo))

    # def test(self):
    #     self.resize(240, 200)
    #     self.centralWidget.setGeometry(10, 0, 230, 190)
    #     widj = QLabel("This is a test")
    #     self.verticalLayout.insertWidget(len(self.verticalLayout)-1, widj)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaSctDelDialog()
    ui.show()
    sys.exit(app.exec_())
