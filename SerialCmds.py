

class SerialCmds:
    """
    All serial commands related to the
    Arduino board are contained in this
    class
    """

    def __init__(self):
        self._rqstBoardInfos = {"cmd": "0", "resp_bytes": 9}  # cmd will be replaced by BRD
        self._createSctCmd = "1"        # Will be replace by NEW

    @property
    def rqstBoardInfos(self):
        return self._rqstBoardInfos

