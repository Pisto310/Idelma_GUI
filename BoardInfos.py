import numpy as np


class BoardInfos:
    """
    This class will contains all the board
    infos as attributes and all associated methods.
    to get, set and more
    """

    def __init__(self):

        self._serialNum = 0
        self._fwVersion = 0
        self.sctsInfo = {
            "capacity": 0,
            "remaining": 0,
            "assigned": 0
        }
        self.pxlsInfo = {
            "capacity": 0,
            "remaining": 0,
            "assigned": 0
        }

    def allAttrUpdate(self, updated_infos_list):
        self.serialNum = updated_infos_list[0]
        self.fwVersion = updated_infos_list[1] + (updated_infos_list[2]/10)
        for i, key in enumerate(self.sctsInfo):
            if i == 0:
                self.sctsInfo[key] = updated_infos_list[3]
            if i == 1:
                self.sctsInfo[key] = updated_infos_list[4]
            if i == 2:
                self.sctsInfo[key] = updated_infos_list[5]

        for i, key in enumerate(self.pxlsInfo):
            if i == 0:
                self.pxlsInfo[key] = updated_infos_list[6]
            if i == 1:
                self.pxlsInfo[key] = updated_infos_list[7]
            if i == 2:
                self.pxlsInfo[key] = updated_infos_list[8]

    @property
    def serialNum(self):
        return self._serialNum

    @serialNum.setter
    def serialNum(self, new_serial):
        self._serialNum = new_serial

    @property
    def fwVersion(self):
        return self._fwVersion

    @fwVersion.setter
    def fwVersion(self, new_version):
        self._fwVersion = new_version

    # @property
    # def sctsInfo(self):
    #     return self.sctsInfo
    #
    # @sctsInfo.setter
    # def sctsInfo(self, scts_infos_update):
    #     # Let's first check if argument passed is iterable
    #     if np.iterable(scts_infos_update):
    #         for index, key in enumerate(self.sctsInfo):
    #             # Just need to be updated on first Get Board Info pass
    #             if key == "capacity" and self.sctsInfo[key] == 0:
    #                 # We know for a fact that the capacity can't exceed 12 for Mega2560 board
    #                 if 0 < scts_infos_update[index] <= 12:
    #                     self.sctsInfo[key] = scts_infos_update[index]
    #                 else:
    #                     print("capacity exceeds self-imposed limit of 12 pins")
    #             elif key == "assigned":
    #                 if 0 <= scts_infos_update[index] <= self.sctsInfo["capacity"]:
    #                     self.sctsInfo[key] = scts_infos_update[index]
    #                 else:
    #                     print("cannot assign more than the board capacity of {} sections"
    #                           .format(self.sctsInfo["capacity"]))
    #             elif key == "remaining":
    #                 if 0 < scts_infos_update[index] <= self.sctsInfo["capacity"] and \
    #                         scts_infos_update[index] == (self.sctsInfo["capacity"] - self.sctsInfo["assigned"]):
    #                     self.sctsInfo[key] = scts_infos_update[index]
    #     else:
    #         print("argument passed isn't iterable, can't proceed with attribute update")

    # @property
    # def pxlsInfo(self):
    #     return self.pxlsInfo

    # @pxlsInfo.setter
    # def pxlsInfo(self, pxls_infos_update):
    #     # Let's first check if argument passed is iterable
    #     if np.iterable(pxls_infos_update):
    #         for index, key in enumerate(self.pxlsInfo):
    #             # Just need to be updated on first Get Board Info pass
    #             if key == "capacity" and self.pxlsInfo[key] == 0:
    #                 # We know for a fact that the capacity can't exceed 12 for Mega2560 board
    #                 if 0 < pxls_infos_update[index] <= 100:
    #                     self.pxlsInfo[key] = pxls_infos_update[index]
    #                 else:
    #                     print("capacity exceeds self-imposed heap space of pixel_info struct of a 100")
    #             elif key == "assigned":
    #                 if 0 <= pxls_infos_update[index] <= self.pxlsInfo["capacity"]:
    #                     self.pxlsInfo[key] = pxls_infos_update[index]
    #                 else:
    #                     print("cannot assign more than the board capacity of {} sections"
    #                           .format(self.pxlsInfo["capacity"]))
    #             elif key == "remaining":
    #                 if 0 < pxls_infos_update[index] <= self.pxlsInfo["capacity"] and \
    #                         pxls_infos_update[index] == (self.pxlsInfo["capacity"] - self.pxlsInfo["assigned"]):
    #                     self.pxlsInfo[key] = pxls_infos_update[index]
    #     else:
    #         print("argument passed isn't iterable, can't proceed with attribute update")

