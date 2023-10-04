from UsrSerial import *
from BoardInfos import BoardInfos


class SerialHandler:
    """Class to be used for handling
    all things serial with the MCU
    """

    def __init__(self, serial_port):

        self.serial = UsrSerial(port=serial_port)

        self._awaitingReply = False

        # Below are all commands for metadata (0-9 reserved)
        self.serialNum   = "1"
        self.fwVersion   = "2"
        self.sctsBrdMgmt = "3"
        self.pxlsBrdMgmt = "4"
        # self._serialNum   = {"cmd": "1", "reply_expected": True}
        # self._fwVersion   = {"cmd": "2", "reply_expected": True}
        # self._sctsBrdMgmt = {"cmd": "3", "reply_expected": True}
        # self._pxlsBrdMgmt = {"cmd": "4", "reply_expected": True}

        # Commands necessitating the MCU to send an ACK
        self.configBrdCmd = "10"
        # self._configBrdCmd = {"cmd": "10", "reply_expected": True}

        self.ack = 6

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
        # self.serial.writeToPort(self.serial.txDataParsing("1"))
        # self.awaitingReply = True
        #
        # while self.awaitingReply:
        #     if self.checkRqstStatus():
        #         self.serial.rxMessageParsing()
        #         pass
        """-----     debug    -----"""

        self.serialNumRqst(board_inst)
        self.fwVersionRqst(board_inst)
        self.sctsBrdMgmtRqst(board_inst)
        self.pxlsBrdMgmtRqst(board_inst)

    def configBrdRqst(self, board_inst: BoardInfos, *args):
        """
        Sends all the necessary sections info to configure board

        Parameters:
            board_inst (BoardInfos): a BoardInfos obj to updt attr after config
            *args (tuple): a tuple containing the sections info (a tuple for each scts)
        """
        self.serRqst(self.configBrdCmd, board_inst.configBrdUpdt, *args)

    def serRqst(self, serial_command, func_cb, *args):
        """
        Method used to set-up a serial request

        Parameters:
            serial_command (str): The serial command, normally an int, as a string
            func_cb: A callback function to interpret the message received
            *args: Additional info (an iterable of integers)
        """
        self.serial.confirmCmd(serial_command)
        self.sendRqst(*args)
        while self.awaitingReply:
            if self.checkRqstStatus():
                func_cb(self.serial.rxMessageParsing(), *args)
                self.rqstComplete()

    def sendRqst(self, *args):
        if not self.awaitingReply:
            if args:
                self.serial.txDataParsing(*args)
            self.serial.sendTxBuffer()
            self.awaitingReply = True
            self.notifyRxerEmit()
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

    def notifyRxerEmit(self):
        """
        To be implemented in children classes
        """
        pass

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

    # @property
    # def serialNum(self):
    #     return self._serialNum
    #
    # @property
    # def fwVersion(self):
    #     return self._fwVersion
    #
    # @property
    # def sctsBrdMgmt(self):
    #     return self._sctsBrdMgmt
    #
    # @property
    # def pxlsBrdMgmt(self):
    #     return self._pxlsBrdMgmt
    #
    # @property
    # def configBrdCmd(self):
    #     return self._configBrdCmd
    # # def configBrd(self):
    # #     return self._configBrd
