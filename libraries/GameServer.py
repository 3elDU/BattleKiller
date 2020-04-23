from threading import *
import socket
from typing import List
from libraries import Map


_map = {}
_objects = {}
_players = []


class _Client(Thread):
    def __init__(self, conn, addr, thread_name, thread_id):
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr

        self.thread_name = thread_name
        self.thread_id = thread_id

        self.data = None
        self.tosend = None
        self.close = False
        self.alive = True
        self.commands = 0

        self.playerClass = ''
        self.playerX = 0
        self.playerY = 0
        self.index = None

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
            self.alive = False
            tosend = 'ok'
            self.close = True
        elif 'cmd-setblocks' in data:
            try:
                d = eval(data.replace('cmd-setblocks', ''))
                for block in d:
                    _map[block[0], block[1]] = block[2]
            except:
                tosend = 'again'
        elif 'cmd-setobjects' in data:
            try:
                d = eval(data.replace('cmd-setobjects'))
                global _objects
                for obj in d:
                    _objects[obj[0], obj[1]] = obj[2]
            except:
                tosend = 'again'
        elif 'cmd-setplayer' in data:
            try:
                d = eval(data.replace('cmd-setplayer', ''))
                self.playerClass = d[2]
                self.playerX = int(d[0])
                self.playerY = int(d[1])
            except:
                tosend = 'again'
        elif data == 'cmd-getplayers':
            tosend = ''
            for i in _players:
                if i != [self.playerX, self.playerY, self.playerClass]:
                    tosend += str(i)
        elif data == 'cmd-getmap':
            tosend = _map
        elif data == 'cmd-getobjects':
            tosend = _objects

        print(self.addr, ': Server response :', tosend)
        self.tosend = str(tosend)

    def run(self):
        global _players

        while self.alive:
            try:
                self.data = self.conn.recv(131072).decode('utf-8')
                print(self.addr, ':', self.data)

                self.react(self.data)
                self.commands += 1

                if not [self.playerX, self.playerY, self.playerClass] == [0, 0, None]:
                    if not [self.playerX, self.playerY, self.playerClass] in _players:
                        self.index = len(_players)
                        _players.append([self.playerX, self.playerY, self.playerClass])
                        print(_players)
                    else:
                        if not [self.playerX, self.playerY, self.playerClass] == _players[self.index]:
                            _players[self.index] = [self.playerX, self.playerY, self.playerClass]

                if self.tosend is not None:
                    try:
                        self.conn.send(self.tosend.encode('utf-8'))
                        self.tosend = None
                    except socket.error:
                        pass

                if self.close:
                    self.conn.close()
                    self.alive = False
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
                                self.clients.remove((thr.getConn()))
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
        global _objects

        self.ip = ip
        self.port = port
        self.dir = directory
        self.mapName = mapName

        self.map = Map.Map(mapName, directory=directory)

        _map = self.map.getMap()
        _objects = self.map.getObjects()

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
