import json
import random

import zmq

from dimint_client.command import Command


class Connection:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__init_address = 'tcp://{0}:{1}'.format(self.__host, self.__port)
        self.__is_connected = False
        self.__connect()

    def get(self, key):
        cmd = Command.get_by_key(key)
        return self.__send(cmd)

    def set(self, key, value):
        cmd = Command.set_value(key, value)
        return self.__send(cmd)

    def state(self):
        cmd = Command.get_state()
        return self.__send(cmd)

    def __connect(self):
        context = zmq.Context()
        init_socket = context.socket(zmq.REQ)
        init_socket.connect(self.__init_address)
        init_socket.send(Command.get_overlords_list())
        self.__overlords = json.loads(init_socket.recv().decode('utf-8'))['overlords']
        print(self.__overlords)
        self.__sockets = [context.socket(zmq.REQ)
                          for _ in range(len(self.__overlords))]
        init_socket.disconnect(self.__init_address)
        for i, overlord in enumerate(self.__overlords):
            self.__sockets[i].connect('tcp://{0}'.format(overlord))
        self.__is_connected = True

    def __disconnect(self):
        if self.connected:
            for socket in self.__sockets:
                try:
                    socket.disconnect()
                except:
                    pass

    def __send(self, command):
        loc = self.__get_overlord_location()
        self.__sockets[loc].send(command)
        return json.loads(self.__sockets[loc].recv().decode('utf-8'))

    def __get_overlord_location(self):
        if not self.connected:
            self.__connect()
        if len(self.__sockets) <= 0:
            raise Exception
        return random.randint(0, 2**31-1) % len(self.__sockets)

    def __del__(self):
        self.__disconnect()

    @property
    def connected(self):
        return self.__is_connected
