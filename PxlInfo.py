from enum import Enum


class PixelState(Enum):
    IDLE = 0
    HSV_FADE = 1
    RGB_FADE = 2
    BLINK_ONCE = 3
    BLINK = 4
    SPARKLE = 5


class PxlInfo:
    """
    Class that aims to recreate the content of
    all "attributes" found in pixel_info_type
    as defined in the FW
    """

    def __init__(self, state: pixelState, action_time, action_start,
                 rgbw_color, hsv_color, rgbw_target, hsv_target):

        self.pixelState = state
        self.pxlActionTime = action_time
        self.pxlActionStart = action_start
        self.rgbwColor = rgbw_color
        self.hsvColor = hsv_color
        self.rgbwTarget = rgbw_target
        self.hsvTarget = hsv_target
