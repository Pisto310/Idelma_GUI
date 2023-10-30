from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QLayout, QGridLayout, QLabel, QLineEdit, QSpinBox,
                             QPushButton, QSpacerItem, QSlider, QCheckBox, QDialogButtonBox, QApplication, QDialog,
                             QWidget, QSizePolicy, QFrame)
from PyQt5.QtCore import (Qt, QRect, QSize, QCoreApplication, pyqtSignal, QMetaObject)


class IdelmaSctDialog(QDialog):

    accepted = pyqtSignal(int, int, int, bool, str, bool, name='Returning user inputs')

    def __init__(self, sct_index: int, pxls_remaining: int, brightness: int = 50, strip_single_ctrl: bool = False,
                 pxl_count: int = 0, sct_name: str = ""):
        """
        Dialog that pops-up when user asks to create a new section or edit an existing one

        Parameters:
            sct_index (int): The ID of the section being created
            pxls_remaining (int): Remaining pixels (unassigned ones)
            brightness (int): Brightness level for the whole strip (set to 50 over 255 by default)
            strip_single_ctrl (bool): Indicates if the whole strip is to be controlled as a single pixel
            pxl_count (int): Actual pixel count in the section (set to 0 by default)
            sct_name (str): Name of the section for user ID purpose (set to empty by default)

        Return (a pyqt signal containing the following variables):
            sct_index (int);
            pxl_count (int);
            brightness (int);
            strip_single_pixel (bool);
            sct_name (str);
            set_default_name (bool)
        """
        super().__init__()

        self.maxPxls = pxls_remaining
        self.defaultName = "Section " + str(sct_index)
        self.setDefault = False
        self.sctIdx = sct_index
        self.pxlCount = pxl_count
        self.sctName = sct_name

        self.maxBrightness = 255
        self.brightness = brightness
        self.brightnessPageStepUnit = 25

        self.stripSinglePxl = strip_single_ctrl

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
        self.retranslateUi()
        self.slotConnect()

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
        # self.brightnessSpinBox.setObjectName("brightnessSpinBox")
        self.sctAsPxlLabel.setObjectName("sctAsPxlLabel")

        self.buttonBox.setObjectName("buttonBox")

    def setupUi(self):
        # Resizing whole window
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
        self.sctNameLineEdit.setPlaceholderText(self.defaultName)
        self.sctNameLineEdit.setText(self.sctName)
        self.sctNameLineEdit.setMaxLength(20)

        # Pixel Number Label and associated SpinBox widget
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
        self.pxlsSpinBox.setMaximum(self.pxlCount + self.maxPxls)
        self.pxlsSpinBox.setValue(self.pxlCount)

        # Strip brightness Label and associated widgets
        self.brightnessSlider.setMaximum(self.maxBrightness)
        self.brightnessSlider.setPageStep(self.brightnessPageStepUnit)
        self.brightnessSlider.setSliderPosition(self.brightness)
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
        self.singlePxlCheckBox.setChecked(self.stripSinglePxl)

        # Setting the dialog ButtonBox
        self.buttonBox.setOrientation(Qt.Horizontal)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Arranging formLayout and ButtonBox in a vertical grid Layout
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVLayout.setObjectName("mainVLayout")
        self.mainVLayout.addLayout(self.formLayout)
        self.mainVLayout.addWidget(self.buttonBox)

        self.setTabOrder(self.sctNameLineEdit, self.pxlsSpinBox)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SectionSetupDialog", "Section Configuration"))
        self.sctNameLabel.setText(_translate("SectionSetupDialog", "Section name:"))
        self.pxlsCountLabel.setText(_translate("SectionSetupDialog", "Pixels number:"))
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
        self.brightnessSingleStepDown.clicked.connect(self.sliderUnitDown)
        self.brightnessSingleStepUp.clicked.connect(self.sliderUnitUp)
        self.brightnessPageStepUp.clicked.connect(self.sliderPageUp)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #QMetaObject.connectSlotsByName(self)                       Not sure if needed... TBD

    def updtBrightVal(self):
        self.brightnessValLabel.setText(str(self.brightnessSlider.value()))

    def sliderPageDown(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() - self.brightnessSlider.pageStep())

    def sliderUnitDown(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() - 1)

    def sliderUnitUp(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() + 1)

    def sliderPageUp(self):
        self.brightnessSlider.setValue(self.brightnessSlider.value() + self.brightnessSlider.pageStep())

    def accept(self):
        super().accept()
        if self.sctNameLineEdit.text() == "":
            self.sctName = self.defaultName
            self.setDefault = True
        else:
            self.sctName = self.sctNameLineEdit.text()
        self.pxlCount = self.pxlsSpinBox.value()
        self.brightness = self.brightnessSlider.value()
        self.stripSinglePxl = self.singlePxlCheckBox.isChecked()
        self.accepted.emit(self.sctIdx, self.pxlCount, self.brightness, self.stripSinglePxl,
                           self.sctName, self.setDefault)

    def connectAccepted(self, callback):
        self.accepted.connect(callback)

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
    ui = IdelmaSctDialog(0, 100, 79)
    # ui = IdelmaSctDialog(0, 100, "Soleil", 24)
    ui.show()
    sys.exit(app.exec_())
