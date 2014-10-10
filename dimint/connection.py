from hashlib import sha1
import json

import zmq

from dimint.command import Command


class Connection:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__init_address = 'tcp://{0}:{1}'.format(self.__host, self.__port)
        self.__is_connected = False
        self.__connect()

    def get(self, key):
        cmd = Command.get_by_key(key)
        loc = self.__get_overload_location_by_key(key)
        self.__sockets[loc].send(cmd)
        value = self.__sockets[loc].recv()
        return json.loads(value.decode('utf-8'))

    def set(self, key, value):
        cmd = Command.set_value(key, value)
        loc = self.__get_overload_location_by_key(key)
        self.__sockets[loc].send(cmd)
        result = self.__sockets[loc].recv()
        return json.loads(result.decode('utf-8'))

    def __connect(self):
        context = zmq.Context()
        init_socket = context.socket(zmq.REQ)
        init_socket.connect(self.__init_address)
        init_socket.send(Command.get_overloads_list())
        self.__overloads = json.loads(init_socket.recv().decode('utf-8'))['overloads']
        print(self.__overloads)
        self.__sockets = [context.socket(zmq.REQ)
                          for _ in range(len(self.__overloads))]
        init_socket.disconnect(self.__init_address)
        for i, overload in enumerate(self.__overloads):
            self.__sockets[i].connect('tcp://{0}'.format(overload))
        self.__is_connected = True

    def __disconnect(self):
        if self.connected:
            for socket in self.__sockets:
                try:
                    socket.disconnect()
                except:
                    pass

    def __get_overload_location_by_key(self, key):
        if not self.connected:
            self.__connect()
        if len(self.__sockets) <= 0:
            raise Exception
        hex_data = int(sha1(json.dumps(key).encode('utf-8')).hexdigest(), 16)
        return hex_data % len(self.__sockets)

    def __del__(self):
        self.__disconnect()

    @property
    def connected(self):
        return self.__is_connected
