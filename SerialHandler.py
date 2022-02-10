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
        self._rqstBoardInfos = {"cmd": "0", "reply_bytes": 9}  # cmd will be replaced by BRD
        self._createSctCmd = "1"        # Will be replace by NEW

    def boardInfosRqst(self):
        self.sendRqst(self.rqstBoardInfos)

    def sendRqst(self, command_dict):
        if not self.awaitingReply:
            for i, key in enumerate(command_dict):
                if i == 0:
                    self.serial.writeToPort(command_dict.get(key))
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
            self.rqstComplete()

    def rqstComplete(self):
        self.awaitingReply = False
        self.replySize = 0

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
