from PyQt5.QtWidgets import (QListWidgetItem)


class ListWidgetItemUserType:
    """
    Simple class to track user created
    types for ListWidgetItem
    """
    typeIndex = int(QListWidgetItem.UserType) - 1
    typeDict = {}

    @classmethod
    def newUserType(cls, user_string: str) -> QListWidgetItem.ItemType:
        """
        Method used to create a new UserType
        """
        cls.typeIndex += 1
        itemType = QListWidgetItem.ItemType(cls.typeIndex)
        cls.typeDict.update({user_string: itemType})
        return itemType
