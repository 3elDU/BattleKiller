from threading import *
import socket
from typing import List
from libraries import Map


_map = None


class _Client(Thread):
    def __init__(self, conn, addr, thread_name, thread_id):
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr

        self.thread_name = thread_name
        self.thread_id = thread_id

        self.data = None
        self.tosend = None
        self.alive = True
        self.commands = 0

        self.playerClass = ''
        self.playerX = 0
        self.playerY = 0

    def getConn(self):
        return self.conn, self.addr

    def setAlive(self, b):
        self.alive = b

    def getAlive(self):
        return self.alive

    def react(self, data):
        global _map
        tosend = ''

        if data == 'cmd-stop':
            self.conn.close()
            self.alive = False
            tosend = 'ok'
        elif data == 'cmd-setplayer':
            try:
                d = eval(data)
                self.playerClass = d[2]
                self.playerX = d[0]
                self.playerY = d[1]
            except:
                tosend = 'again'

        self.tosend = tosend

    def run(self):
        while self.alive:
            try:
                self.data = self.conn.recv(131072).decode('utf-8')
                print(self.addr, ':', self.data)

                self.react(self.data)
                self.commands += 1

                if self.tosend is not None:
                    try:
                        self.conn.send(self.tosend.encode('utf-8'))
                        self.tosend = None
                    except socket.error:
                        pass
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

    def getAlive(self):
        return self.alive

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
        print('Server started')
        if self.connected:
            try:
                self.s.listen(2)
                print('Started listening to clients...')
                while self.alive:
                    try:
                        for thr in self.threads:
                            if not thr.getAlive():
                                self.threads.remove(thr)
                                self.clients.remove(self.threads.index(thr))
                                print('Threads -', len(self.threads))

                        conn, addr = self.s.accept()

                        if not (conn, addr) in self.clients:
                            print('LOG: New connection:', addr)

                            self.clients.append((conn, addr))

                            thread = _Client(conn, addr, 'client', len(self.clients))
                            thread.start()
                            self.threads.append(thread)
                            print('Threads -', len(self.threads))
                    except socket.error:
                        pass
            except Exception as e:
                print('LOG: ERROR:', e)

        for c in self.threads:
            c.setAlive(False)


class Server:
    def __init__(self, ip, port, directory, mapName):
        global _map

        self.ip = ip
        self.port = port
        self.dir = directory
        self.mapName = mapName

        _map = Map.Map(mapName, directory=directory)

        print('Creating thread...')
        self.server = _Server(self.ip, self.port, 'server', 0)
        print('Starting thread...')
        self.server.start()
        print('Thread started!')

        try:
            self.server.join()
        except Exception as e:
            print('LOG: ERROR:', e)
            print('Exiting...')
            self.server.setAlive(False)
