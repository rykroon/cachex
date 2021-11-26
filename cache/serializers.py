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
        return value


class JsonSerializer(BaseSerializer):

    def dumps(self, value):
        return json.dumps(value)

    def loads(self, value):
        if value is None:
            return None
        return json.loads(value)


class PickleSerializer(BaseSerializer):

    def dumps(self, value):
        return pickle.dumps(value)

    def loads(self, value):
        if value is None:
            return None
        return pickle.loads(value)