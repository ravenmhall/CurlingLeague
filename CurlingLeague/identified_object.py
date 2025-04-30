"""IdentifiedObject -- an abstract class...no instances of it will be created (file name: identified_object.py)

oid [r/o prop] -- the object id for this object
__init__(oid) -- initialization method that sets the oid property as specified by the argument
__eq__(other) -- two IndentifiedObjects are equal if they have the same type and the same oid
__hash__() -- return hash code based on object's oid"""

class IdentifiedObject():
    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        return type(self) == type(other) and self.oid == other.oid

    def __hash__(self):
        return hash(self.oid)