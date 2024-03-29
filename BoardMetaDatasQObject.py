from BoardMetaDatas import BoardMetaDatas
from BrdMgmtMetaData import BrdMgmtMetaData
from SctMetaData import SctMetaData

from PyQt5.QtCore import (QObject, pyqtSignal)


class BoardMetaDatasQObject(QObject, BoardMetaDatas):
    """
    TBD
    """
    snUpdted = pyqtSignal(str, name='sn_updated')
    fwVerUpdted = pyqtSignal(str, name='fw_ver_updated')
    sctsUpdted = pyqtSignal(str, name='sections_info_updated')
    pxlsUpdted = pyqtSignal(str, name='pixels_info_updated')

    def __init__(self):
        super().__init__()

    def deletingSection(self, sct_metadata: SctMetaData):
        """
        Supercharge the method by adding the popping of element being deleted

        Parameters:
            sct_metadata (SctMetaData): SctMetaData obj with all info related to the deleted section
        """
        super().deletingSection(sct_metadata)
        self.sctsMetaDataList.pop(sct_metadata.sctIdx)

    def connectSnSignal(self, callback):
        self.snUpdted.connect(callback)

    def connectFwVerSignal(self, callback):
        self.fwVerUpdted.connect(callback)

    def connectSctsMgmtSignal(self, callback):
        self.sctsUpdted.connect(callback)

    def connectPxlsMgmtSignal(self, callback):
        self.pxlsUpdted.connect(callback)

    def snUpdtEmit(self, *args):
        self.snUpdted.emit(*args)

    def fwVerUpdtEmit(self, *args):
        self.fwVerUpdted.emit(*args)

    def sctsMgmtUpdtEmit(self, *args):
        self.sctsUpdted.emit(*args)

    def pxlsMgmtUpdtEmit(self, *args):
        self.pxlsUpdted.emit(*args)
