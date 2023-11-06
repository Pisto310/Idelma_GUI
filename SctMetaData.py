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

    # def keyIndex(self):
    #     """
    #     Returns the of each key for quick tuple association
    #     """
