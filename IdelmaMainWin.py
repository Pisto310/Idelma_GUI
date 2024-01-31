from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFormLayout, QPushButton, QVBoxLayout,
                             QHBoxLayout, QListWidget, QFrame, QMenuBar, QMenu, QAction, QStatusBar, QTabWidget,
                             QBoxLayout, QColorDialog, QComboBox, QSizePolicy, QTableWidget, QGridLayout, QToolBar)
from PyQt5.QtCore import (Qt, QSize, QRect, QLocale, QMetaObject, QCoreApplication, QEvent, QObject)
from PyQt5.QtGui import (QFont)


class IdelmaMainWin(QMainWindow):
    """
    Create the main window of the Idelma Application.
    No functionalities, only a "shell"
    """
    def __init__(self):
        super().__init__()

        self.winSize_x = 1100
        self.winSize_y = 517

        self.centralWidget = QWidget(self)

        self.mainHLayoutWdgt = QWidget(self.centralWidget)
        self.mainHLayout = QHBoxLayout(self.mainHLayoutWdgt)

        self.mainTab = QTabWidget(self.mainHLayoutWdgt)
        self.lineVTabToColor = QFrame(self.mainHLayoutWdgt)
        self.colorPickerWdgt = QWidget(self.mainHLayoutWdgt)

        self.addressingTab = QWidget()
        self.addrTabHLayoutWdgt = QWidget(self.addressingTab)
        self.addrTabHLayout = QHBoxLayout(self.addrTabHLayoutWdgt)

        self.sctListAndBttnsWdgt = QWidget(self.addrTabHLayoutWdgt)
        self.sectionsList = QListWidget(self.sctListAndBttnsWdgt)
        self.sctAddButton = QPushButton(self.sctListAndBttnsWdgt)
        self.sctDeleteButton = QPushButton(self.sctListAndBttnsWdgt)
        self.sctEditButton = QPushButton(self.sctListAndBttnsWdgt)

        self.lineVListToInfo = QFrame(self.addrTabHLayoutWdgt)

        self.infosAndProgBttnsVLayout = QVBoxLayout()
        self.brdInfosMainVLayout = QVBoxLayout()

        self.snNumberVLayout = QVBoxLayout()
        self.snIdLabel = QLabel(self.addrTabHLayoutWdgt)
        self.snNumberLabel = QLabel(self.addrTabHLayoutWdgt)
        self.fwVersionLayout = QVBoxLayout()
        self.fwVerIdLabel = QLabel(self.addrTabHLayoutWdgt)
        self.fwVerLabel = QLabel(self.addrTabHLayoutWdgt)
        self.sectionsLayout = QVBoxLayout()
        self.sctsIdLabel = QLabel(self.addrTabHLayoutWdgt)
        self.sctsLabel = QLabel(self.addrTabHLayoutWdgt)
        self.pixelsLayout = QVBoxLayout()
        self.pxlsIdLabel = QLabel(self.addrTabHLayoutWdgt)
        self.pxlsLabel = QLabel(self.addrTabHLayoutWdgt)

        self.fetchBttnHLayout = QHBoxLayout()
        self.fetchInfosButton = QPushButton(self.addrTabHLayoutWdgt)

        self.lineHInfoToConfig = QFrame(self.addrTabHLayoutWdgt)

        self.boardProgVLayout = QVBoxLayout()
        self.configButton = QPushButton(self.addrTabHLayoutWdgt)
        self.saveButton = QPushButton(self.addrTabHLayoutWdgt)

        self.mappingTab = QWidget()
        self.mapTabVLayoutWdgt = QWidget(self.mappingTab)
        self.mapTabVLayout = QVBoxLayout(self.mapTabVLayoutWdgt)

        self.sctSelectFLayout = QFormLayout()
        self.sctSelectLabel = QLabel(self.mapTabVLayoutWdgt)
        self.sctSelectComboBox = QComboBox(self.mapTabVLayoutWdgt)
        self.lineHSelectToMap = QFrame(self.mapTabVLayoutWdgt)
        self.pxlsMapTable = QTableWidget(self.mapTabVLayoutWdgt)

        self.colorPickerHLayout = QHBoxLayout(self.colorPickerWdgt)
        self.colorPicker = QColorDialog()

        self.menuBar = QMenuBar(self)
        self.menuFile = QMenu(self.menuBar)
        self.menuEdit = QMenu(self.menuBar)
        self.menuWindow = QMenu(self.menuBar)
        self.menuDebug = QMenu(self.menuBar)

        self.actionDebug = QAction(self)
        self.actionReset_EEPROM = QAction(self)
        self.actionAll_OFF = QAction(self)

        self.statusBar = QStatusBar(self)

        self.setupUi()
        self.retranslateUi()

    def setGeometries(self):
        """
        Set the geometry of multiple widgets and layouts
        """
        self.mainHLayoutWdgt.setGeometry(QRect(-1, -1, self.winSize_x, (self.winSize_y - 26)))

        self.addrTabHLayoutWdgt.setGeometry(QRect(-1, -1, 471, (self.winSize_y - 26)))
        self.sectionsList.setGeometry(QRect(5, 5, 240, (self.winSize_y - 66)))
        self.sctAddButton.setGeometry(QRect(-1, (self.winSize_y - 66), 50, 42))
        self.sctDeleteButton.setGeometry(QRect(35, (self.winSize_y - 66), 50, 42))
        self.sctEditButton.setGeometry(QRect(71, (self.winSize_y - 66), 180, 42))

        self.mapTabVLayoutWdgt.setGeometry(QRect(9, -1, 461, 481))

        self.menuBar.setGeometry(QRect(0, 0, 1012, 24))

    def setMargins(self):
        """
        Set the margin for all layouts of the window
        """
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.colorPickerHLayout.setContentsMargins(0, 0, 0, 0)

        self.addrTabHLayout.setContentsMargins(0, 0, 0, 0)
        self.infosAndProgBttnsVLayout.setContentsMargins(0, 5, -1, 5)
        self.brdInfosMainVLayout.setContentsMargins(0, -1, -1, 0)
        self.fetchBttnHLayout.setContentsMargins(25, -1, 25, -1)
        self.boardProgVLayout.setContentsMargins(25, 12, 25, 12)

        self.mapTabVLayout.setContentsMargins(3, 6, 3, 0)
        self.sctSelectFLayout.setContentsMargins(10, 6, 10, 3)

    def setStretches(self):
        """
        Set appropriate stretch values for required layouts
        """
        self.customStretch(self.mainHLayout, (100, 1, 118))
        self.customStretch(self.addrTabHLayout, (50, 1, 40))
        self.customStretch(self.infosAndProgBttnsVLayout, (60, 5, 5, 30))
        self.customStretch(self.mapTabVLayout, (10, 1, 189))

    def setFonts(self):
        """
        All fonts of QLabel Wdgts are set here
        """
        self.sctAddButton.setFont(self.customFont(point_size=22, weight=75, bold=True))
        self.sctDeleteButton.setFont(self.customFont(point_size=22, weight=75, bold=True))
        self.sctEditButton.setFont(self.customFont(point_size=18, weight=50))
        self.sctSelectLabel.setFont(self.customFont(point_size=14, italic=True))

    def setFramesAndLines(self):
        """
        Frames (and lines also) are set in this method
        """
        self.customFrame(self.sectionsList, shape=QFrame.Box, shadow=QFrame.Raised)
        self.customFrame(self.lineVListToInfo, shape=QFrame.VLine, shadow=QFrame.Sunken)
        self.customFrame(self.lineHInfoToConfig, shape=QFrame.HLine, shadow=QFrame.Sunken)
        self.customFrame(self.lineHSelectToMap, shape=QFrame.HLine, shadow=QFrame.Sunken)
        self.customFrame(self.pxlsMapTable, shape=QFrame.Box, shadow=QFrame.Raised, width=2)
        self.customFrame(self.lineVTabToColor, shape=QFrame.VLine, shadow=QFrame.Raised, width=2)

    def setTab(self):
        """
        Set the tab widget of the window
        """
        self.mainTab.setTabPosition(QTabWidget.West)
        self.mainTab.setTabShape(QTabWidget.Rounded)
        self.mainTab.setElideMode(Qt.ElideMiddle)
        self.mainTab.setDocumentMode(True)

    def setBrdInfosZone(self, sub_v_layout: QVBoxLayout, info_id_label: QLabel, info_val_label: QLabel):
        """
        Set-up each zone of the mcu information

        Parameters:
            sub_v_layout (QVBoxLayout): parent layout for the QLabels to be inserted. Sub Layout to brdInfosMainVLayout
            info_id_label (QLabel): Information identification label
            info_val_label (QLabel): Information id. associated value
        """
        # Preparing the label that is used to identify the value of the label beneath
        info_id_label.setFont(self.customFont(point_size=20, weight=50, underline=True))
        info_id_label.setAlignment(Qt.AlignCenter)

        # Prepping the label showing the info coming from the mcu
        info_val_label.setFont(self.customFont(italic=True))
        info_val_label.setAlignment(Qt.AlignCenter)

        # Adding widgets to sub-layout
        sub_v_layout.addWidget(info_id_label)
        sub_v_layout.addWidget(info_val_label)
        sub_v_layout.setContentsMargins(-1, -1, -1, 12)

        # Inserting sub-layout into a parent layout
        self.brdInfosMainVLayout.addLayout(sub_v_layout)

    def setupUi(self):
        """
        Main set-up for the UI is done in this method. This include
        calling other 'set methods', adding widgets, layouts and tabs
        and managing size policies among many things
        """
        self.resize(self.winSize_x, self.winSize_y)

        self.mainHLayout.addWidget(self.mainTab)
        self.mainHLayout.addWidget(self.lineVTabToColor)
        self.mainHLayout.addWidget(self.colorPickerWdgt)

        self.mainTab.addTab(self.addressingTab, "")
        self.mainTab.addTab(self.mappingTab, "")
        self.mainTab.setCurrentIndex(0)

        self.sctAddButton.setMaximumSize(QSize(50, 16777215))
        self.sctDeleteButton.setMaximumSize(QSize(50, 16777215))

        self.addrTabHLayout.addWidget(self.sctListAndBttnsWdgt)
        self.addrTabHLayout.addWidget(self.lineVListToInfo)
        self.addrTabHLayout.addLayout(self.infosAndProgBttnsVLayout)

        self.infosAndProgBttnsVLayout.addLayout(self.brdInfosMainVLayout)
        self.infosAndProgBttnsVLayout.addLayout(self.fetchBttnHLayout)
        self.infosAndProgBttnsVLayout.addWidget(self.lineHInfoToConfig)
        self.infosAndProgBttnsVLayout.addLayout(self.boardProgVLayout)

        self.setBrdInfosZone(self.snNumberVLayout, self.snIdLabel, self.snNumberLabel)
        self.setBrdInfosZone(self.fwVersionLayout, self.fwVerIdLabel, self.fwVerLabel)
        self.setBrdInfosZone(self.sectionsLayout, self.sctsIdLabel, self.sctsLabel)
        self.setBrdInfosZone(self.pixelsLayout, self.pxlsIdLabel, self.pxlsLabel)

        self.fetchBttnHLayout.addWidget(self.fetchInfosButton)

        self.boardProgVLayout.addWidget(self.configButton)
        self.boardProgVLayout.addWidget(self.saveButton)

        self.mapTabVLayout.addLayout(self.sctSelectFLayout)
        self.mapTabVLayout.addWidget(self.lineHSelectToMap)
        self.mapTabVLayout.addWidget(self.pxlsMapTable)

        self.sctSelectFLayout.setWidget(0, QFormLayout.LabelRole, self.sctSelectLabel)
        self.sctSelectFLayout.setWidget(0, QFormLayout.FieldRole, self.sctSelectComboBox)
        self.sctSelectFLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.sctSelectFLayout.setHorizontalSpacing(90)
        self.sctSelectComboBox.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.colorPicker.setOptions(QColorDialog.NoButtons | QColorDialog.DontUseNativeDialog)
        self.colorPickerHLayout.addWidget(self.colorPicker)

        self.setCentralWidget(self.centralWidget)

        self.setGeometries()
        self.setMargins()
        self.setStretches()
        self.setFonts()
        self.setFramesAndLines()
        self.setTab()

        self.menuBar.setNativeMenuBar(True)
        self.menuDebug.addAction(self.actionReset_EEPROM)
        self.menuDebug.addAction(self.actionAll_OFF)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuWindow.menuAction())
        self.menuBar.addAction(self.menuDebug.menuAction())
        self.setMenuBar(self.menuBar)

        self.setStatusBar(self.statusBar)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        """
        Translate and set texts for all necessary wdgts
        """
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Idelma"))

        self.mainTab.setTabText(self.mainTab.indexOf(self.addressingTab), _translate("MainWindow", "Addressing"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.mappingTab), _translate("MainWindow", "Pxls Mapping"))

        self.sctAddButton.setText(_translate("MainWindow", "+"))
        self.sctDeleteButton.setText(_translate("MainWindow", "-"))
        self.sctEditButton.setText(_translate("MainWindow", "Edit"))

        self.snIdLabel.setText(_translate("MainWindow", "Serial Number"))
        self.snNumberLabel.setText(_translate("MainWindow", "- Empty -"))
        self.fwVerIdLabel.setText(_translate("MainWindow", "FW Version"))
        self.fwVerLabel.setText(_translate("MainWindow", "- Empty -"))
        self.sctsIdLabel.setText(_translate("MainWindow", "Sections Available"))
        self.sctsLabel.setText(_translate("MainWindow", "- Empty -"))
        self.pxlsIdLabel.setText(_translate("MainWindow", "Pixels Available"))
        self.pxlsLabel.setText(_translate("MainWindow", "- Empty -"))

        self.fetchInfosButton.setText(_translate("MainWindow", "Fetch Infos"))

        self.configButton.setText(_translate("MainWindow", "Config. Board"))
        self.saveButton.setText(_translate("MainWindow", "Save Settings"))

        self.sctSelectLabel.setText(_translate("MainWindow", "Please Select a Section :"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuDebug.setTitle(_translate("MainWindow", "Debug"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionReset_EEPROM.setText(_translate("MainWindow", "Reset EEPROM"))
        self.actionAll_OFF.setText(_translate("MainWindow", "All OFF"))

    @staticmethod
    def customFrame(frame: QFrame, shape: QFrame.Shape, shadow: QFrame.Shadow, width: int = 1):
        """
        Call the right methods for QFrame wdgts to set
        a custom frame with desired attributes

        Parameters:
            frame (QFrame wdgt): QFrame widget of which to modify attributes
            shape (QFrame.Shape): Specific shape to set on 'frame' input param.
            shadow (QFrame.shadow): Specific shadow to set on 'frame' input param.
            width (int): Specific width to set on 'frame' input param. Set to '1' by default
        """
        frame.setFrameShape(shape)
        frame.setFrameShadow(shadow)
        frame.setLineWidth(width)

    @staticmethod
    def customStretch(layout: QBoxLayout, proportions: tuple):
        """
        Set the stretch factor with the given values of the 'proportion'
        tuple var. for all widgets contained in a layout

        Parameters:
            layout (QBoxLayout): QBoxLayout widget of which to set stretch to contained widgets
            proportions (tuple): A tuple of integers representing the proportions of space in
                                 the layout for each widget to occupy
        """
        for idx, prop in enumerate(proportions):
            layout.setStretch(idx, prop)

    @staticmethod
    def customFont(point_size: int = 13, weight: int = 50,
                   underline: bool = False, italic: bool = False, bold: bool = False,
                   kerning: bool = True):
        """
        Create a custom font object that is then returned with
        the aim of modifying a QLabel widget font

        Parameters:
            point_size (int): Point size of the font. Set to '13' by default
            weight (int): Weight of the font. Higher value make it look like Bold writing. Set to '50' by default
            underline (bool): Set underline On or Off
            italic (bool): Set italic On of Off
            bold (bool): Set bold On of Off
            kerning (bool): Set kerning On or Off. If On, more space is allowed btwn each char
        """
        font = QFont()
        font.setPointSize(point_size)
        font.setWeight(weight)
        font.setUnderline(underline)
        font.setItalic(italic)
        font.setBold(bold)
        font.setKerning(kerning)
        return font


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = IdelmaMainWin()
    ui.show()
    sys.exit(app.exec_())