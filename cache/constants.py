
DEFAULT_TTL = 300

# NotPassed = object()
# MissingKey = object()


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


class MissingKeyType(Singleton):
    _repr = 'MissingKey'
    
    def __bool__(self):
        return False

MissingKey = MissingKeyType()


class NotPassedType(Singleton):
    _repr = 'NotPassed'
    
    def __bool__(self):
        return False

NotPassed = NotPassedType()
