from dataclasses import dataclass


@dataclass
class PxlMetaData:
    """
    Dataclass to contain all metadata of a pixel. Colors are
    encoded over 32-bits, so int range is [0 to 4294967295]]
    """
    pxlIdx: int
    rgbwColor: int = 0x00000000
    hsvColor: int = 0x00000000
    rgbwTarget: int = 0x00000000
    hsvTarget: int = 0x00000000
