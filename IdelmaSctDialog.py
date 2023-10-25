from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLayout, QLabel, QLineEdit, QSpinBox, QDialogButtonBox,
                             QApplication, QDialog, QWidget, QSizePolicy)
from PyQt5.QtCore import (Qt, QRect, QSize, QCoreApplication, pyqtSignal, QMetaObject)


class IdelmaSctDialog(QDialog):
    """
    Dialog that pops-up when user asks to create a new section
    Inputs:
        - scts_assigned: sections actually assigned (Used as an id)
        - pxls_remaining: remaining available pixel to map

    Outputs (as an emitted signal to connect to a slot):
        - str: section name given by the user
        - int: number of pixels in section
    """

    accepted = pyqtSignal(str, int, bool, name='Returning user inputs')
    # indexTracker = 0
    # defaultName = "Section " + str(indexTracker)

    def __init__(self, sct_index: int, pxls_remaining: int, sct_name: str = "", pxl_count: int = 0):
        super().__init__()

        self.maxPxls = pxls_remaining
        self.defaultName = "Section " + str(sct_index)
        self.setDefault = False
        self.sctName = sct_name
        self.pxlCount = pxl_count

        self.setupUi()
        self.retranslateUi()
        self.slotConnect()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(280, 120)

        # Creating central widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setGeometry(QRect(10, 10, 250, 100))
        self.centralWidget.setObjectName("widget")

        # Section Name label and associated LineEdit widget
        self.sctNameLabel = QLabel(self)
        self.sctNameLabel.setObjectName("sctNameLabel")
        self.sctNameLineEdit = QLineEdit(self)
        self.sctNameLineEdit.setPlaceholderText(self.defaultName)
        self.sctNameLineEdit.setText(self.sctName)
        self.sctNameLineEdit.setMaxLength(20)
        self.sctNameLineEdit.setObjectName("lineEdit")

        # Pixel Number Label and associated SpinBox widget
        self.pxlsNbrLabel = QLabel(self)
        self.pxlsNbrLabel.setObjectName("pxlsNbrLabel")
        self.pxlsSpinBox = QSpinBox(self)
        self.pxlsSpinBox.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pxlsSpinBox.sizePolicy().hasHeightForWidth())
        self.pxlsSpinBox.setSizePolicy(sizePolicy)
        self.pxlsSpinBox.setSizeIncrement(QSize(0, 0))
        self.pxlsSpinBox.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(13)
        font.setKerning(True)
        self.pxlsSpinBox.setFont(font)
        self.pxlsSpinBox.setLayoutDirection(Qt.LeftToRight)
        self.pxlsSpinBox.setAlignment(Qt.AlignLeft|Qt.AlignTrailing|Qt.AlignVCenter)
        self.pxlsSpinBox.setMinimum(1)
        self.pxlsSpinBox.setMaximum(self.pxlCount + self.maxPxls)
        self.pxlsSpinBox.setValue(self.pxlCount)
        self.pxlsSpinBox.setObjectName("pxlsSpinBox")

        # Arranging previously created widgets in a FormLayout
        self.formLayout = QFormLayout()
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.sctNameLabel)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sctNameLineEdit)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.pxlsNbrLabel)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pxlsSpinBox)

        # Setting the dialog ButtonBox
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Arranging formLayout and ButtonBox in a vertical grid Layout
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.buttonBox)

        self.setTabOrder(self.sctNameLineEdit, self.pxlsSpinBox)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Section Config"))
        self.sctNameLabel.setText(_translate("Dialog", "Section name:"))
        self.pxlsNbrLabel.setText(_translate("Dialog", "Pixels number:"))

    def slotConnect(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #QMetaObject.connectSlotsByName(self)                       Not sure if needed... TBD

    def accept(self):
        super().accept()
        if self.sctNameLineEdit.text() == "":
            self.sctName = self.defaultName
            self.setDefault = True
        else:
            self.sctName = self.sctNameLineEdit.text()
        self.pxlCount = self.pxlsSpinBox.value()
        self.accepted.emit(self.sctName, self.pxlCount, self.setDefault)

    def connectAccepted(self, callback):
        self.accepted.connect(callback)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaSctDialog(0, 100, "Soleil", 24)
    ui.show()
    sys.exit(app.exec_())
