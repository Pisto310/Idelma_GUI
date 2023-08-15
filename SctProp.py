

class SctProp:
    """
    Contains all properties relating to user-created section
    """
    remainingPxls = 0

    def __init__(self, name: str, pixel_count: int, set_default_name: bool):

        self._sctName = name
        self._pxlCount = pixel_count
        self._setDefaultName = set_default_name

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
    def pxlCount(self):
        return self._pxlCount

    @pxlCount.setter
    def pxlCount(self, new_val: int):
        try:
            if self.typeCheck(new_val, int) and self.valueBoundCheck(new_val, 0, self.remainingPxls):
                self._pxlCount = new_val
        except (TypeError, ValueError) as error:
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

