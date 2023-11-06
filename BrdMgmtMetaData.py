

class BrdMgmtMetaData:
    """Basic class to create obj of which
    the attributes are the mutable infos
    of the IDELMA board
    """
    def __init__(self, capacity, remaining, assigned):
        self._capacity = capacity
        self._remaining = remaining
        self._assigned = assigned

    def __eq__(self, other):
        if not isinstance(other, BrdMgmtMetaData):
            return NotImplemented
        return (self.capacity == other.capacity and
                self.remaining == other.remaining and
                self.assigned == other.assigned)

    def __ne__(self, other):
        return not self == other

    @classmethod
    def blockUpdt(cls, remaining, assigned, blocks):
        """
        Assigns blocks (remaining drops, assigned increases) internally to this class
        Using this func to change attr. doesn't trigger signal of calling objs.

        Parameters:
            capacity (int): Board's blocks capacity
            remaining (int): Board's remaining available blocks
            assigned (int): Board's already assigned blocks
            blocks (int): Count of used or freed blocks in the transaction
        """
        remaining -= blocks
        assigned += blocks
        return cls((remaining + assigned), remaining, assigned)

    @property
    def capacity(self):
        return self._capacity

    @property
    def assigned(self):
        return self._assigned

    @assigned.setter
    def assigned(self, updt_assigned: int):
        try:
            if self.valueBoundCheck(updt_assigned, 0, self.capacity):
                self._assigned = updt_assigned
        except ValueError as error:
            print(error)

    @property
    def remaining(self):
        return self._remaining

    @remaining.setter
    def remaining(self, updt_remaining: int):
        try:
            if self.valueBoundCheck(updt_remaining, 0, self.capacity):
                self._remaining = updt_remaining
        except ValueError as error:
            print(error)

    @staticmethod
    def valueBoundCheck(val, low_bound, up_bound):
        if low_bound <= val <= up_bound:
            return True
        else:
            raise ValueError("Value is out of bound. Must be in [{}, {}] interval".format(low_bound, up_bound))
