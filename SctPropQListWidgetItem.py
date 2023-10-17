from SctProp import SctProp

from PyQt5.QtWidgets import (QListWidgetItem, QListWidget)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import (QFont)


class SctPropQListWidgetItem(SctProp, QListWidgetItem):
    """
    A SctProp subclass aimed to be used in a PyQt
    environment by also subclassing the QListWidgetItem
    class to be use in a QListWidget
    """
    def __init__(self, index: int, pixel_count: int, name: str, set_default_name: bool,
                 item_parent: QListWidget, item_type: QListWidgetItem.ItemType):
        # Calling the superclass
        super().__init__(index=index, pixel_count=pixel_count, name=name, set_default_name=set_default_name)
        QListWidgetItem.__init__(self, name, parent=item_parent, type=item_type)

        self.sctPropItemType = item_type
        self.modFont()

    def __eq__(self, other):
        if not isinstance(other, SctProp):
            return NotImplemented
        return (self.sctID == other.sctID and
                self.pxlCount == other.pxlCount and
                self.sctName == other.sctName and
                self.setDefaultName == other.setDefaultName)

    def __ne__(self, other):
        return not self == other

    def modFont(self):
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

    def type(self) -> int:
        return self.sctPropItemType

    def setText(self):
        super().setText(self.sctName)

    # def updtRemainingPxls(self, pxls_remaining):
    #     self.remainingPxls = pxls_remaining
