from threading import *
import socket
from typing import List
from libraries import Map


class _Client(Thread):
    def __init__(self, conn, addr, thread_name, thread_id):
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr

        self.thread_name = thread_name
        self.thread_id = thread_id

        self.data = None
        self.alive = True

    def setAlive(self, b):
        self.alive = b

    def react(self, data):
        pass

    def run(self):
        while self.alive:
            try:
                self.data = self.conn.recv(131072).decode('utf-8')

                self.react(self.data)
            except socket.error:
                pass

        self.conn.close()


class _Server(Thread):
    threads: List[_Client]

    def __init__(self, ip, port, thread_name, thread_id):
        Thread.__init__(self)

        self.name = thread_name
        self.id = thread_id

        self.ip = ip
        self.port = port
        self.connected = False
        self.alive = True
        self.clients = []
        self.threads = []

        self.s = socket.socket()
        self.s.setblocking(False)

    def setAlive(self, b):
        self.alive = b

    def connect(self):
        c = False
        while not c:
            try:
                self.s.bind((self.ip, self.port))
                c = True
            except socket.error:
                pass

        self.connected = c

    def run(self):
        self.connect()
        if self.connected:
            try:
                self.s.listen(2)
                while self.alive:
                    try:
                        conn, addr = self.s.accept()

                        if not (conn, addr) in self.clients:
                            self.clients.append((conn, addr))

                            thread = _Client(conn, addr, 'client', len(self.clients))
                            self.threads.append(thread)
                            thread.start()
                    except socket.error:
                        pass
            except Exception as e:
                print('LOG: ERROR:', e)

        for c in self.threads:
            c.setAlive(False)


class Server:
    def __init__(self, ip, port, mapName):
        self.ip = ip
        self.port = port
        self.mapName = mapName

        self.Map = Map.Map(mapName)

        self.server = _Server(self.ip, self.port, 'server', 0)
        self.server.start()

        try:
            self.server.join()
        except Exception as e:
            print('LOG: ERROR:', e)
            print('Exiting...')
            self.server.setAlive(False)
