from BoardInfosQObject import BoardInfosQObject
from MutableMetaData import MutableMetaData

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout,
                             QListWidget, QFrame, QMenuBar, QStatusBar)
from PyQt5.QtCore import (Qt, QSize, QRect, QLocale, QCoreApplication, QEvent, QObject)
from PyQt5.QtGui import (QFont)
from PyQt5.Qt import (QMouseEvent, QResizeEvent, QKeyEvent)

from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


class IdelmaGui(QMainWindow):
    """Main Window."""
    def __init__(self):
        super().__init__()

        # setting main window
        self.initUi()
        self.retranslateUi()

    """
    Function used to set up the zone of the window where all the info relating to the MCU is shown
    """
    def setBrdInfosZone(self, sub_layout: QVBoxLayout, sub_layout_name: str, info_id_label: QLabel,
                        info_id_label_name: str, info_val_label: QLabel, info_val_label_name: str):
        # Setting the sub-layout
        sub_layout.setContentsMargins(-1, -1, -1, 12)
        sub_layout.setObjectName(sub_layout_name)

        # Preparing the label that is used to identify the value of the label beneath
        info_id_label.setParent(self.verticalLayoutWidget)
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
        info_val_label.setParent(self.verticalLayoutWidget)
        info_val_label.setAlignment(Qt.AlignCenter)
        info_val_label.setObjectName(info_val_label_name)
        # Adding it to the sub-layout
        sub_layout.addWidget(info_val_label)

        # Inserting sub-layout into a parent layout
        self.brdInfosMainLayout.addLayout(sub_layout)

    def centralWidgetButton(self, button: QPushButton, button_name: str,
                            x_max_size: hex = 0xFFFFFF, y_max_size: hex = 0xFFFFFF, enabled: bool = False):
        button.setParent(self.centralwidget)
        button.setEnabled(enabled)
        button.setMaximumSize(QSize(x_max_size, y_max_size))

        button.setIconSize(QSize(16, 16))
        button.setAutoDefault(False)
        button.setFlat(False)
        button.setObjectName(button_name)

    def initUi(self):
        self.setObjectName("MainWindow")
        self.resize(480, 540)

        # setting the central widget and general layout
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralWidget")

        # adding a list view widget to the main window
        self.sectionsList = QListWidget(self.centralwidget)
        self.sectionsList.setGeometry(QRect(10, 10, 240, 451))
        self.sectionsList.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.sectionsList.setFrameShape(QFrame.Box)
        self.sectionsList.setFrameShadow(QFrame.Raised)
        self.sectionsList.setLineWidth(1)
        self.sectionsList.setMidLineWidth(0)
        self.sectionsList.setObjectName("sectionsList")

        # Vertical Layout to contain layouts of each board info category
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(270, 10, 191, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.brdInfosMainLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.brdInfosMainLayout.setContentsMargins(0, 0, 0, 0)
        self.brdInfosMainLayout.setObjectName("brdInfosMainLayout")

        self.snNumberLayout = QVBoxLayout()
        self.snIdLabel = QLabel()
        self.snNumberLabel = QLabel()
        self.setBrdInfosZone(self.snNumberLayout, "snNumberLayout", self.snIdLabel, "snIdLabel",
                             self.snNumberLabel, "snNumberLabel")
        self.fwVersionLayout = QVBoxLayout()
        self.fwVerIdLabel = QLabel()
        self.fwVerLabel = QLabel()
        self.setBrdInfosZone(self.fwVersionLayout, "fwVersionLayout", self.fwVerIdLabel, "fwVerIdLabel",
                             self.fwVerLabel, "fwVerLabel")
        self.sectionsLayout = QVBoxLayout()
        self.sctsIdLabel = QLabel()
        self.sctsLabel = QLabel()
        self.setBrdInfosZone(self.sectionsLayout, "sectionsLayout", self.sctsIdLabel, "sctsIdLabel",
                             self.sctsLabel, "sctsLabel")
        self.pixelsLayout = QVBoxLayout()
        self.pxlsIdLabel = QLabel()
        self.pxlsLabel = QLabel()
        self.setBrdInfosZone(self.pixelsLayout, "pixelsLayout", self.pxlsIdLabel, "pxlsIdLabel",
                             self.pxlsLabel, "pxlsLabel")

        self.vertiLine = QFrame(self.centralwidget)
        self.vertiLine.setGeometry(QRect(250, 10, 20, 481))
        self.vertiLine.setFrameShape(QFrame.VLine)
        self.vertiLine.setFrameShadow(QFrame.Sunken)
        self.vertiLine.setObjectName("vertiLine")
        self.horizLine = QFrame(self.centralwidget)
        self.horizLine.setGeometry(QRect(266, 350, 201, 20))
        self.horizLine.setFrameShape(QFrame.HLine)
        self.horizLine.setFrameShadow(QFrame.Sunken)
        self.horizLine.setObjectName("horizLine")

        self.sctEditButton = QPushButton()
        self.sctEditButton.setGeometry(QRect(79, 456, 177, 42))
        self.centralWidgetButton(self.sctEditButton, "sctEditButton")
        self.frameBttnsFont(self.sctEditButton,18, 50)
        self.sctDeleteButton = QPushButton()
        self.sctDeleteButton.setGeometry(QRect(42, 456, 50, 42))
        self.centralWidgetButton(self.sctDeleteButton, "sctDeleteButton", 50)
        self.frameBttnsFont(self.sctDeleteButton, 22, 75)
        self.sctAddButton = QPushButton()
        self.sctAddButton.setGeometry(QRect(5, 456, 50, 42))
        self.centralWidgetButton(self.sctAddButton, "sctAddButton", 50)
        self.frameBttnsFont(self.sctAddButton, 22, 75)
        self.fetchInfosButton = QPushButton()
        self.fetchInfosButton.setGeometry(QRect(304, 320, 120, 32))
        self.centralWidgetButton(self.fetchInfosButton, "fetchInfosButtons", 120, enabled=True)
        font = QFont()
        font.setKerning(True)
        self.fetchInfosButton.setFont(font)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QRect(290, 380, 151, 91))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.boardProgLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.boardProgLayout.setContentsMargins(0, 0, 0, 0)
        self.boardProgLayout.setObjectName("boardProgLayout")

        self.configButton = QPushButton(self.verticalLayoutWidget_2)
        self.configButton.setObjectName("configButton")
        self.configButton.setEnabled(False)
        self.boardProgLayout.addWidget(self.configButton)

        self.saveButton = QPushButton(self.verticalLayoutWidget_2)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setEnabled(False)
        self.boardProgLayout.addWidget(self.saveButton)

        self.setCentralWidget(self.centralwidget)

        # self.menubar = QMenuBar(self)
        # self.menubar.setGeometry(QRect(0, 0, 480, 24))
        # self.menubar.setObjectName("menubar")
        # self.setMenuBar(self.menubar)
        # self.statusbar = QStatusBar(self)
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)

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
    def frameBttnsFont(button: QPushButton, font_point_size: int, font_weight: int):
        font = QFont()
        font.setPointSize(font_point_size)
        font.setBold(True)
        font.setWeight(font_weight)
        font.setKerning(True)
        button.setFont(font)
