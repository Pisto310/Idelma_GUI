from BoardInfosQObject import BoardInfosQObject
from MutableMetaData import MutableMetaData

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout,
                             QBoxLayout, QListWidget, QFrame, QMenuBar, QMenu, QAction, QStatusBar)
from PyQt5.QtCore import (Qt, QSize, QRect, QLocale, QCoreApplication, QEvent, QObject)
from PyQt5.QtGui import (QFont)
from PyQt5.Qt import (QMouseEvent, QResizeEvent, QKeyEvent)

from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


class IdelmaGui(QMainWindow):
    """Main Window."""
    def __init__(self):
        super().__init__()

        # Declaring instance attr.
        self.centralWidget = QWidget(self)

        self.sectionsList = QListWidget(self.centralWidget)

        self.brdInfosVerticalLayoutWidget = QWidget(self.centralWidget)
        self.progBttnsVerticalLayoutWidget = QWidget(self.centralWidget)
        self.brdInfosBoxLayout = QVBoxLayout(self.brdInfosVerticalLayoutWidget)
        self.progBttnsBoxLayout = QVBoxLayout(self.progBttnsVerticalLayoutWidget)

        self.snNumberLayout = QVBoxLayout()
        self.snIdLabel = QLabel()
        self.snNumberLabel = QLabel()

        self.fwVersionLayout = QVBoxLayout()
        self.fwVerIdLabel = QLabel()
        self.fwVerLabel = QLabel()

        self.sectionsLayout = QVBoxLayout()
        self.sctsIdLabel = QLabel()
        self.sctsLabel = QLabel()

        self.pixelsLayout = QVBoxLayout()
        self.pxlsIdLabel = QLabel()
        self.pxlsLabel = QLabel()

        self.vertiLine = QFrame(self.centralWidget)
        self.horizLine = QFrame(self.centralWidget)

        self.sctEditButton = QPushButton()
        self.sctDeleteButton = QPushButton()
        self.sctAddButton = QPushButton()
        self.fetchInfosButton = QPushButton()

        self.configButton = QPushButton(self.progBttnsVerticalLayoutWidget)
        self.saveButton = QPushButton(self.progBttnsVerticalLayoutWidget)

        self.menubar = None
        self.menuFile = None
        self.menuEdit = None
        self.menuWindow = None
        self.menuDebug = None

        self.actionDebug = None
        self.actionReset_EEPROM = None
        self.actionAll_OFF = None

        # setting main window
        self.initUi()
        self.retranslateUi()

    def initUi(self):
        self.setObjectName("MainWindow")
        self.resize(480, 540)

        # setting the central widget and general layout
        self.centralWidget.setObjectName("centralWidget")

        # adding a list view widget to the main window
        self.setListWidget()

        # Vertical Layout to contain layouts of each board info category
        self.setVerticalLayout(self.brdInfosVerticalLayoutWidget, (270, 10, 191, 311), "brdInfosVerticalLayoutWidget")
        self.setVerticalLayout(self.progBttnsVerticalLayoutWidget, (290, 380, 151, 91), "progBttnsVerticalLayoutWidget")
        self.setBoxLayout(self.brdInfosBoxLayout, (0, 0, 0, 0), "brdInfosBoxLayout")
        self.setBoxLayout(self.progBttnsBoxLayout, (0, 0, 0, 0), "progBttnsBoxLayout")

        self.setBrdInfosZone(self.snNumberLayout, "snNumberLayout", self.snIdLabel, "snIdLabel",
                             self.snNumberLabel, "snNumberLabel")
        self.setBrdInfosZone(self.fwVersionLayout, "fwVersionLayout", self.fwVerIdLabel, "fwVerIdLabel",
                             self.fwVerLabel, "fwVerLabel")
        self.setBrdInfosZone(self.sectionsLayout, "sectionsLayout", self.sctsIdLabel, "sctsIdLabel",
                             self.sctsLabel, "sctsLabel")
        self.setBrdInfosZone(self.pixelsLayout, "pixelsLayout", self.pxlsIdLabel, "pxlsIdLabel",
                             self.pxlsLabel, "pxlsLabel")

        self.setLineWidget(self.vertiLine, QFrame.VLine, QFrame.Sunken, (250, 10, 20, 481), "vertiLine")
        self.setLineWidget(self.horizLine, QFrame.HLine, QFrame.Sunken, (266, 350, 201, 20), "horizLine")

        self.centralWidgetButton(self.sctEditButton, (79, 456, 177, 42), "sctEditButton", 18, 50)
        self.centralWidgetButton(self.sctDeleteButton, (42, 456, 50, 42), "sctDeleteButton", 22, 75)
        self.centralWidgetButton(self.sctAddButton, (5, 456, 50, 42), "sctAddButton", 22, 75)
        self.centralWidgetButton(self.fetchInfosButton, (304, 320, 120, 32), "fetchInfosButtons", 120, enabled=True)

        self.setProgBttns(self.configButton, "configButton")
        self.setProgBttns(self.saveButton, "saveButton")

        self.setCentralWidget(self.centralWidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 480, 24))
        self.menubar.setObjectName("menubar")

        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")

        self.menuDebug = QMenu(self.menubar)
        self.menuDebug.setObjectName("menuDebug")

        self.actionDebug = QAction(self)
        self.actionDebug.setObjectName("actionDebug")
        self.actionReset_EEPROM = QAction(self)
        self.actionReset_EEPROM.setObjectName("actionReset_EEPROM")
        self.actionAll_OFF = QAction(self)
        self.actionAll_OFF.setObjectName("actionAll_OFF")
        self.menuDebug.addAction(self.actionReset_EEPROM)
        self.menuDebug.addAction(self.actionAll_OFF)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuDebug.menuAction())

        self.setMenuBar(self.menubar)

        # self.statusbar = QStatusBar(self)
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)

    def setListWidget(self):
        self.sectionsList.setGeometry(QRect(10, 10, 240, 451))
        self.sectionsList.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.sectionsList.setFrameShape(QFrame.Box)
        self.sectionsList.setFrameShadow(QFrame.Raised)
        self.sectionsList.setLineWidth(1)
        self.sectionsList.setMidLineWidth(0)
        self.sectionsList.setObjectName("sectionsList")

    """
    Function used to set up the zone of the window where all the info relating to the MCU is shown
    """
    def setBrdInfosZone(self, sub_layout: QVBoxLayout, sub_layout_name: str, info_id_label: QLabel,
                        info_id_label_name: str, info_val_label: QLabel, info_val_label_name: str):
        """
        Set-up each zone
        """
        # Setting the sub-layout
        sub_layout.setContentsMargins(-1, -1, -1, 12)
        sub_layout.setObjectName(sub_layout_name)

        # Preparing the label that is used to identify the value of the label beneath
        info_id_label.setParent(self.brdInfosVerticalLayoutWidget)
        font = QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        info_id_label.setFont(font)
        info_id_label.setAlignment(Qt.AlignCenter)
        info_id_label.setObjectName(info_id_label_name)
        # Adding the label to the sub-layout
        sub_layout.addWidget(info_id_label)

        # Prepping the label showing the info coming from the board
        info_val_label.setParent(self.brdInfosVerticalLayoutWidget)
        info_val_label.setAlignment(Qt.AlignCenter)
        info_val_label.setObjectName(info_val_label_name)
        # Adding it to the sub-layout
        sub_layout.addWidget(info_val_label)

        # Inserting sub-layout into a parent layout
        self.brdInfosBoxLayout.addLayout(sub_layout)

    def centralWidgetButton(self, button: QPushButton, size_tuple: tuple, button_name: str, font_point_size: int = 0,
                            font_weight: int = 0, x_max_size: hex = 0xFFFFFF, y_max_size: hex = 0xFFFFFF,
                            enabled: bool = False):
        button.setParent(self.centralWidget)
        button.setEnabled(enabled)
        button.setGeometry(QRect(*size_tuple))
        button.setMaximumSize(QSize(x_max_size, y_max_size))

        button.setIconSize(QSize(16, 16))
        button.setAutoDefault(False)
        button.setFlat(False)
        button.setObjectName(button_name)

        if font_weight and font_point_size:
            self.setFrameBttnsFont(button, font_point_size, font_weight)

    def setProgBttns(self, bttn: QPushButton, button_name: str):
        bttn.setEnabled(False)
        bttn.setObjectName(button_name)
        self.progBttnsBoxLayout.addWidget(bttn)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Idelma"))
        self.snIdLabel.setText(_translate("MainWindow", "Serial Number"))
        self.snNumberLabel.setText(_translate("MainWindow", "- Empty -"))
        self.fwVerIdLabel.setText(_translate("MainWindow", "FW Version"))
        self.fwVerLabel.setText(_translate("MainWindow", "- Empty -"))
        self.sctsIdLabel.setText(_translate("MainWindow", "Sections Available"))
        self.sctsLabel.setText(_translate("MainWindow", "- Empty -"))
        self.pxlsIdLabel.setText(_translate("MainWindow", "Pixels Available"))
        self.pxlsLabel.setText(_translate("MainWindow", "- Empty -"))
        self.sctEditButton.setText(_translate("MainWindow", "Edit"))
        self.sctDeleteButton.setText(_translate("MainWindow", "-"))
        self.sctAddButton.setText(_translate("MainWindow", "+"))
        self.fetchInfosButton.setText(_translate("MainWindow", "Fetch Infos"))
        self.configButton.setText(_translate("MainWindow", "Config. Board"))
        self.saveButton.setText(_translate("MainWindow", "Save Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuDebug.setTitle(_translate("MainWindow", "Debug"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionReset_EEPROM.setText(_translate("MainWindow", "Reset EEPROM"))
        self.actionAll_OFF.setText(_translate("MainWindow", "All OFF"))

    def enableListWidgetBttns(self):
        self.sctDeleteButton.setEnabled(True)
        self.sctEditButton.setEnabled(True)

    def disableListWidgetBttns(self):
        self.sctDeleteButton.setEnabled(False)
        self.sctEditButton.setEnabled(False)

    def updtSnNumLabel(self, text: str):
        self.snNumberLabel.setText(text)

    def updtFwVerLabel(self, text: str):
        self.fwVerLabel.setText(text)

    def updtSctsInfo(self, mutable_brd_info_inst: MutableMetaData):
        self.sctsLabel.setText(str(mutable_brd_info_inst.remaining))

    def updtPxlsInfo(self, mutable_brd_info_inst: MutableMetaData):
        self.pxlsLabel.setText(str(mutable_brd_info_inst.remaining))

    @staticmethod
    def setVerticalLayout(widget: QWidget, size_tuple: tuple, widget_name: str):
        widget.setGeometry(QRect(*size_tuple))
        widget.setObjectName(widget_name)

    @staticmethod
    def setBoxLayout(box_layout: QBoxLayout, margin_tuple: tuple, layout_name: str):
        box_layout.setContentsMargins(*margin_tuple)
        box_layout.setObjectName(layout_name)

    @staticmethod
    def setLineWidget(widget: QWidget, frame_enum: QFrame.Shape, frame_shadow: QFrame.Shadow, size_tuple: tuple,
                      widget_name: str):
        widget.setGeometry(QRect(*size_tuple))
        widget.setFrameShape(frame_enum)
        widget.setFrameShadow(frame_shadow)
        widget.setObjectName(widget_name)

    @staticmethod
    def setFrameBttnsFont(button: QPushButton, font_point_size: int, font_weight: int):
        font = QFont()
        font.setPointSize(font_point_size)
        font.setBold(True)
        font.setWeight(font_weight)
        font.setKerning(True)
        button.setFont(font)
