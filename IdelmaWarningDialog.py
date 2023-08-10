from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLayout, QLabel, QLineEdit, QSpinBox, QDialogButtonBox,
                             QApplication, QDialog, QWidget, QSizePolicy, QCheckBox)
from PyQt5.QtCore import (Qt, QRect, QSize, QCoreApplication, pyqtSignal, QMetaObject, QLocale)


class IdelmaWarningDialog(QDialog):
    """
    Template class for when creating warning dialogs in the
    project
    """
    def __init__(self):
        super().__init__()

        # Declaring instance attributes
        self.win_x = None
        self.win_y = None
        self.rect = QRect(0, 0, 0, 0)

        self.centralWidget = None
        self.warningTitle = None
        self.warningMssg = None
        self.hideMssgCheckBox = None
        self.buttonBox = None
        self.verticalLayout = None

        self.winSize()
        self.rectSize()
        self.setupUi()
        self.assigningSlots()
        self.retranslateUi()

    def winSize(self):
        x_default = 240
        y_default = 140
        if self.win_x is None:
            self.win_x = x_default
        if self.win_y is None:
            self.win_y = y_default
        self.resize(self.win_x, self.win_y)

    def rectSize(self):
        x_margin = 12
        y_margin = 10
        self.rect.setRect(x_margin, 0, self.win_x - 2 * x_margin, self.win_y - y_margin)

    def setupUi(self):
        self.setObjectName("Warning")

        # Central widget
        self.centralWidget = QWidget(self)
        self.centralWidget.setGeometry(self.rect)
        self.centralWidget.setObjectName("central widget")

        # Warning title as a QLabel widget
        self.warningTitle = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        # font.setWeight(60)
        font.setKerning(True)
        self.warningTitle.setFont(font)
        self.warningTitle.setAlignment(Qt.AlignCenter)
        self.warningTitle.setWordWrap(True)
        self.warningTitle.setObjectName("warningTitle")

        # Warning message as a QLabel widget
        self.warningMssg = QLabel(self)
        font = QFont()
        font.setPointSize(14)
        # font.setWeight(60)
        # font.setKerning(True)
        self.warningMssg.setFont(font)
        self.warningMssg.setAlignment(Qt.AlignJustify)
        self.warningMssg.setContentsMargins(7, 0, 7, 10)
        self.warningMssg.setWordWrap(True)
        self.warningMssg.setObjectName("warningMssg")

        # Checkbox for 'Don't show this message again'
        self.hideMssgCheckBox = QCheckBox(self)
        self.hideMssgCheckBox.setText('Don\'t show this message again'),
        font = QFont()
        font.setPointSize(14)
        font.setFamily('Marion')
        self.hideMssgCheckBox.setFont(font)

        # Dialog button box
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.settingBttns()

        # Arranging all widgets in a vertical layout
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.warningTitle)
        self.verticalLayout.addWidget(self.warningMssg)
        self.verticalLayout.addWidget(self.hideMssgCheckBox)
        self.verticalLayout.addWidget(self.buttonBox)

    def settingBttns(self):
        """
        To be implemented by children classes
        """
        pass

    def assigningSlots(self):
        """
        To be implemented by children classes
        """
        pass

    def retranslateUi(self):
        """
        To be implemented by children classes
        """
        pass
