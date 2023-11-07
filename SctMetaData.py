from dataclasses import dataclass


@dataclass
class SctMetaData:
    """
    Dataclass to contain all metadata related to sections that is to be sent over serial
    """
    sctIdx: int
    pixelCount: int = 0
    brightness: int = 50
    singlePxlCtrl: int = 0

    def pxlHeapBlocksCount(self):
        """
        Return the number of blocks to be used in the heap
        """
        if self.singlePxlCtrl:
            return self.singlePxlCtrl
        else:
            return self.pixelCount
