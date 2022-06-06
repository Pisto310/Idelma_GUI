from UsrSerial import *
from BoardInfos import BoardInfos


class SerialHandler:
    """Class to be used for handling
    all things serial with the MCU
    """

    def __init__(self):

        self.serial = UsrSerial()

        self._awaitingReply = False

        # Below are all commands
        self._serialNum   = {"cmd": "1", "reply_expected": True}
        self._fwVersion   = {"cmd": "2", "reply_expected": True}
        self._sctsBrdMgmt = {"cmd": "3", "reply_expected": True}
        self._pxlsBrdMgmt = {"cmd": "4", "reply_expected": True}

        # self._boardInfos     = {"cmd": "1", "reply_expected": True}
        # self._sectionInfoArr = {"cmd": "2", "reply_expected": True}
        # self._setupSct       = {"cmd": "3", "reply_expected": True}
        # self._saveSctsConfig = {"cmd": "4", "reply_expected": True}
        # self._ledColorChange = {"cmd": "5", "reply_expected": False}

    def serRqst(self, serial_command, board_inst_func_cb):
        self.sendRqst(serial_command)
        while self.awaitingReply:
            if self.checkRqstStatus():
                board_inst_func_cb(self.serial.messageParsing())
                self.rqstComplete()

    def serialNumRqst(self, board_inst: BoardInfos):
        self.serRqst(self.serialNum, board_inst.serialNumSet)

    def fwVersionRqst(self, board_inst: BoardInfos):
        self.serRqst(self.fwVersion, board_inst.fwVersionSet)

    def sctsBrdMgmtRqst(self, board_inst: BoardInfos):
        self.serRqst(self.sctsBrdMgmt, board_inst.sctsBrdMgmtSet)

    def pxlsBrdMgmtRqst(self, board_inst: BoardInfos):
        self.serRqst(self.pxlsBrdMgmt, board_inst.pxlsBrdMgmtSet)

    def getAllBrdInfos(self, board_inst: BoardInfos):
        self.serialNumRqst(board_inst)
        self.fwVersionRqst(board_inst)
        self.sctsBrdMgmtRqst(board_inst)
        self.pxlsBrdMgmtRqst(board_inst)

    # # Method to request necessary board infos from MCU
    # def boardInfosRqst(self, board):
    #     self.sendRqst(self.boardInfos)
    #     while self.awaitingReply:                       # Maybe add timeout?
    #         if self.checkRqstStatus():
    #             board = BoardInfos(*self.serial.messageParsing())
    #             self.rqstComplete()
    #     return board
    #
    # def sctInfoArrRqst(self):
    #     self.sendRqst(self.sectionInfoArr)
    #     while self.awaitingReply:                       # Maybe add timeout?
    #         if self.checkRqstStatus():
    #             print(self.serial.rxBuffer)
    #             self.rqstComplete()
    #
    # # Method to create/setup a new section by passing the desired number of LEDs to be contained in it
    # def setupSctRqst(self, led_count, board: BoardInfos):
    #     self.sendRqst(self.setupSct, numLED=str(led_count))
    #     while self.awaitingReply:
    #         if self.checkRqstStatus():
    #             board.updtSctsInfo(self.serial.rxBuffer[:3])
    #             board.updtPxlsInfo(self.serial.rxBuffer[3:])
    #             self.rqstComplete()
    #
    # # Method used to save sections configurations
    # def saveSctsConfigRqst(self):
    #     self.sendRqst(self.saveSctsConfig)
    #     while self.awaitingReply:
    #         if self.checkRqstStatus():
    #             print("Sections configuration successfully saved")
    #             self.rqstComplete()
    #
    # def ledColorChangeRqst(self, section, pixel, rgb_color, white_val):
    #     self.sendRqst(self.ledColorChange, sctNbr=section, pxlNbr=pixel, rgbCastColor=rgb_color, whiteCastVal=white_val)

    def sendRqst(self, command_dict, **kwargs):
        if not self.awaitingReply:
            if not kwargs:
                self.serial.writeToPort(command_dict.get("cmd"))
            else:
                self.serial.writeToPort(self.serial.concatenateData(command_dict.get("cmd"), **kwargs))
            if command_dict.get("reply_expected"):
                self.awaitingReply = True
        else:
            print("Serial port already busy with pending request")

    def checkRqstStatus(self):
        if self.awaitingReply:
            self.serial.readPort()
        if len(self.serial.rxBuffer):
            return True
        else:
            return False

    def rqstComplete(self):
        self.awaitingReply = False
        self.serial.clearBuffer()

    """
    This section for attributes' getters, setters and delete
    """
    @property
    def awaitingReply(self):
        return self._awaitingReply

    @awaitingReply.setter
    def awaitingReply(self, toggle_bool: bool):
        if toggle_bool is False or toggle_bool is True:
            self._awaitingReply = toggle_bool
        else:
            raise ValueError("Attribute must be a boolean, no other type accepted")

    @property
    def serialNum(self):
        return self._serialNum

    @property
    def fwVersion(self):
        return self._fwVersion

    @property
    def sctsBrdMgmt(self):
        return self._sctsBrdMgmt

    @property
    def pxlsBrdMgmt(self):
        return self._pxlsBrdMgmt

    # @property
    # def boardInfos(self):
    #     return self._boardInfos
    #
    # @property
    # def sectionInfoArr(self):
    #     return self._sectionInfoArr
    #
    # @property
    # def setupSct(self):
    #     return self._setupSct
    #
    # @property
    # def saveSctsConfig(self):
    #     return self._saveSctsConfig
    #
    # @property
    # def ledColorChange(self):
    #     return self._ledColorChange
