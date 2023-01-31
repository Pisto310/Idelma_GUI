from PyQt5.QtCore import (QEvent)


class UserEvents:

    def __init__(self):
        self.eventType = 1000
        self.noneEvent = QEvent(0)

    def createCustomEvent(self):
        # Method to be called when creating a new custom event
        self.noneEvent.registerEventType(self.eventType)
        newCustomEvent = QEvent(self.eventType)
        self.incrEventType()
        return newCustomEvent

    def incrEventType(self):
        self.eventType += 1
