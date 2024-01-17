from dataclasses import dataclass

from BrdMgmtMetaData import BrdMgmtMetaData

import os


class ArduinoSerialEmulator:
    """
    A class that aims to create a 'virtual arduino'. Every macro as defined in 'Board.h'
    are in the constructor of the class. All methods refer to the content of useful
    '.cpp' files, notably 'Board.cpp' and 'Serial_lib.cpp'
    """
    def __init__(self, master):

        self.master = master

        self.serialBufferSize = 64

        self.serialNum = "12345678"

        self.fwVerMajor = 0
        self.fwVerMinor = 1
        self.fwVerPatch = 0
        self.fwVersion = None

        self.pxlInfoHeapSize = 100
        self.pixelsInfo = None

        self.maxNoScts = 12
        self.sectionsInfo = None

        self.rxBuffer = SerialBufferType(self.serialBufferSize)
        self.txBuffer = SerialBufferType(self.serialBufferSize)
        self.pendingRqst = None

        self.acknowledge = 6
        self.lineFeedChar = 10
        self.notAck = 21
        self.spaceChar = 32

        self.cmdsDict = {
            "1":  self.serialNumSend,
            "2":  self.fwVersionSend,
            "3":  self.sctsMetaDataSend,
            "4":  self.pxlsMetaDataSend,
            "5":  self.sendNak,

            "10": self.configBrd,

            "20": self.saveSettings,

            "254": self.allOff,
        }

        self.localVarDef()

    def localVarDef(self):
        """
        Basically replicates what is done in the 'LOCAL VARIABLES' section
        of the 'Board.cpp' file, but no defining pointer struct
        """
        self.fwVersion = bytearray([self.fwVerMajor, self.fwVerMinor, self.fwVerPatch])
        self.sectionsInfo = BrdMgmtMetaData(self.maxNoScts, self.maxNoScts, 0)
        self.pixelsInfo = BrdMgmtMetaData(self.pxlInfoHeapSize, self.pxlInfoHeapSize, 0)

    def processSerialMssg(self):
        """
        Method is called by a signal when a serial mssg is sent and processes the data
        to and dispatch it to the appropriate function
        """
        self.rxBuffer.mssgLen = os.readv(self.master, [self.rxBuffer.buffer])
        self.rxBuffer.mssgLen = self.rxDataParsing()
        self.cmdsDict[str(self.pendingRqst)]()

    def serialWrite(self):
        self.insertLineFeedChar()
        os.writev(self.master, [self.txBuffer.buffer[:self.txBuffer.mssgLen:]])
        # self.resetTxBuffer()

    def serialNumSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer,
                                                   bytearray.fromhex(self.uint32LittleEndian(self.serialNum)))
        self.serialWrite()

    def fwVersionSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer, self.fwVersion)
        self.serialWrite()

    def sctsMetaDataSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer,
                                                   bytearray([self.sectionsInfo.capacity,
                                                              self.sectionsInfo.remaining,
                                                              self.sectionsInfo.assigned]))
        self.serialWrite()

    def pxlsMetaDataSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer,
                                                   bytearray([self.pixelsInfo.capacity,
                                                              self.pixelsInfo.remaining,
                                                              self.pixelsInfo.assigned]))
        self.serialWrite()

    def configBrd(self):
        """
        Updates mcu attributes with message content and sends an ACK (0x06) back to the PC
        """

        # Do the mcu attribute update here

        self.sendAck()

    def saveSettings(self):
        """
        Save actual mcu configuration in the EEPROM (might implement virtual EEPROM?)
        """

        # Do saving of settings here

        self.sendAck()

    def allOff(self):
        self.sendAck()

    def sendAck(self):
        """
        Method that returns an "ACK" character once mssg has been processed
        """
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer, bytearray([self.acknowledge]))
        self.serialWrite()

    def sendNak(self):
        """
        Method that returns an "ACK" character once mssg has been processed
        """
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer, bytearray([self.notAck]))
        self.serialWrite()

    def rxDataParsing(self):
        """
        Method to parse bytes received through serial. Bytes are broken into single digits,
        separated by space char (0x20) and arranged in a little endian format. Message always
        end with line feed character (0x10)
        """
        rqstCheck = False
        unitsTracker = 0
        recomposedNbr = 0
        newMssgLen = 0
        for index, val in enumerate(self.rxBuffer.buffer):
            if not val == self.spaceChar and not val == self.lineFeedChar:
                recomposedNbr += self.ascii2Hex(val) * (10 ** unitsTracker)
                unitsTracker += 1
            elif unitsTracker:
                if not rqstCheck:
                    self.pendingRqst = recomposedNbr
                    rqstCheck = True
                else:
                    self.rxBuffer.buffer[newMssgLen] = recomposedNbr
                    newMssgLen += 1
                unitsTracker = 0
                recomposedNbr = 0
                if val == self.lineFeedChar:
                    break
        return newMssgLen

    def txDataParsing(self, buffer, output_data):
        """
        Parses the serial message by separating each individual digits as single bytes.
        Output_data has to be of type bytearray, or else method won't work
        """
        mssgLen = 0
        for i, byte in enumerate(output_data):
            while byte >= 10:
                buffer[mssgLen], byte = self.moduloTen(byte)
                mssgLen += 1
            buffer[mssgLen] = byte
            mssgLen += 1
            if i != (len(output_data) - 1):
                buffer[mssgLen] = self.spaceChar
                mssgLen += 1
        return mssgLen

    def insertLineFeedChar(self):
        self.txBuffer.buffer[self.txBuffer.mssgLen] = self.lineFeedChar
        self.txBuffer.mssgLen += 1

    def resetTxBuffer(self):
        lineFeedCheck = False
        index = 0
        while not lineFeedCheck:
            if self.txBuffer.buffer[index] == self.lineFeedChar:
                lineFeedCheck = True
            self.txBuffer.buffer[index] = 0
            index += 1
        self.txBuffer.mssgLen = 0

    @staticmethod
    def ascii2Hex(ascii_byte):
        if ascii_byte > 0x39:
            ascii_byte -= 7
        return ascii_byte & 0x0F

    @staticmethod
    def uint32LittleEndian(uint_32):
        """
        Reorganizes an hex str in a Little Endian manner to emulate the storing
        of variables in the RAM of an Arduino mcu
        """
        container = ''
        index = -2
        while index >= -8:
            if index == -2:
                container += uint_32[index::]
            else:
                container += uint_32[index: index + 2:]
            index -= 2
        return container

    @staticmethod
    def moduloTen(digit):
        remainder = digit % 10
        result = int((digit - remainder) / 10)
        return remainder, result


class SerialBufferType:
    """
    Simple class meant to replicate the ser_buffer_t struct
    as defined in the FW code (Serial_lib.h)
    """
    def __init__(self, buffer_size):
        self.buffer = bytearray(buffer_size)
        self.mssgLen = 0


@dataclass
class PixelMetaDataType:
    """
    Class that replicates the pixel_metadata_t struct appearing
    in SK6812 header
    """
    pxlSctID = None
    pxlID = None
    pxlState = None
    pxlActionTimes = None
    pxlActionStart = None
    rgbwColor = None
    hsvColor = None
    rgbwTarget = None
    hsvTarget = None


# if __name__ == '__main__':
#     master, slave = pty.openpty()
#     virtualPort = os.ttyname(slave)
#     arduinoSerEmu = ArduinoSerialEmulator(master)
#     obj = json.dumps(arduinoSerEmu.__dict__, indent=4)
#     pass
