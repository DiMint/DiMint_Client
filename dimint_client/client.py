from dimint_client.connection import Connection


class DiMintClient:
    __host = None
    __port = None

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__connect()

    def get(self, key, default=None):
        try:
            return self.__connection.get(key)
        except Exception as e:
            return default

    def set(self, key, value):
        result = self.__connection.set(key, value)
        return result

    def state(self):
        result = self.__connection.state()
        return result['state']

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __connect(self):
        self.__connection = Connection(self.__host, self.__port)

    def __disconnect(self):
        del self.__connection

    def __del__(self):
        try:
            self.__disconnect()
        except ImportError:
            pass
