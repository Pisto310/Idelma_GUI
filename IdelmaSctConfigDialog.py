from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QLabel, QLineEdit, QSpinBox,
                             QPushButton, QSlider, QCheckBox, QDialogButtonBox, QApplication, QDialog, QWidget,
                             QSizePolicy, QFrame)
from PyQt5.QtCore import (Qt, QRect, QSize, QCoreApplication, QMetaObject)


class IdelmaSctConfigDialog(QDialog):
    def __init__(self):
        """
        Creates a dialog window for configuring new or existing sections
        """
        super().__init__()

        self.centralWidget = QWidget(self)

        self.mainVLayout = QVBoxLayout(self.centralWidget)
        self.widgetsGridLayout = QGridLayout()
        self.brightVLayout = QVBoxLayout()
        self.brightBttnsHLayout = QHBoxLayout()
        self.checkBoxHLayout = QHBoxLayout()

        self.sctNameLabel = QLabel(self.centralWidget)
        self.sctNameLineEdit = QLineEdit(self.centralWidget)
        self.pxlsCountLabel = QLabel(self.centralWidget)
        self.pxlsSpinBox = QSpinBox(self.centralWidget)
        self.brightnessLabel = QLabel(self.centralWidget)
        self.brightnessSlider = QSlider(self.centralWidget)
        self.brightnessValLabel = QLabel(self.centralWidget)
        self.brightnessPageStepDown = QPushButton(self.centralWidget)
        self.brightnessSingleStepDown = QPushButton(self.centralWidget)
        self.brightnessSingleStepUp = QPushButton(self.centralWidget)
        self.brightnessPageStepUp = QPushButton(self.centralWidget)
        self.sctAsPxlLabel = QLabel(self.centralWidget)
        self.singlePxlCheckBox = QCheckBox(self.centralWidget)

        self.buttonBox = QDialogButtonBox(self.centralWidget)

        self.formLayout = QFormLayout()

        self.setObjNames()
        self.setupUi()
        self.slotConnect()
        self.setWidgetsAttr()
        self.retranslateUi()

    def setObjNames(self):
        self.setObjectName("SectionSetupDialog")

        self.centralWidget.setObjectName("centralWidget")

        self.mainVLayout.setObjectName("mainVLayout")
        self.widgetsGridLayout.setObjectName("widgetsGridLayout")
        self.brightVLayout.setObjectName("brightVLayout")
        self.brightBttnsHLayout.setObjectName("brightBttnsHLayout")
        self.checkBoxHLayout.setObjectName("checkBoxHLayout")

        self.sctNameLabel.setObjectName("sctNameLabel")
        self.sctNameLineEdit.setObjectName("lineEdit")
        self.pxlsCountLabel.setObjectName("pxlsCountLabel")
        self.pxlsSpinBox.setObjectName("pxlsSpinBox")
        self.brightnessLabel.setObjectName("brightnessLabel")
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.brightnessValLabel.setObjectName("brightnessValLabel")
        self.brightnessPageStepDown.setObjectName("brightnessPageStepDown")
        self.brightnessSingleStepDown.setObjectName("brightnessSingleStepDown")
        self.brightnessSingleStepUp.setObjectName("brightnessSingleStepUp")
        self.brightnessPageStepUp.setObjectName("brightnessPageStepUp")
        self.sctAsPxlLabel.setObjectName("sctAsPxlLabel")

        self.buttonBox.setObjectName("buttonBox")

    def setupUi(self):
        # Resizing window
        self.resize(415, 225)

        # Setting central widget
        self.centralWidget.setGeometry(QRect(10, 10, 395, 210))

        # Settings layouts
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.addLayout(self.widgetsGridLayout)
        self.mainVLayout.addWidget(self.buttonBox)

        self.widgetsGridLayout.addWidget(self.sctNameLabel, 0, 0, 1, 1)
        self.widgetsGridLayout.addWidget(self.sctNameLineEdit, 0, 1, 1, 1)
        self.widgetsGridLayout.addWidget(self.pxlsCountLabel, 1, 0, 1, 1)
        self.widgetsGridLayout.addWidget(self.pxlsSpinBox, 1, 1, 1, 1)
        self.widgetsGridLayout.addWidget(self.brightnessLabel, 2, 0, 1, 1)
        self.widgetsGridLayout.addLayout(self.brightVLayout, 2, 1, 1, 1)
        self.widgetsGridLayout.addWidget(self.sctAsPxlLabel, 3, 0, 1, 1)
        self.widgetsGridLayout.addLayout(self.checkBoxHLayout, 3, 1, 1, 1)

        self.brightVLayout.addWidget(self.brightnessSlider)
        self.brightVLayout.addLayout(self.brightBttnsHLayout)
        self.brightBttnsHLayout.addWidget(self.brightnessPageStepDown)
        self.brightBttnsHLayout.addWidget(self.brightnessSingleStepDown)
        self.brightBttnsHLayout.addWidget(self.brightnessValLabel)
        self.brightBttnsHLayout.addWidget(self.brightnessSingleStepUp)
        self.brightBttnsHLayout.addWidget(self.brightnessPageStepUp)

        self.checkBoxHLayout.addWidget(self.singlePxlCheckBox)

        # Section Name label and associated LineEdit widget
        self.sctNameLineEdit.setMaxLength(20)

        # Pixel Count Label and associated SpinBox widget
        self.pxlsSpinBox.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pxlsSpinBox.sizePolicy().hasHeightForWidth())
        self.pxlsSpinBox.setSizePolicy(sizePolicy)
        self.pxlsSpinBox.setSizeIncrement(QSize(0, 0))
        self.pxlsSpinBox.setBaseSize(QSize(0, 0))
        self.pxlsSpinBox.setFont(self.fontSetter(kerning=True))
        self.pxlsSpinBox.setLayoutDirection(Qt.LeftToRight)
        self.pxlsSpinBox.setAlignment(Qt.AlignLeft | Qt.AlignTrailing | Qt.AlignVCenter)
        self.pxlsSpinBox.setMinimum(1)

        # Strip brightness Label and associated widgets
        self.brightnessSlider.setMaximum(255)
        self.brightnessSlider.setPageStep(25)
        self.brightnessSlider.setOrientation(Qt.Horizontal)
        self.brightnessSlider.setTickPosition(QSlider.NoTicks)
        self.brightnessValLabel.setFont(self.fontSetter(point_size=14, bold=True, weight=75))
        self.brightnessValLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.brightnessValLabel.setAutoFillBackground(True)
        self.brightnessValLabel.setFrameShape(QFrame.Box)
        self.brightnessValLabel.setFrameShadow(QFrame.Raised)
        self.brightnessValLabel.setLineWidth(1)
        self.brightnessPageStepDown.setFont(self.fontSetter(bold=True, weight=75))
        self.brightnessSingleStepDown.setFont(self.fontSetter(bold=True, weight=75))
        self.brightnessSingleStepUp.setFont(self.fontSetter(bold=True, weight=75))
        self.brightnessPageStepUp.setFont(self.fontSetter(bold=True, weight=75))

        # Strip controlled as a single pixel Label and Checkbox
        self.singlePxlCheckBox.setText("")

        # Setting the dialog ButtonBox
        self.buttonBox.setOrientation(Qt.Horizontal)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # Arranging formLayout and ButtonBox in a vertical grid Layout
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.addLayout(self.formLayout)
        self.mainVLayout.addWidget(self.buttonBox)

        # self.setTabOrder(self.sctNameLineEdit, self.pxlsSpinBox)

    def setWidgetsAttr(self):
        """
        Sets a number of widget attributes (max, min, placeholder text, etc.)
        To be implemented in children classes
        """
        pass

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SectionSetupDialog", "Section Configuration"))
        self.sctNameLabel.setText(_translate("SectionSetupDialog", "Section name:"))
        self.pxlsCountLabel.setText(_translate("SectionSetupDialog", "Pixels count:"))
        self.brightnessLabel.setText(_translate("SectionSetupDialog", "Brightness:"))
        self.brightnessValLabel.setText(_translate("SectionSetupDialog", str(self.brightnessSlider.value())))
        self.brightnessPageStepDown.setText(_translate("SectionSetupDialog", "<<"))
        self.brightnessSingleStepDown.setText(_translate("SectionSetupDialog", "<"))
        self.brightnessSingleStepUp.setText(_translate("SectionSetupDialog", ">"))
        self.brightnessPageStepUp.setText(_translate("SectionSetupDialog", ">>"))
        self.sctAsPxlLabel.setText(_translate("SectionSetupDialog", "Single Pxl Ctrl:"))

    def slotConnect(self):
        self.brightnessSlider.valueChanged.connect(self.updtBrightVal)
        self.brightnessPageStepDown.clicked.connect(self.sliderPageDown)
        self.brightnessPageStepUp.clicked.connect(self.sliderPageUp)
        self.brightnessSingleStepDown.clicked.connect(self.sliderUnitDown)
        self.brightnessSingleStepUp.clicked.connect(self.sliderUnitUp)
        self.singlePxlCheckBox.stateChanged.connect(self.checkBoxStateChanged)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #QMetaObject.connectSlotsByName(self)                       Not sure if needed... TBD

    def updtBrightVal(self):
        self.brightnessValLabel.setText(str(self.brightnessSlider.value()))

    def sliderPageDown(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() - self.brightnessSlider.pageStep())

    def sliderPageUp(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() + self.brightnessSlider.pageStep())

    def sliderUnitDown(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() - 1)

    def sliderUnitUp(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() + 1)

    def checkBoxStateChanged(self, new_state: int):
        """
        Handle what to do in real-time when the checkbox state has changed.
        Implemented in children classes
        """
        pass

    @staticmethod
    def fontSetter(point_size: int = 13, kerning: bool = False, bold: bool = False, italic: bool = False,
                   underline: bool = False, weight: int = 0):
        font = QFont()
        font.setKerning(kerning)
        font.setPointSize(point_size)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(underline)
        font.setWeight(weight)
        return font


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = IdelmaSctConfigDialog()
    ui.show()
    sys.exit(app.exec_())
