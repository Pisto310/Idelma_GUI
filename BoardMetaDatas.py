from NonSerSctMetaData import NonSerSctMetaData
from BrdMgmtMetaData import BrdMgmtMetaData
from SctMetaData import SctMetaData

from dataclasses import (astuple, asdict)


class BoardMetaDatas:
    """
    This class contains all the mcu info
    as attributes and all associated methods
    to get, set and more
    """
    def __init__(self):

        self._serialNum        = None
        self._fwVersion        = None
        self._sctsMgmtMetaData = None
        self._pxlsMgmtMetaData = None

        self.sctsMetaDataList = []

        self.configBrdSubCmds = {"create_sct": self.addingSection,
                                 "edit_sct":   self.editingSection,
                                 "delete_sct": self.deletingSection}
        self.configBrdSubCmdsKeys = list(self.configBrdSubCmds.keys())

        self.ackChar = 6
        self.nakChar = 21

    def __eq__(self, other):
        if not isinstance(other, BoardMetaDatas):
            return NotImplemented
        return (self.serialNum == other.serialNum and
                self.fwVersion == other.fwVersion and
                self.sctsMgmtMetaData == other.sctsMgmtMetaData and
                self.pxlsMgmtMetaData == other.pxlsMgmtMetaData and
                self.sctsMetaDataList == other.sctsMetaDataList)

    def __ne__(self, other):
        return not self == other

    def serialNumUpdt(self, parsed_ser_mssg: list):
        """
        Update the serial number attr from a received serial message

        Parameters:
            parsed_ser_mssg (list): List of bytes of a 32-bit serial number in little endian (LE) format
        """
        hex_container = 0
        for index, val in enumerate(parsed_ser_mssg):
            hex_container += val << (8 * index)
        self.serialNum = hex(hex_container)

    def fwVersionUpdt(self, parsed_ser_mssg: list):
        """
        Update the firmware version attr from a received serial message

        Parameters:
            parsed_ser_mssg (list): List of bytes, one for each part of FW version (major, minor & patch).
                                    LE format
        """
        str_container = ""
        for index, val in enumerate(parsed_ser_mssg):
            str_container += str(val)
            if (index + 1) < len(parsed_ser_mssg):
                str_container += "."
        self.fwVersion = str_container

    def sctsMgmtUpdt(self, parsed_ser_mssg: list):
        """
        Update the sections mgmt attr from a received serial message

        Parameters:
            parsed_ser_mssg (list): List of bytes representing mcu sections capacity, remaining & assigned
        """
        self.sctsMgmtMetaData = BrdMgmtMetaData(*parsed_ser_mssg)

    def pxlsMgmtUpdt(self, parsed_ser_mssg: list):
        """
        Update the pixels mgmt attr from a received serial message

        Parameters:
            parsed_ser_mssg (list): List of bytes representing mcu pixels capacity, remaining & assigned
        """
        self.pxlsMgmtMetaData = BrdMgmtMetaData(*parsed_ser_mssg)

    def sctsMetaDataListUpdt(self, parsed_ser_mssg: list):
        """

        """
        if parsed_ser_mssg[0] != self.nakChar and len(parsed_ser_mssg) > 1:
            data_pckt_len = int(len(parsed_ser_mssg) / self.sctsMgmtMetaData.assigned)
            indexed_scts_metadatas = [parsed_ser_mssg[x:x + data_pckt_len]
                                      for x in range(0, len(parsed_ser_mssg), data_pckt_len)]
            for i in range(0, self.sctsMgmtMetaData.assigned):
                self.sctsMetaDataList.append(SctMetaData(i, *indexed_scts_metadatas[i]))

    def configBrd(self, parsed_ser_mssg: list, *args):
        """
        Checks if ACK has been received and if so, updates mcu attributes following a config request

        Parameters:
            parsed_ser_mssg (list): Received serial response, parsed (should be ack char 0x06)
            *args (tuple of tuples): In each tuple is a sub_cmd (int) @ idx = 0 and sctMetaData raw data (tuple)
                                     @ idx = 1
        """
        if self.ackConfirmed(parsed_ser_mssg):
            if args[-1][-1][0] < len(self.sctsMetaDataList):       # Maybe change index zero for a method returning "sctIdx" attr index?
                args = args[::-1]
            for dataPacket in args:
                sub_cmd = dataPacket[0]
                sct_metadata = SctMetaData(*dataPacket[1])
                self.configBrdSubCmds[self.configBrdSubCmdsKeys[sub_cmd]](sct_metadata)

    def addingSection(self, sct_metadata: SctMetaData):
        """
        Take care of all mcu mgmt attributes updates when a new section is created

        Parameters:
            sct_metadata (SctMetaData): SctMetaData obj with all info related to the created section
        """
        try:
            self.sctsMetaDataList[sct_metadata.sctIdx] = sct_metadata
        except IndexError:
            self.sctsMetaDataList.append(sct_metadata)
        finally:
            self.sctsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.sctsMgmtMetaData.remaining,
                                                              self.sctsMgmtMetaData.assigned,
                                                              1)
            self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                              self.pxlsMgmtMetaData.assigned,
                                                              sct_metadata.pxlHeapBlocksCount())

    def editingSection(self, edit_sct_metadata: SctMetaData):
        """
        Handle all actions related to this class' attributes when editing a section

        Parameters:
            edit_sct_metadata (SctMetaData): A new SctMetaData obj representing the edited section and its new attr.
        """
        self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                          self.pxlsMgmtMetaData.assigned,
                                                          (edit_sct_metadata.pxlHeapBlocksCount() -
                                                           self.sctsMetaDataList[edit_sct_metadata.sctIdx].
                                                           pxlHeapBlocksCount()))
        self.sctsMetaDataList[edit_sct_metadata.sctIdx] = edit_sct_metadata

    def deletingSection(self, sct_metadata: SctMetaData):
        """
        Take care of all mcu mgmt attributes updates when a section is deleted

        Parameters:
            sct_metadata (SctMetaData): SctMetaData obj with all info related to the deleted section
        """
        self.sctsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.sctsMgmtMetaData.remaining,
                                                          self.sctsMgmtMetaData.assigned,
                                                          -1)
        self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                          self.pxlsMgmtMetaData.assigned,
                                                          -abs(self.sctsMetaDataList[sct_metadata.sctIdx]
                                                               .pxlHeapBlocksCount()))

    def shiftSection(self, sct_idx: int):
        """
        Called during a section deletion procedure to shift sections

        Parameters:
            sct_idx (int): Index of the section where to shift the next one (sct_idx + 1)
        """
        if self.sctsMetaDataList[sct_idx + 1].pixelCount:
            self.sctsMetaDataList[sct_idx].pixelCount = self.sctsMetaDataList[sct_idx + 1].pixelCount
            self.sctsMetaDataList[sct_idx].brightness = self.sctsMetaDataList[sct_idx + 1].brightness
            self.sctsMetaDataList[sct_idx].singlePxlCtrl = self.sctsMetaDataList[sct_idx + 1].singlePxlCtrl

    def clearSection(self, sct_idx: int):
        """
        Clear the section MetaDatas. A sort of shift used when the next section is either
        None or has empty attributes

        Parameters:
            sct_idx (int): Index of the section from which to clear attr.
        """
        self.sctsMetaDataList[sct_idx] = SctMetaData(sct_idx, 0, 0, 0)

    def sctMetaDataTupleFormat(self, sct_idx: int = -1):
        """
        Update the SctMetaData obj format to a tuple

        Parameters:
            sct_idx (int): section index of SctMetaData obj to return as tuple.
                           If no idx is given, the whole list is returned in tuple format (contained in a list)
        """
        if sct_idx == -1:
            container = []
            for obj in self.sctsMetaDataList:
                container.append(astuple(obj))
            return container
        return astuple(self.sctsMetaDataList[sct_idx])

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
                while True:
                    pass
        except IndexError as error:
            print(error)

    def snUpdtEmit(self, *args):
        pass

    def fwVerUpdtEmit(self, *args):
        pass

    def sctsMgmtUpdtEmit(self, *args):
        pass

    def pxlsMgmtUpdtEmit(self, *args):
        pass

    @property
    def serialNum(self):
        return self._serialNum

    @serialNum.setter
    def serialNum(self, new_serial: int):
        if not self.valCompare(new_serial, self.serialNum):
            self._serialNum = new_serial
            self.snUpdtEmit(self.serialNum)

    @property
    def fwVersion(self):
        return self._fwVersion

    @fwVersion.setter
    def fwVersion(self, new_version: str):
        if not self.valCompare(new_version, self.fwVersion):
            self._fwVersion = new_version
            self.fwVerUpdtEmit(self.fwVersion)

    @property
    def sctsMgmtMetaData(self) -> BrdMgmtMetaData:
        return self._sctsMgmtMetaData

    @sctsMgmtMetaData.setter
    def sctsMgmtMetaData(self, new_inst: BrdMgmtMetaData):
        if not self.valCompare(new_inst, self.sctsMgmtMetaData):
            self._sctsMgmtMetaData = new_inst
            self.sctsMgmtUpdtEmit(str(self.sctsMgmtMetaData.remaining))

    @property
    def pxlsMgmtMetaData(self) -> BrdMgmtMetaData:
        return self._pxlsMgmtMetaData

    @pxlsMgmtMetaData.setter
    def pxlsMgmtMetaData(self, new_inst: BrdMgmtMetaData):
        if not self.valCompare(new_inst, self.pxlsMgmtMetaData):
            self._pxlsMgmtMetaData = new_inst
            self.pxlsMgmtUpdtEmit(str(self.pxlsMgmtMetaData.remaining))

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
