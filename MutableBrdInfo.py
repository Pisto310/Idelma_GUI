

class MutableBrdInfo:
    """Basic class to create obj of which
    the attributes are the mutable infos
    of the IDELMA board"""

    def __init__(self, *args):
        self._capacity = args[0]
        self._remaining = args[1]
        self._assigned = args[2]

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, updt_cap: int):
        self._capacity = updt_cap

    @property
    def assigned(self):
        return self._assigned

    @assigned.setter
    def assigned(self, updt_assigned: int):
        self._assigned = updt_assigned

    @property
    def remaining(self):
        return self._remaining

    @remaining.setter
    def remaining(self, updt_remaining: int):
        self._remaining = updt_remaining
