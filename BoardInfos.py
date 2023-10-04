from MutableBrdInfo import MutableBrdInfo
from enum import Enum


class BoardInfos:
    """
    This class contains all the board info
    as attributes and all associated methods
    to get, set and more
    """
    def __init__(self):

        self._serialNum   = None
        self._fwVersion   = None
        self._sctsBrdMgmt = None
        self._pxlsBrdMgmt = None

        self.sctsList = []

        self.configBrdByteToFunc = {0: self.pixelBlocksAssig}

        self.ackChar = 6

    def __eq__(self, other):
        if not isinstance(other, BoardInfos):
            return NotImplemented
        return (self.serialNum == other.serialNum and
                self.fwVersion == other.fwVersion and
                self.sctsBrdMgmt == other.sctsBrdMgmt and
                self.pxlsBrdMgmt == other.pxlsBrdMgmt)

    def __ne__(self, other):
        return not self == other

    # Method used to set the serial number of the board using the parsed message received in the serial buffer
    def serialNumMssgDecode(self, parsed_ser_mssg: list):
        hex_container = 0
        for index, val in enumerate(parsed_ser_mssg):
            hex_container += val << (8 * index)
        self.serialNum = hex(hex_container)

    # Method to set the FW version with the parsed message of the serial buffer
    def fwVersionMssgDecode(self, parsed_ser_mssg: list):
        str_container = ""
        for index, val in enumerate(parsed_ser_mssg):
            str_container += str(val)
            if (index + 1) < len(parsed_ser_mssg):
                str_container += "."
        self.fwVersion = str_container

    def sctsBrdMgmtMssgDecode(self, parsed_ser_mssg: list):
        self.sctsBrdMgmt = MutableBrdInfo(*parsed_ser_mssg)

    def pxlsBrdMgmtMssgDecode(self, parsed_ser_mssg: list):
        self.pxlsBrdMgmt = MutableBrdInfo(*parsed_ser_mssg)

    # def blocksUsageUpdt(self, param):
    #     # Compare with actual assigned count to check for allocation or reallocation?
    #     self.sctsBrdMgmt.blockAssignation(1)
    #     self.pxlsBrdMgmt.blockAssignation(param)

    def configBrdUpdt(self, parsed_ser_mssg: list, *args):
        """
        Checks if ACK has been received and if so, updates board attributes

        Parameters:
            parsed_ser_mssg (list): received serial response, parsed (should be ack char 0x06)
            *args (tuple of tuples): a tuple of sctInfoTuple
        """
        if self.ackConfirmed(parsed_ser_mssg):
            for i, sctInfoTuple in enumerate(args):
                for j, val in enumerate(sctInfoTuple[1::]):
                    self.sctsBrdMgmt.blockAssignation(1)
                    self.configBrdByteToFunc[j](val)

    def pixelBlocksAssig(self, pixel_count):
        self.pxlsBrdMgmt = self.pxlsBrdMgmt.blockAssignation(pixel_count)

    def ackConfirmed(self, parsed_ser_mssg: list):
        """
        Reads parsed serial message to confirm that it is solely the expected ACK char

        Parameters:
            parsed_ser_mssg (list): Normally a list of len = 1 solely containing the ACK char
        """
        try:
            if parsed_ser_mssg[0] == self.ackChar:
                return True
            else:
                return False
        except IndexError as error:
            print(error)

    # def sctSetupUpdt(self, parsed_ser_mssg, led_count: int):
    #     if parsed_ser_mssg:
    #         self.sctsBrdMgmt.blockDecrement(1)
    #         self.pxlsBrdMgmt.blockDecrement(led_count)
    #     else:
    #         print("section assignation failed")

    def snUpdtedEmit(self, *args):
        pass

    def fwVerUpdtedEmit(self, *args):
        pass

    def sctsUpdtedEmit(self, *args):
        pass

    def pxlsUpdtedEmit(self, *args):
        pass

    @property
    def serialNum(self):
        return self._serialNum

    @serialNum.setter
    def serialNum(self, new_serial: int):
        if not self.valCompare(new_serial, self.serialNum):
            self._serialNum = new_serial
            self.snUpdtedEmit(self.serialNum)

    @property
    def fwVersion(self):
        return self._fwVersion

    @fwVersion.setter
    def fwVersion(self, new_version: str):
        if not self.valCompare(new_version, self.fwVersion):
            self._fwVersion = new_version
            self.fwVerUpdtedEmit(self.fwVersion)

    @property
    def sctsBrdMgmt(self) -> MutableBrdInfo:
        return self._sctsBrdMgmt

    @sctsBrdMgmt.setter
    def sctsBrdMgmt(self, new_inst: MutableBrdInfo):
        if not self.valCompare(new_inst, self.sctsBrdMgmt):
            self._sctsBrdMgmt = new_inst
            self.sctsUpdtedEmit(self.sctsBrdMgmt)

    @property
    def pxlsBrdMgmt(self) -> MutableBrdInfo:
        return self._pxlsBrdMgmt

    @pxlsBrdMgmt.setter
    def pxlsBrdMgmt(self, new_inst: MutableBrdInfo):
        if not self.valCompare(new_inst, self.pxlsBrdMgmt):
            self._pxlsBrdMgmt = new_inst
            self.pxlsUpdtedEmit(self.pxlsBrdMgmt)

    @staticmethod
    def valCompare(new_val, old_val):
        """
        Static method to compare two variable and
        check if their value is the same. Returns
        True if equal and False otherwise
        """
        if new_val == old_val:
            return True
        else:
            return False

    # @property
    # def snUpdtFlag(self) -> bool:
    #     return self._snUpdtFlag
    #
    # @snUpdtFlag.setter
    # def snUpdtFlag(self, new_state: bool):
    #     self.booleanUpdt(self._snUpdtFlag, new_state)
    #
    # @property
    # def fwUpdtFlag(self) -> bool:
    #     return self._fwUpdtFlag
    #
    # @fwUpdtFlag.setter
    # def fwUpdtFlag(self, new_state: bool):
    #     self.booleanUpdt(self._fwUpdtFlag, new_state)
    #
    # @property
    # def sctUpdtFlag(self) -> bool:
    #     return self._sctUpdtFlag
    #
    # @sctUpdtFlag.setter
    # def sctUpdtFlag(self, new_state: bool):
    #     self.booleanUpdt(self._sctUpdtFlag, new_state)
    #
    # @property
    # def pxlUpdtFlag(self) -> bool:
    #     return self._pxlUpdtFlag
    #
    # @pxlUpdtFlag.setter
    # def pxlUpdtFlag(self, new_state: bool):
    #     self.booleanUpdt(self._pxlUpdtFlag, new_state)
    #
    # @property
    # def flagsTuple(self) -> tuple:
    #     return self._flagsTuple

    @staticmethod
    def booleanUpdt(actual_state: bool, new_state: bool):
        try:
            if type(new_state) != bool:
                raise ValueError
            if new_state == actual_state:
                pass
            else:
                actual_state = new_state
        except ValueError:
            print("New value should be a boolean")
