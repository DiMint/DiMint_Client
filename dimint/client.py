class DiMintClient:
    __hosts = []
    __data = {}
    __connected = False

    def __init__(self, hosts):
        self.__hosts = hosts
        self.__connect()

    def get(self, key, default=None):
        key = self.__convert_key(key)
        return self.__data.get(key, default)

    def set(self, key, value):
        key = self.__convert_key(key)
        self.__data[key] = value

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __connect(self):
        self.__connected = True
        print('connected')

    def __disconnect(self):
        self.__connected = False
        print('disconnected')

    def __convert_key(self, key):
        return str(key)

    def __del__(self):
        self.__disconnect()
