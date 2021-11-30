import json
import pickle


class BaseSerializer:

    def dumps(self, value):
        raise NotImplementedError

    def loads(self, value):
        raise NotImplementedError


class StringSerializer(BaseSerializer):

    def dumps(self, value):
        return str(value)

    def loads(self, value):
        if value is None:
            return None
        if isinstance(value, bytes):
            return value.decode()
        return str(value)


class JsonSerializer(BaseSerializer):

    def __init__(self, dump_kwargs=None, load_kwargs=None):
        self.dump_kwargs = dump_kwargs or {}
        self.load_kwargs = load_kwargs or {}

    def dumps(self, value):
        return json.dumps(value, **self.dump_kwargs)

    def loads(self, value):
        if value is None:
            return None
        return json.loads(value, **self.load_kwargs)


class PickleSerializer(BaseSerializer):

    def dumps(self, value):
        return pickle.dumps(value)

    def loads(self, value):
        if value is None:
            return None
        return pickle.loads(value)