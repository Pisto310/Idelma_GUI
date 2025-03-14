from PxlMetaData import PxlMetaData

from TableWidgetItemUserType import TableWidgetItemUserType

from PyQt5.QtWidgets import QTableWidgetItem


class PxlMetaDataQTableWidgetItem(PxlMetaData, QTableWidgetItem):
    """
    Special object to use PxlMetaData class in the context
    of a QTableWidget by setting this class a child of
    QTableWidgetItem & PxlMetaData
    """
    tableWidgetItemType = TableWidgetItemUserType.newUserType('Pxl MetaData Type')

    def __init__(self, pxl_idx: int):
        super().__init__(pxl_idx)
        QTableWidgetItem.__init__(self, type=self.tableWidgetItemType)

    def type(self) -> str:
        return TableWidgetItemUserType.typeDict[self.tableWidgetItemType]
