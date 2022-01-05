

class SerialCmds:
    """All serial commands related to the
    Arduino board are contained in this
    class"""

    def __init__(self):
        self._getBoardInfosCmd = "0"    # Will replace by BRD
        self._createSctCmd = "1"        # Will replace by NEW

    @property
    def getBoardInfosCmd(self):
        return self._getBoardInfosCmd

    @property
    def getCreateSctCmd(self):
        return self._getBoardInfosCmd

