import json
import pickle


class BaseSerializer:

    def dumps(self, value):
        raise NotImplementedError

    def loads(self, value):
        raise NotImplementedError


class PassthroughSerializer(BaseSerializer):

    def dumps(self, value):
        return value

    def loads(self, value):
        return value


class StringSerializer(BaseSerializer):

    def dumps(self, value):
        if isinstance(value, bytes):
            return value.decode()
        return str(value)

    def loads(self, value):
        return value


class JsonSerializer(BaseSerializer):

    def __init__(self, encoder=None, decoder=None):
        self.encoder = encoder
        self.decoder = decoder

    def dumps(self, value):
        return json.dumps(value, cls=self.encoder)

    def loads(self, value):
        return json.loads(value, cls=self.decoder)


class PickleSerializer(BaseSerializer):

    def __init__(self, protocol=pickle.DEFAULT_PROTOCOL):
        self.protocol = protocol

    def dumps(self, value):
        return pickle.dumps(value, protocol=self.protocol)

    def loads(self, value):
        return pickle.loads(value)
