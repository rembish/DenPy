from direct_access import DirectAccess
from nintendo_mmc1 import NintendoMmc1

class Mapper(object):
    __mapper = None
    __current = None
    __types = {
        0: DirectAccess,
        1: NintendoMmc1,
    }
    def __new__(cls, type = 0):
        if not cls.__mapper or type != self.__current:
            cls.__current = type
            cls.__mapper = cls.__types[type]()

        return cls.__mapper
