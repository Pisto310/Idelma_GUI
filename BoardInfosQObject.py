import sys
from BoardInfos import BoardInfos
from MutableBrdInfo import MutableBrdInfo

from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtCore import (QObject, pyqtSignal)


class BoardInfosQObject(QObject, BoardInfos):
    """
    TBD
    """
    snUpdted = pyqtSignal(str, name='sn_updated')
    fwVerUpdted = pyqtSignal(str, name='fw_ver_updated')
    sctsUpdted = pyqtSignal(MutableBrdInfo, name='sections_info_updated')
    pxlsUpdted = pyqtSignal(MutableBrdInfo, name='pixels_info_updated')

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

    # def emitSignal(self, *args, **kwargs):
    #     for index, qt_signal in enumerate(self.sigTuple):
    #         if kwargs.values() == self.extractSigName(qt_signal):
    #             qt_signal.emit(*args)
    #         else:
    #             # Should raise error since no signal is associated to a board attr
    #             pass

    # def extractSigName(self, pyqt_sig: pyqtSignal):
    #     """
    #     pyqtSignal obj have an attribute called 'signatures' which is essentially a tuple of 1 element. This tuple is
    #     made up of a string constituted of the signal name, followed by the input type(s) in parenthesis. If there are
    #     multiple input types, they are separated by a comma
    #
    #     ex. w/ sn_updt: signatures = ('snUpdted(str)')
    #     """
    #     final_char = '('
    #     signal_name = ''
    #     for index, val in enumerate(pyqt_sig.signatures[0]):
    #         if val != final_char:
    #             signal_name += val
    #         else:
    #             return signal_name
