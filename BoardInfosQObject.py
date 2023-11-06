import sys
from BoardInfos import BoardInfos
from BrdMgmtMetaData import BrdMgmtMetaData

from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtCore import (QObject, pyqtSignal)


class BoardInfosQObject(QObject, BoardInfos):
    """
    TBD
    """
    snUpdted = pyqtSignal(str, name='sn_updated')
    fwVerUpdted = pyqtSignal(str, name='fw_ver_updated')
    sctsUpdted = pyqtSignal(BrdMgmtMetaData, name='sections_info_updated')
    pxlsUpdted = pyqtSignal(BrdMgmtMetaData, name='pixels_info_updated')
    sctsInfoTupleSig = pyqtSignal(list, name="sections_info_tuple_from_MCU")

    def __init__(self):
        super().__init__()

    def connectSnSignal(self, callback):
        self.snUpdted.connect(callback)

    def connectFwVerSignal(self, callback):
        self.fwVerUpdted.connect(callback)

    def connectSctsMgmtSignal(self, callback):
        self.sctsUpdted.connect(callback)

    def connectPxlsMgmtSignal(self, callback):
        self.pxlsUpdted.connect(callback)

    def connectSctsInfoTupleSig(self, callback):
        self.sctsInfoTupleSig.connect(callback)

    def snUpdtEmit(self, *args):
        self.snUpdted.emit(*args)

    def fwVerUpdtEmit(self, *args):
        self.fwVerUpdted.emit(*args)

    def sctsMgmtUpdtEmit(self, *args):
        self.sctsUpdted.emit(*args)

    def pxlsMgmtUpdtEmit(self, *args):
        self.pxlsUpdted.emit(*args)

    def sctsInfoTupleEmit(self, *args):
        self.sctsInfoTupleSig.emit(*args)
