from NonSerSctMetaData import NonSerSctMetaData
from BrdMgmtMetaData import BrdMgmtMetaData
from SctMetaData import SctMetaData

from dataclasses import astuple


class BoardInfos:
    """
    This class contains all the board info
    as attributes and all associated methods
    to get, set and more
    """
    def __init__(self):

        self._serialNum        = None
        self._fwVersion        = None
        self._sctsMgmtMetaData = None
        self._pxlsMgmtMetaData = None

        self.sctsMetaDataList = []

        # self.configBrdByteToFunc = {NonSerSctMetaData.infoTupleIndexes.get('pixel_count_index'): self.pixelBlockAssig}

        self.ackChar = 6

    def __eq__(self, other):
        if not isinstance(other, BoardInfos):
            return NotImplemented
        return (self.serialNum == other.serialNum and
                self.fwVersion == other.fwVersion and
                self.sctsMgmtMetaData == other.sctsMgmtMetaData and
                self.pxlsMgmtMetaData == other.pxlsMgmtMetaData)

    def __ne__(self, other):
        return not self == other

    # Method used to set the serial number of the board using the parsed message received in the serial buffer
    def serialNumUpdt(self, parsed_ser_mssg: list):
        hex_container = 0
        for index, val in enumerate(parsed_ser_mssg):
            hex_container += val << (8 * index)
        self.serialNum = hex(hex_container)

    # Method to set the FW version with the parsed message of the serial buffer
    def fwVersionUpdt(self, parsed_ser_mssg: list):
        str_container = ""
        for index, val in enumerate(parsed_ser_mssg):
            str_container += str(val)
            if (index + 1) < len(parsed_ser_mssg):
                str_container += "."
        self.fwVersion = str_container

    def sctsMgmtUpdt(self, parsed_ser_mssg: list):
        self.sctsMgmtMetaData = BrdMgmtMetaData(*parsed_ser_mssg)

    def pxlsMgmtUpdt(self, parsed_ser_mssg: list):
        self.pxlsMgmtMetaData = BrdMgmtMetaData(*parsed_ser_mssg)

    def setSctInfosTuple(self, parsed_ser_mssg: list):
        """
        Fill the sctInfoTuple list with the rxed SctInfoArr to initialize the GUI
        according to the saved set-up of the board. Only called in fetchBrdMetaDatas
        method of IdelmaApp obj

        Parameters:
            parsed_ser_mssg (list): list containing the sectionInfoArr array, which
                                    is composed of section_info_t structs of len =
                                    core_data_len
        """
        core_data_len = 2
        idx = 0
        while idx < len(parsed_ser_mssg):
            sct_Id = int(idx / core_data_len)
            self.sctsMetaDataList.append((sct_Id, parsed_ser_mssg[idx]))
            idx += core_data_len
        self.sctsInfoTupleEmit(self.sctsMetaDataList)

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
            sct_id_index = NonSerSctMetaData.infoTupleIndexes.get('sctID_index')
            pxl_count_index = NonSerSctMetaData.infoTupleIndexes.get('pixelCount_index')
            for sctInfoTuple in args:
                try:
                    sct_id = sctInfoTuple[sct_id_index]
                    pxl_count_diff = sctInfoTuple[pxl_count_index] - self.sctsMetaDataList[sct_id][pxl_count_index]
                    pxl_total_blocks += pxl_count_diff
                    if not sctInfoTuple[pxl_count_index]:
                        sct_total_blocks -= 1
                        self.sctsMetaDataList.pop(sct_id)
                        continue
                    self.sctsMetaDataList[sct_id] = (sct_id, sctInfoTuple[pxl_count_index])
                except IndexError:
                    if sctInfoTuple[pxl_count_index]:
                        sct_total_blocks += 1
                        pxl_total_blocks += sctInfoTuple[pxl_count_index]
                        self.sctsMetaDataList.append(sctInfoTuple)
            if sct_total_blocks:
                self.sctsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.sctsMgmtMetaData.capacity,
                                                                  self.sctsMgmtMetaData.remaining,
                                                                  self.sctsMgmtMetaData.assigned,
                                                                  sct_total_blocks)
            if pxl_total_blocks:
                self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.capacity,
                                                                  self.pxlsMgmtMetaData.remaining,
                                                                  self.pxlsMgmtMetaData.assigned,
                                                                  pxl_total_blocks)

    def addingSection(self, sct_metadata: SctMetaData):
        """
        Take care of all board mgmt attributes updates when a new section is created

        Parameters:
            sct_metadata (SctMetaData): SctMetaData obj with all info related to the created section
        """
        real_pxl_count = sct_metadata.pixelCount
        if sct_metadata.singlePxlCtrl:
            real_pxl_count = sct_metadata.singlePxlCtrl
        self.sctsMetaDataList.append(sct_metadata)
        self.sctsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.sctsMgmtMetaData.remaining,
                                                          self.sctsMgmtMetaData.assigned,
                                                          1)
        self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                          self.pxlsMgmtMetaData.assigned,
                                                          real_pxl_count)

    def deletingSection(self, sct_metadata: SctMetaData):
        """
        Take care of all board mgmt attributes updates when a section is deleted

        Parameters:
            sct_metadata (SctMetaData): SctMetaData obj with all info related to the deleted section
        """
        real_pxl_count = sct_metadata.pixelCount
        if sct_metadata.singlePxlCtrl:
            real_pxl_count = sct_metadata.singlePxlCtrl
        self.sctsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.sctsMgmtMetaData.remaining,
                                                          self.sctsMgmtMetaData.assigned,
                                                          -1)
        self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                          self.pxlsMgmtMetaData.assigned,
                                                          -abs(real_pxl_count))

    def editingSection(self, edit_sct_metadata: SctMetaData):
        """
        Handle all actions related to this class' attributes when editing a section

        Parameters:
            edit_sct_metadata (SctMetaData): A new SctMetaData obj representing the edited section and its new attr.
        """
        pxl_diff = edit_sct_metadata.pixelCount - self.sctsMetaDataList[edit_sct_metadata.sctIdx].pixelCount
        if edit_sct_metadata.singlePxlCtrl and self.sctsMetaDataList[edit_sct_metadata.sctIdx].singlePxlCtrl:
            pxl_diff = 0
        elif edit_sct_metadata.singlePxlCtrl and not self.sctsMetaDataList[edit_sct_metadata.sctIdx].singlePxlCtrl:
            pxl_diff = edit_sct_metadata.singlePxlCtrl - self.sctsMetaDataList[edit_sct_metadata.sctIdx].pixelCount
        elif not edit_sct_metadata.singlePxlCtrl and self.sctsMetaDataList[edit_sct_metadata.sctIdx].singlePxlCtrl:
            pxl_diff = edit_sct_metadata.pixelCount - self.sctsMetaDataList[edit_sct_metadata.sctIdx].singlePxlCtrl
        self.pxlsMgmtMetaData = BrdMgmtMetaData.blockUpdt(self.pxlsMgmtMetaData.remaining,
                                                          self.pxlsMgmtMetaData.assigned,
                                                          pxl_diff)
        self.sctsMetaDataList[edit_sct_metadata.sctIdx] = edit_sct_metadata

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

    def sctsInfoTupleEmit(self, *args):
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
            self.sctsMgmtUpdtEmit(self.sctsMgmtMetaData)

    @property
    def pxlsMgmtMetaData(self) -> BrdMgmtMetaData:
        return self._pxlsMgmtMetaData

    @pxlsMgmtMetaData.setter
    def pxlsMgmtMetaData(self, new_inst: BrdMgmtMetaData):
        if not self.valCompare(new_inst, self.pxlsMgmtMetaData):
            self._pxlsMgmtMetaData = new_inst
            self.pxlsMgmtUpdtEmit(self.pxlsMgmtMetaData)

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
