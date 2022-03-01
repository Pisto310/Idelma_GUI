from UsrSerial import *


class SerialHandler:
    """Class to be used for handling
    all things serial with the MCU
    """

    def __init__(self):

        self.serial = UsrSerial()

        self._awaitingReply = False
        self._replySize = 0

        # Below are all commands and the MCU number of bytes to respond
        self._rqstBoardInfos = {"cmd": "1", "reply_bytes": 9}
        self._setupSct = {"cmd": "2", "reply_bytes": 1}                # 6 bytes of reply would pertain to scts and pxls mgmt?

    # Method to request necessary board infos from MCU. Takes a BoardInfos instance as argument
    def boardInfosRqst(self, board_info_instance):
        self.sendRqst(self.rqstBoardInfos)
        while self.awaitingReply:                       # Maybe add timeout?
            if self.checkRqstStatus():
                board_info_instance.allAttrUpdate(self.serial.rxBuffer)
                self.rqstComplete()

    # Method to create/setup a new section by passing the desired number of LEDs to be contained in it
    def setupSctRqst(self, led_count):
        self.sendRqst(self.setupSct, numLED=str(led_count))
        while self.awaitingReply:
            if self.checkRqstStatus():

                self.rqstComplete()

    def sendRqst(self, command_dict, **kwargs):
        if not self.awaitingReply:
            for i, key in enumerate(command_dict):
                if i == 0:
                    if not kwargs:
                        self.serial.writeToPort(command_dict.get(key))
                    else:
                        self.serial.writeToPort(self.serial.concatenateData(command_dict.get(key), **kwargs))
                elif i == 1:
                    if command_dict.get(key):
                        self.replySize = command_dict.get(key)
                        self.awaitingReply = True
        else:
            print("Serial port already busy with pending request")

    def checkRqstStatus(self):
        if self.awaitingReply:
            self.serial.readPort(self.replySize)
        if len(self.serial.rxBuffer):
            return True
        else:
            return False

    def rqstComplete(self):
        self.awaitingReply = False
        self.replySize = 0
        self.serial.clearBuffer()

    """
    This section for attributes' getters, setters and delete
    """
    @property
    def awaitingReply(self):
        return self._awaitingReply

    @awaitingReply.setter
    def awaitingReply(self, toggle_bool):
        if toggle_bool == False or toggle_bool == True:
            self._awaitingReply = toggle_bool
        else:
            raise ValueError("Attribute is a boolean, no other value accepted")

    @property
    def replySize(self):
        return self._replySize

    @replySize.setter
    def replySize(self, new_size):
        if new_size < 0:
            raise ValueError("Cannot expect negative bytes on serial bus")
        else:
            self._replySize = new_size

    @property
    def rqstBoardInfos(self):
        return self._rqstBoardInfos

    @property
    def setupSct(self):
        return self._setupSct
