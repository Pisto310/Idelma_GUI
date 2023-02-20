

class SctProp:
    """
    Contains all properties relating to user-
    created section
    """
    def __init__(self, name: str, pixel_count: int):

        self._sctName = name
        self._pxlCount = pixel_count

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
            if self.typeCheck(new_val, int) and self.valueBoundCheck(new_val, 0, 0):
                self._pxlCount = new_val
        except (TypeError, ValueError) as error:
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

