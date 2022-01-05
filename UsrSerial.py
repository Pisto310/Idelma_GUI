from serial import *
from time import sleep


class UsrSerial(Serial):
    """A serial class inherited from the pySerial
    module. Done so that methods and attributes can
    added to the convenience of the dev"""

    def __init__(self, port='/dev/cu.usbmodem14101', baudrate=9600, timeout=0.1, serial_wait=1.2):
        super().__init__(port=port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE,
                         stopbits=STOPBITS_ONE, timeout=timeout, xonxoff=False, rtscts=False,
                         write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None)
        time.sleep(serial_wait)     # To allow Arduino to RST

    # Method to call to write on serial port
    def writeToPort(self, serial_data):
        self.write(bytes(serial_data, 'utf-8'))
        time.sleep(0.05)

    # Methods will read port and return a list containing all in bytes read
    def readPort(self):
        if self.in_waiting:
            print(self.in_waiting)
            bytes_buff = []
            while self.in_waiting:
                # Reading one byte at a time
                bytes_buff.append(self.read(1))
            print(bytes_buff)

