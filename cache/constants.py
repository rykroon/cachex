
DEFAULT_TTL = 300
Persist = None # a Synonym for a Persistent key, AKA a key that does not expire.


class Singleton:
    _singleton = None
    _repr = None

    def __new__(cls):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)
        return cls._singleton

    def __repr__(self):
        if self._repr is not None:
            return self._repr
        return super().__repr__()


class UndefinedType(Singleton):
    _repr = 'Undefined'

    def __bool__(self):
        return False


Undefined = UndefinedType()

MissingKey = Undefined
NotPassed = Undefined
