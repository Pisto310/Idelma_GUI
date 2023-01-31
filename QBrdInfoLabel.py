from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import (QEvent)


class QBrdInfoLabel(QLabel):
    """
    coming soon
    """

    def __init__(self, new_event_type: int):
        super().__init__()
        self.customEventType = new_event_type

    def event(self, event: QEvent) -> bool:
        if event.type() == self.customEventType:
            # Here, the goal is to change the label's text to the string content of the associated board info attr
            pass
        else:
            return super().event(event)
