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
        self.__socket.send('GET::::{0}'.format(key).encode('utf-8'))
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
        self.__socket.send('SET::::{0}::::{1}'.format(
            key, json.dumps(value)).encode('utf-8'))
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
        key = str(key)
        if '::::' in key:
            raise KeyError('"::::" cannot be contained in key')
        return key

    def __del__(self):
        try:
            self.__disconnect()
        except ImportError:
            pass
