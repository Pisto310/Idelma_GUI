from SctProp import SctProp
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

        self.sctsMetaData = []

        # self.configBrdByteToFunc = {SctProp.infoTupleIndexes.get('pixel_count_index'): self.pixelBlockAssig}

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
    #     self.sctsBrdMgmt.blockAssig(1)
    #     self.pxlsBrdMgmt.blockAssig(param)

    def configBrdAttrUpdt(self, parsed_ser_mssg: list, *args):
        """
        Checks if ACK has been received and if so, updates board attributes

        Parameters:
            parsed_ser_mssg (list): received serial response, parsed (should be ack char 0x06)
            *args (tuple of tuples): a tuple of sctInfoTuple
        """
        if self.ackConfirmed(parsed_ser_mssg):
            sct_total_blocks = 0
            pxl_total_blocks = 0
            sct_id_index = SctProp.infoTupleIndexes.get('sctID_index')
            pxl_count_index = SctProp.infoTupleIndexes.get('pixelCount_index')
            for sctInfoTuple in args:
                try:
                    sct_id = sctInfoTuple[sct_id_index]
                    pxl_count_diff = sctInfoTuple[pxl_count_index] - self.sctsMetaData[sct_id][pxl_count_index]
                    pxl_total_blocks += pxl_count_diff
                    if abs(pxl_count_diff) == self.sctsMetaData[sct_id][pxl_count_index]:
                        sct_total_blocks -= 1
                        self.sctsMetaData.pop(sct_id)
                        continue
                    self.sctsMetaData[sct_id] = (sct_id, sctInfoTuple[pxl_count_index])
                except IndexError:
                    if sctInfoTuple[pxl_count_index]:
                        sct_total_blocks += 1
                        pxl_total_blocks += sctInfoTuple[pxl_count_index]
                        self.sctsMetaData.append(sctInfoTuple)
            if sct_total_blocks:
                self.sctsBrdMgmt = MutableBrdInfo.blockUpdt(self.sctsBrdMgmt.capacity,
                                                            self.sctsBrdMgmt.remaining,
                                                            self.sctsBrdMgmt.assigned,
                                                            sct_total_blocks)
            if pxl_total_blocks:
                self.pxlsBrdMgmt = MutableBrdInfo.blockUpdt(self.pxlsBrdMgmt.capacity,
                                                            self.pxlsBrdMgmt.remaining,
                                                            self.pxlsBrdMgmt.assigned,
                                                            pxl_total_blocks)

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
