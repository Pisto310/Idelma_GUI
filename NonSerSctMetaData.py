

class NonSerSctMetaData:
    """
    Contains all properties relating to user-created section
    """

    infoTupleIndexes = {'sctID_index': 0,
                        'pixelCount_index': 1,
                        'brightness_index': 2,
                        'singlePxlCtrl_index': 3}

    def __init__(self, name: str):
        self._sctName = name

    # def decrDefaultName(self):
    #     if self.setDefaultName:
    #         self.sctName = "Section " + str(self.extractNameInt() - 1)
    #
    # def extractNameInt(self):
    #     container = ""
    #     for index, val in enumerate(self.sctName[::-1]):
    #         if val == " ":
    #             break
    #         else:
    #             container += val
    #     return int(container[::-1])

    def defaultNameCheck(self, sct_idx: int):
        """
        Check if the set name is the default one

        Parameters:
            sct_idx (int): Index of the section that has to pass check

        Return:
            A boolean indicating if default name is set (True) or not (False)
        """
        default_name_str = "Section " + str(sct_idx)
        if self.sctName == default_name_str:
            return True
        else:
            return False

    def defaultNameSet(self, sct_idx: int):
        """
        Set the name to the default format

        Parameters:
            sct_idx (int): Index of the section
        """
        self.sctName = "Section " + str(sct_idx)

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

    @classmethod
    def instWithDefaultName(cls, sct_idx):
        """
        Instantiate an object of the class with default name

        Parameters:
            sct_idx (int): Index of the section
        """
        return cls("Section " + str(sct_idx))

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

