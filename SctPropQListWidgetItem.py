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
    def __init__(self, name: str, pixel_count: int, set_default_name: bool, item_parent: QListWidget, item_type: QListWidgetItem.ItemType):
        # Calling the superclass
        super().__init__(name=name, pixel_count=pixel_count, set_default_name=set_default_name)
        QListWidgetItem.__init__(self, name, parent=item_parent, type=item_type)

        self.sctPropItemType = item_type
        self.modFont()

    def modFont(self):
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

    def type(self) -> int:
        return self.sctPropItemType

    def setText(self):
        super().setText(self.sctName)
