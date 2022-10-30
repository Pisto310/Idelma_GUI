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

        self._lineFeed = 10
        self._spaceChar = 32

    # Method to call to write on serial port
    def writeToPort(self, serial_data):
        serial_data += chr(self._lineFeed)
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
        unitsTracker = 0
        recomposedNbr = 0
        msg_container = []
        for index, val in enumerate(self.rxBuffer):
            if not val == self._spaceChar and not val == self._lineFeed:
                recomposedNbr += val * (10 ** unitsTracker)
                unitsTracker += 1
            else:
                if unitsTracker:
                    msg_container.append(recomposedNbr)
                    unitsTracker = 0
                    recomposedNbr = 0
                if val == self._lineFeed:
                    break
        print(msg_container)
        return msg_container

    # Used to add numbers to the serial command to send. Padding 0 bytes are added to numbers that aren't big enough to
    # to respect the hundreds, tens and unit format for ease of processing and generality. This allows to not use
    # separation characters like space since 3 bytes always represent a divided number
    def txDataEncoding(self, initial_data, *args):
        conc_data = initial_data
        for i in args:
            i_str = str(i)[::-1]
            conc_data += (chr(self._spaceChar) + i_str)
        return conc_data

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




