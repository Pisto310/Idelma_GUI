import numpy as np
from MutableBrdInfo import MutableBrdInfo


class BoardInfos:
    """
    This class contains all the board info
    as attributes and all associated methods.
    to get, set and more
    """
    def __init__(self):

        self._serialNum = None
        self._fwVersion = None
        self._sctsBrdMgmt = None
        self._pxlsBrdMgmt = None

    # Method used to set the serial number of the board using the parsed message received in the serial buffer
    def serialNumSet(self, parsed_ser_mssg: list):
        hex_container = 0
        for index, val in enumerate(parsed_ser_mssg):
            hex_container += val << (8 * index)
        self.serialNum = hex_container

    # Method to set the FW version with the parsed message of the serial buffer
    def fwVersionSet(self, parsed_ser_mssg: list):
        str_container = ""
        for index, val in enumerate(parsed_ser_mssg):
            str_container += str(val)
            if (index + 1) < len(parsed_ser_mssg):
                str_container += "."
        self.fwVersion = str_container

    def sctsBrdMgmtSet(self, parsed_ser_mssg: list):
        self.sctsBrdMgmt = MutableBrdInfo(*parsed_ser_mssg)

    def pxlsBrdMgmtSet(self, parsed_ser_mssg: list):
        self.pxlsBrdMgmt = MutableBrdInfo(*parsed_ser_mssg)

    @property
    def serialNum(self):
        return self._serialNum

    @serialNum.setter
    def serialNum(self, new_serial: int):
        self._serialNum = hex(new_serial)

    @property
    def fwVersion(self):
        return self._fwVersion

    @fwVersion.setter
    def fwVersion(self, new_version: str):
        self._fwVersion = new_version

    @property
    def sctsBrdMgmt(self):
        return self._sctsBrdMgmt

    @sctsBrdMgmt.setter
    def sctsBrdMgmt(self, new_inst: MutableBrdInfo):
        self._sctsBrdMgmt = new_inst

    @property
    def pxlsBrdMgmt(self):
        return self._pxlsBrdMgmt

    @pxlsBrdMgmt.setter
    def pxlsBrdMgmt(self, new_inst: MutableBrdInfo):
        self._pxlsBrdMgmt = new_inst