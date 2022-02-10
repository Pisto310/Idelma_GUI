import time

from serial import *
from time import sleep


class UsrSerial(Serial):
    """
    A serial class inherited from the pySerial
    module. Done so that methods and attributes can
    be added to the convenience of the dev
    """

    def __init__(self, port='/dev/cu.usbmodem14101', baudrate=9600, timeout=0.1, serial_wait=1.2):
        super().__init__(port=port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE,
                         stopbits=STOPBITS_ONE, timeout=timeout, xonxoff=False, rtscts=False,
                         write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        time.sleep(serial_wait)     # To allow Arduino to RST

        self._rxBuffer = []

    # Method to call to write on serial port
    def writeToPort(self, serial_data):
        self.write(bytes(serial_data, 'utf-8'))
        time.sleep(0.05)

    def readPort(self, expected_size):
        if self.in_waiting == expected_size:
            self.rxBuffer = list(self.read_until(expected=LF, size=expected_size))
            print(self.rxBuffer)

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




