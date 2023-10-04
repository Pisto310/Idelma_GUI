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
        self.spaceChar = 32

    def sendTxBuffer(self):
        self.txBuffer += chr(self.lineFeed)
        print(list(bytes(self.txBuffer, 'utf-8')))
        self.write(bytes(self.txBuffer, 'utf-8'))
        time.sleep(0.05)

    def readPort(self):
        """
        Reading serial port until a line feed char is met
        """
        self.rxBuffer = list(self.readline())

    def clearBuffer(self):
        self.rxBuffer = []

    def confirmCmd(self, str_cmd):
        """
        First method to be called when sending a serial packet from the PC
        to the MCU. It ensures the txBuffer is reset and adds the cmd as
        the first (few) byte(s) of the transmission
        """
        self.resetTxBuffer()
        self.txBuffer += str_cmd[::-1]

    def resetTxBuffer(self):
        """
        Simply resets the txBuffer by assigning an empty string to it
        """
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
            if not val == self.spaceChar and not val == self.lineFeed:
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
        If called, it is after confirmCmd or else an AssertionError is raised.
        It will fill out the txBuffer with additional info necessary for the
        MCU to process the command
        """
        if len(self.txBuffer) != 0:
            for index, val in enumerate(args):
                if hasattr(val, '__iter__') and len(val) > 1:
                    self.txDataParsing(*val)
                else:
                    if not isinstance(val, str):
                        val = str(val)
                    self.txBuffer += chr(self.spaceChar) + val[::-1]
                # Condition to check for length of txBuffer == 63 && how much more bytes there are to write in buffer
                # This is to ensure that each transmission doesn't overflow the 64 bytes limit on serial blocks
        else:
            raise AssertionError("Transmission buffer must contain a specific serial command")

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



