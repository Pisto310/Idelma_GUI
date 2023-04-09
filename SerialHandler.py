import serial.serialutil
from serial.tools.list_ports_osx import comports

from UsrSerial import *
from BoardInfos import BoardInfos


class SerialHandler:
    """Class to be used for handling
    all things serial with the MCU
    """

    def __init__(self):

        self.serial = None
        # self.serial = UsrSerial()

        self._awaitingReply = False

        # Below are all commands
        self._serialNum   = {"cmd": "1", "reply_expected": True}
        self._fwVersion   = {"cmd": "2", "reply_expected": True}
        self._sctsBrdMgmt = {"cmd": "3", "reply_expected": True}
        self._pxlsBrdMgmt = {"cmd": "4", "reply_expected": True}
        self._sctSetup    = {"cmd": "5", "reply_expected": False}

        self.openSerialPort()

        # self._boardInfos     = {"cmd": "1", "reply_expected": True}
        # self._sectionInfoArr = {"cmd": "2", "reply_expected": True}
        # self._setupSct       = {"cmd": "3", "reply_expected": True}
        # self._saveSctsConfig = {"cmd": "4", "reply_expected": True}
        # self._ledColorChange = {"cmd": "5", "reply_expected": False}

    def openSerialPort(self):
        try:
            # Might be useful to list all available serial ports and choose which one to open
            #   for ports in comports():
            #       print(ports)
            self.serial = UsrSerial(port='/dev/cu.usbmodem14101')
        except serial.serialutil.SerialException:
            self.serial = UsrSerial(port=None)

    def serialNumRqst(self, board_inst: BoardInfos):
        self.serRqst(self.serialNum, board_inst.serialNumMssgDecode)

    def fwVersionRqst(self, board_inst: BoardInfos):
        self.serRqst(self.fwVersion, board_inst.fwVersionMssgDecode)

    def sctsBrdMgmtRqst(self, board_inst: BoardInfos):
        self.serRqst(self.sctsBrdMgmt, board_inst.sctsBrdMgmtMssgDecode)

    def pxlsBrdMgmtRqst(self, board_inst: BoardInfos):
        self.serRqst(self.pxlsBrdMgmt, board_inst.pxlsBrdMgmtMssgDecode)

    def getAllBrdInfos(self, board_inst: BoardInfos):

        """-----     debug    -----"""
        # self.serial.writeToPort(self.serial.concatenateData("1"))
        # self.awaitingReply = True
        #
        # while self.awaitingReply:
        #     if self.checkRqstStatus():
        #         self.serial.messageParsing()
        #         pass
        """-----     debug    -----"""

        self.serialNumRqst(board_inst)
        self.fwVersionRqst(board_inst)
        self.sctsBrdMgmtRqst(board_inst)
        self.pxlsBrdMgmtRqst(board_inst)

    # For this method, each device (arduino and PC) will update the board infos on their own. To signal that everything
    # was done right in the MCU, it will respond with an ACK (defined as 6 in the ascii table). From there, the PC will
    # update the board info back in the SectionEditWin class
    def sctSetupRqst(self, board_inst: BoardInfos, led_count: int, single_pixel: bool):
        self.serRqst(self.sctSetup, board_inst.sctSetupUpdt, led_count, single_pixel)

    def serRqst(self, serial_command, board_inst_func_cb, *args):
        self.sendRqst(serial_command, *args)
        while self.awaitingReply:
            if self.checkRqstStatus():
                board_inst_func_cb(self.serial.messageParsing(), *args)
                self.rqstComplete()

    def sendRqst(self, command_dict, *args):
        if not self.awaitingReply:
            if not args:
                self.serial.writeToPort(command_dict.get("cmd"))
            else:
                self.serial.writeToPort(self.serial.txDataEncoding(command_dict.get("cmd"), *args))
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

    @property
    def sctSetup(self):
        return self._sctSetup