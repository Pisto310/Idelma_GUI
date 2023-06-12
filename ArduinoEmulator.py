from MutableBrdInfo import MutableBrdInfo

from numpy import zeros
import os


class ArduinoEmulator:
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

        self.lineFeedChar = 10
        self.spaceChar = 32

        self.cmdsDict = {
            "1": self.serialNumSend,
            "2": self.fwVersionSend,
            "3": self.sctsBrdMgmtSend,
            "4": self.pxlsBrdMgmtSend
        }

        self.localVarDef()

    def localVarDef(self):
        """
        Basically replicates what is done in the 'LOCAL VARIABLES' section
        of the 'Board.cpp' file, but no defining pointer struct
        """
        self.fwVersion = bytearray([self.fwVerMajor, self.fwVerMinor, self.fwVerPatch])
        self.sectionsInfo = MutableBrdInfo(self.maxNoScts, self.maxNoScts, 0)
        self.pixelsInfo = MutableBrdInfo(self.pxlInfoHeapSize, self.pxlInfoHeapSize, 0)

    def processSerialMssg(self):
        """
        Method is called by a signal when a serial mssg is sent and processes the data
        to and dispatch it to the appropriate function
        """
        self.rxBuffer.mssgLen = os.readv(self.master, [self.rxBuffer.buffer])
        self.rxDataParsing()
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

    def sctsBrdMgmtSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer,
                                                   bytearray([self.sectionsInfo.capacity,
                                                              self.sectionsInfo.remaining,
                                                              self.sectionsInfo.assigned]))
        self.serialWrite()

    def pxlsBrdMgmtSend(self):
        self.txBuffer.mssgLen = self.txDataParsing(self.txBuffer.buffer,
                                                   bytearray([self.pixelsInfo.capacity,
                                                              self.pixelsInfo.remaining,
                                                              self.pixelsInfo.assigned]))
        self.serialWrite()

    def rxDataParsing(self):
        """
        Method to parse bytes received through serial. Bytes are broken into single digits,
        separated by space char (0x06) and arranged in a little endian format. Message always
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
        of variables in the RAM of an Arduino board
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
