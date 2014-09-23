import json
import zmq


class DiMintClient:
    __host = None
    __port = None

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__connect()

    def get(self, key, default=None):
        if not self.__connected:
            self.connect()
            if not self.__connected:
                return default
        key = self.__convert_key(key)
        content = json.dumps({
            'cmd_type': 'get',
            'key': key,
        })
        self.__socket.send(content.encode('utf-8'))
        res = self.__socket.recv()
        try:
            return json.loads(res.decode('utf-8'))
        except TypeError:
            return default

    def set(self, key, value):
        if not self.__connected:
            self.connect()
            if not self.__connected:
                return False
        key = self.__convert_key(key)
        content = json.dumps({
            'cmd_type': 'set',
            'key': key,
            'value': value,
        })
        self.__socket.send(content.encode('utf-8'))
        res = self.__socket.recv()
        return json.loads(res.decode('utf-8'))

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __connect(self):
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REQ)
        try:
            self.__socket.connect('tcp://{0}:{1}'.format(
                self.__host, self.__port))
            self.__connected = True
        except:
            pass

    def __disconnect(self):
        if self.__connected:
            self.__socket.disconnect('tcp://{0}:{1}'.format(
                self.__host, self.__port))
            self.__connected = False

    def __convert_key(self, key):
        if not isinstance(key, (int, float, str, bytes)):
            raise KeyError('key must be immutable.')
        key = str(key)
        return key

    def __del__(self):
        try:
            self.__disconnect()
        except ImportError:
            pass
