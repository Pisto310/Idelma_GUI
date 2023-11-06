from NonSerSctMetaData import NonSerSctMetaData

from PyQt5.QtWidgets import (QListWidgetItem, QListWidget)
from PyQt5.QtGui import (QFont)


class NonSerSctMetaDataQListWidgetItem(NonSerSctMetaData, QListWidgetItem):
    """
    A NonSerSctMetaData subclass aimed to be used in a PyQt
    environment by also subclassing the QListWidgetItem
    class to be use in a QListWidget
    """
    def __init__(self, name: str, item_parent: QListWidget, item_type: QListWidgetItem.ItemType):
        super().__init__(name)
        QListWidgetItem.__init__(self, name, parent=item_parent, type=item_type)

        self.sctPropItemType = item_type
        self.modFont()

    def __eq__(self, other):
        if not isinstance(other, NonSerSctMetaData):
            return NotImplemented
        return self.sctName == other.sctName

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
