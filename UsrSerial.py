import time

from serial import *
from time import sleep


class UsrSerial(Serial):
    """
    A serial class inherited from the pySerial
    module. Done so that methods and attributes can
    be added to the convenience of the dev
    """

    def __init__(self, port='/dev/cu.usbmodem14101', baudrate=9600, timeout=0.075, serial_wait=1.2):
        super().__init__(port=port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE,
                         stopbits=STOPBITS_ONE, timeout=timeout, xonxoff=False, rtscts=False,
                         write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        time.sleep(serial_wait)     # To allow Arduino to RST

        self._rxBuffer = []
        self.parsedMssg = []

    # Method to call to write on serial port
    def writeToPort(self, serial_data):
        print(list(bytes(serial_data, 'utf-8')))
        self.write(bytes(serial_data, 'utf-8'))
        time.sleep(0.05)

    # reading Rx buffer is based on the fact that there is always a 'line feed' (\n) char in a serial transmission
    def readPort(self):
        self.rxBuffer = list(self.readline())

    def clearBuffer(self):
        self.rxBuffer = []

    # Method for parsing the bytes received through serial. Since all digits are separated, it is useful to know they
    # are organized in a "little endian" manner. This means that the unit number has a lower index in the list than the
    # tens and hundreds. Easier to process that way
    def messageParsing(self):
        spaceChar = 32
        lineFeed = 10
        unitsTracker = 0
        recomposedNbr = 0
        msg_container = []
        for index, val in enumerate(self.rxBuffer):
            if val == spaceChar:
                msg_container.append(recomposedNbr)
                unitsTracker = 0
                recomposedNbr = 0
            elif val == lineFeed:
                break
            else:
                recomposedNbr += val * (10 ** unitsTracker)
                unitsTracker += 1
        return msg_container

    @staticmethod
    def concatenateData(initial_data, **kwargs):
        updated_data = initial_data
        for arg in kwargs.values():
            updated_data += arg
        return updated_data

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




