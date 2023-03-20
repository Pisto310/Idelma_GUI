

class MutableBrdInfo:
    """Basic class to create obj of which
    the attributes are the mutable infos
    of the IDELMA board
    """
    def __init__(self, *args):
        self._capacity = args[0]
        self._remaining = args[1]
        self._assigned = args[2]

    def __eq__(self, other):
        if not isinstance(other, MutableBrdInfo):
            return NotImplemented
        return (self.capacity == other.capacity and
                self.remaining == other.remaining and
                self.assigned == other.assigned)

    def __ne__(self, other):
        return not self == other

    def blockAssignation(self, used_blocks):
        self._remaining -= used_blocks
        self._assigned += used_blocks

    def blockReallocation(self, restored_blocks):
        self._remaining += restored_blocks
        self._assigned -= restored_blocks

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
