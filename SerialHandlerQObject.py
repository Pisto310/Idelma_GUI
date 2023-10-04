from SerialHandler import SerialHandler

from PyQt5.QtCore import (QObject, pyqtSignal)


class SerialHandlerQObject(QObject, SerialHandler):
    """
    class description
    """
    notifyRxer = pyqtSignal(name='serial_mssg_sent')

    def __init__(self, serial_port):
        super().__init__(serial_port=serial_port)

    def connectNotifySignal(self, callback):
        self.notifyRxer.connect(callback)

    def notifyRxerEmit(self):
        self.notifyRxer.emit()
