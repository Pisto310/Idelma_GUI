

class SctProp:
    """
    Contains all properties relating to user-created section
    """

    infoTupleIndexes = {'sctID_index': 0,
                        'pixelCount_index': 1,
                        'brightness_index': 2,
                        'singlePxlCtrl_index': 3}

    def __init__(self, index: int, pixel_count: int, brightness_level: int, single_pxl_ctrl: bool,
                 name: str, set_default_name: bool):

        self._sctID = index
        self._pxlCount = pixel_count
        self._brightness = brightness_level
        self._singlePxlCtrl = single_pxl_ctrl
        self._sctName = name
        self._setDefaultName = set_default_name

        self._sctInfoTuple = (index, pixel_count, brightness_level, int(single_pxl_ctrl))

    def decrDefaultName(self):
        if self.setDefaultName:
            self.sctName = "Section " + str(self.extractNameInt() - 1)

    def extractNameInt(self):
        container = ""
        for index, val in enumerate(self.sctName[::-1]):
            if val == " ":
                break
            else:
                container += val
        return int(container[::-1])

    @property
    def sctID(self):
        return self._sctID

    @sctID.setter
    def sctID(self, new_index):
        self._sctID = new_index
        self._sctInfoTuple = (self._sctID, self.pxlCount)

    @property
    def pxlCount(self):
        return self._pxlCount

    @pxlCount.setter
    def pxlCount(self, new_val: int):
        try:
            if self.typeCheck(new_val, int):
                # and self.valueBoundCheck(new_val, 0, self.remainingPxls):
                self._pxlCount = new_val
                self._sctInfoTuple = (self.sctID, self._pxlCount)
        except (TypeError, ValueError) as error:
            print(error)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness_level: int):
        if self.typeCheck(brightness_level, int) and self.valueBoundCheck(brightness_level, 0, 255):
            self._brightness = brightness_level

    @property
    def singlePxlCtrl(self):
        return self._singlePxlCtrl

    @singlePxlCtrl.setter
    def singlePxlCtrl(self, new_state: bool):
        if self.typeCheck(new_state, bool):
            self._singlePxlCtrl = new_state

    @property
    def sctName(self):
        return self._sctName

    @sctName.setter
    def sctName(self, new_name: str):
        try:
            if self.typeCheck(new_name, str):
                self._sctName = new_name
        except TypeError as error:
            print(error)

    @property
    def setDefaultName(self):
        return self._setDefaultName

    @setDefaultName.setter
    def setDefaultName(self, bool_state):
        try:
            if self.typeCheck(bool_state, bool):
                self._setDefaultName = bool_state
        except TypeError as error:
            print(error)

    @property
    def sctInfoTuple(self):
        return self._sctInfoTuple

    @sctInfoTuple.setter
    def sctInfoTuple(self, new_sct_id, new_pixel_count, new_brightness_level, new_single_pxl_ctrl):
        self._sctInfoTuple = (new_sct_id, new_pixel_count, new_brightness_level, int(new_single_pxl_ctrl))

    @staticmethod
    def typeCheck(var, user_t):
        if type(var) is user_t:
            return True
        else:
            raise TypeError("Value should be of type {}".format(user_t))

    @staticmethod
    # Simple func to check if value of variable is between set boundary
    # To not stop prog execution, error handling should be done once func is called
    def valueBoundCheck(val, low_bound, up_bound):
        if low_bound <= val <= up_bound:
            return True
        else:
            raise ValueError("Value is out of bound. Must be in [{}, {}] interval".format(low_bound, up_bound))

