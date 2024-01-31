from PyQt5.QtWidgets import (QTableWidgetItem)


class TableWidgetItemUserType:
    """
    Simple class to track user created
    types for TableWidgetItem
    """
    typeIndex = int(QTableWidgetItem.UserType)
    typeDict = {}

    @classmethod
    def newUserType(cls, user_string: str) -> QTableWidgetItem.ItemType:
        """
        Method used to create a new UserType
        """
        itemType = QTableWidgetItem.ItemType(cls.typeIndex)
        cls.typeDict.update({user_string: itemType})
        cls.typeIndex += 1
        return itemType
