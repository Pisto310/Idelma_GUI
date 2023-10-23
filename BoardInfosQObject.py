import sys
from BoardInfos import BoardInfos
from MutableMetaData import MutableMetaData

from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtCore import (QObject, pyqtSignal)


class BoardInfosQObject(QObject, BoardInfos):
    """
    TBD
    """
    snUpdted = pyqtSignal(str, name='sn_updated')
    fwVerUpdted = pyqtSignal(str, name='fw_ver_updated')
    sctsUpdted = pyqtSignal(MutableMetaData, name='sections_info_updated')
    pxlsUpdted = pyqtSignal(MutableMetaData, name='pixels_info_updated')

    def __init__(self):
        super().__init__()

    def connectSnSignal(self, callback):
        self.snUpdted.connect(callback)

    def connectFwVerSignal(self, callback):
        self.fwVerUpdted.connect(callback)

    def connectSctsSignal(self, callback):
        self.sctsUpdted.connect(callback)

    def connectPxlsSignal(self, callback):
        self.pxlsUpdted.connect(callback)

    def snUpdtedEmit(self, *args):
        self.snUpdted.emit(*args)

    def fwVerUpdtedEmit(self, *args):
        self.fwVerUpdted.emit(*args)

    def sctsUpdtedEmit(self, *args):
        self.sctsUpdted.emit(*args)

    def pxlsUpdtedEmit(self, *args):
        self.pxlsUpdted.emit(*args)
