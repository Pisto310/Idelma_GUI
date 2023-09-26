import time

from serial import *
from time import sleep


class UsrSerial(Serial):
    """
    A serial class inherited from the pySerial
    module. Done so that methods and attributes can
    be added to the convenience of the dev
    """

    def __init__(self, port, baudrate=9600, timeout=0.075, serial_wait=1.2):
        super().__init__(port=port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE,
                         stopbits=STOPBITS_ONE, timeout=timeout, xonxoff=False, rtscts=False,
                         write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        time.sleep(serial_wait)     # To allow Arduino to RST

        self.bufferSizeLim = 64

        self._rxBuffer = []
        self.txBuffer = ''

        self.lineFeed = 10
        self.groupSeparator = 29
        self.unitSeparator = 31

    def writeToPort(self, serial_data):
        """
        Write a set of data to the serial port
        Using python serial module separates each bytes for us
        """
        serial_data += chr(self.lineFeed)
        print(list(bytes(serial_data, 'utf-8')))
        self.write(bytes(serial_data, 'utf-8'))
        time.sleep(0.05)
        # Erase tx buffer here

    def readPort(self):
        """
        Reading serial port until a line feed char is met
        """
        self.rxBuffer = list(self.readline())

    def clearBuffer(self):
        self.rxBuffer = []

    def confirmCmd(self, str_cmd):
        self.resetTxBuffer()
        self.txBuffer += str_cmd[::-1]
        pass

    def resetTxBuffer(self):
        self.txBuffer = ''

    def rxMessageParsing(self):
        """
        Method to parse bytes received through serial. Bytes ar broken into single digits,
        separated by space char (0x20) and arranged in a little endian format
        """
        unitsTracker = 0
        recomposedNbr = 0
        msg_container = []
        for index, val in enumerate(self.rxBuffer):
            if not val == self.unitSeparator and not val == self.lineFeed:
                recomposedNbr += val * (10 ** unitsTracker)
                unitsTracker += 1
            else:
                if unitsTracker:
                    msg_container.append(recomposedNbr)
                    unitsTracker = 0
                    recomposedNbr = 0
                if val == self.lineFeed:
                    break
        print(msg_container)
        return msg_container

    def txDataParsing(self, *args):
        """
        """
        self.txBuffer += chr(self.groupSeparator)
        for index, val in enumerate(args):
            if not isinstance(val, str):
                val = str(val)
            self.txBuffer += val[::-1]
            if index != (len(args) - 1):
                self.txBuffer += chr(self.unitSeparator)

    """
    This section for attributes' getters, setters and delete
    """
    @property
    def rxBuffer(self):
        return self._rxBuffer

    @rxBuffer.setter
    def rxBuffer(self, new_list):
        if type(new_list) != list:
            raise TypeError("Should pass a list as argument")
        else:
            self._rxBuffer = new_list
