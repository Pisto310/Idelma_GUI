from UsrSerial import *
from BoardMetaDatas import BoardMetaDatas


class SerialHandler:
    """Class to be used for handling
    all things serial with the MCU
    """

    def __init__(self, serial_port):

        self.serial = UsrSerial(port=serial_port)

        self._awaitingReply = False

        self.serialRqsts = {"serial_num":          "1",
                            "fw_version":          "2",
                            "scts_mgmt_metadata":  "3",
                            "pxls_mgmt_metadata":  "4",
                            "scts_metadata":       "5",
                            "config_board":        "10",
                            "save_settings":       "20",
                            "all_pixels_off":      "254",
                            "reset_eeprom":        "255"}

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
        """
        Parse serial message if additional arguments are to be sent with cmd.
        Empties TX buffer through serial port and triggers awaitingReply var

        Parameters:
            args (bytes): additional bytes to send along cmd byte
        """
        if not self.awaitingReply:
            if args:
                self.serial.txDataParsing(*args)
            self.serial.sendTxBuffer()
            self.awaitingReply = True
            self.notifyRxerEmit()
        else:
            print("Serial port already busy with pending request")

    def checkRqstStatus(self):
        """
        Scans the serial port periodically while the prog is awaiting the MCU's reply
        """
        if self.awaitingReply:
            self.serial.readPort()
        if len(self.serial.rxBuffer):
            return True
        else:
            return False

    def rqstComplete(self):
        """
        Called when a serial rqst is completed to reset important attr.
        """
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
