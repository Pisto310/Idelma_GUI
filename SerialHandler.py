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
        self._rqstBoardInfos = {"cmd": "1", "reply_expected": True}
        self._setupSct =       {"cmd": "2", "reply_expected": True}                # 6 bytes of reply would pertain to scts and pxls mgmt?
        self._saveSctsConfig = {"cmd": "3", "reply_expected": True}
        self._ledColorChange = {"cmd": "4", "reply_expected": False}           # No reply bytes for the time being, visual indicator is sufficient
                                                                        # Command number might change in future

    # Method to request necessary board infos from MCU. Takes a BoardInfos instance as argument
    def boardInfosRqst(self, board: BoardInfos):
        self.sendRqst(self.rqstBoardInfos)
        while self.awaitingReply:                       # Maybe add timeout?
            if self.checkRqstStatus():
                board.allAttrUpdate(self.serial.rxBuffer)
                self.rqstComplete()

    # Method to create/setup a new section by passing the desired number of LEDs to be contained in it
    def setupSctRqst(self, led_count, board: BoardInfos):
        self.sendRqst(self.setupSct, numLED=str(led_count))
        while self.awaitingReply:
            if self.checkRqstStatus():
                board.updtSctsInfo(self.serial.rxBuffer[:3])
                board.updtPxlsInfo(self.serial.rxBuffer[3:])
                self.rqstComplete()

    # Method used to save sections configurations
    def saveSctsConfigRqst(self, board: BoardInfos):
        self.sendRqst(self.saveSctsConfig)
        while self.awaitingReply:
            if self.checkRqstStatus():
                print("Sections configuration successfully saved")
                board.sctsConfigSaved = not board.sctsConfigSaved
                self.rqstComplete()

    def ledColorChangeRqst(self, section, pixel, rgb_color, white_val):
        self.sendRqst(self.ledColorChange, sctNbr=section, pxlNbr=pixel, rgbCastColor=rgb_color, whiteCastVal=white_val)





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
    def awaitingReply(self, toggle_bool):
        if toggle_bool is False or toggle_bool is True:
            self._awaitingReply = toggle_bool
        else:
            raise ValueError("Attribute is a boolean, no other value accepted")

    @property
    def rqstBoardInfos(self):
        return self._rqstBoardInfos

    @property
    def setupSct(self):
        return self._setupSct

    @property
    def saveSctsConfig(self):
        return self._saveSctsConfig

    @property
    def ledColorChange(self):
        return self._ledColorChange
