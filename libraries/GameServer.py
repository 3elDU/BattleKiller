from threading import *
import socket
from typing import List
from libraries import Map


_map = {}
_objects = {}
_players = {}

WIDTH = 48
HEIGHT = 24


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
        self.started = False
        self.step = False
        self.commands = 0

        self.prevMap = {}
        self.prevObjects = {}

        self.playerClass = ''
        self.playerX = 0
        self.playerY = 0
        self.rotation = 0

    def getConn(self):
        return self.conn, self.addr

    def setAlive(self, b):
        self.alive = b

    def getAlive(self):
        return self.alive

    def react(self, data):
        global _map
        tosend = ''

        try:
            data = data.split('--')

            for i in data:
                show = True
                try:
                    if i == 'cmd-start':
                        tosend = 'start'
                        self.started = True
                        print(self.addr, ' started game!')
                    elif i == 'cmd-stop':
                        self.alive = False
                        tosend = 'ok'
                        self.close = True
                    elif 'cmd-setblocks' in data:
                        try:
                            d = eval(i.replace('cmd-setblocks', ''))
                            for block in d:
                                _map[block[0], block[1]] = block[2]
                        except:
                            tosend = 'again'
                    elif 'cmd-setobjects' in data:
                        try:
                            d = eval(i.replace('cmd-setobjects'))
                            global _objects
                            for obj in d:
                                _objects[obj[0], obj[1]] = obj[2]
                        except:
                            tosend = 'again'
                    elif 'cmd-setplayer' in i:
                        try:
                            d = eval(i.replace('cmd-setplayer', ''))
                            self.playerClass = d[2]
                            self.playerX = int(d[0])
                            self.playerY = int(d[1])
                            self.rotation = int(d[3])
                        except Exception as e:
                            print(self.addr, ' : Exception:', e)
                            tosend = 'again'
                    elif i == 'cmd-getplayers':
                        tosend = []
                        for x in _players:
                            if _players[x] != [self.playerX, self.playerY, self.playerClass, self.rotation]:
                                tosend += _players[x]
                    elif i == 'cmd-getmap':
                        tosend = _map
                        self.prevMap = _map
                    elif i == 'cmd-getobjects':
                        tosend = _objects
                        self.prevObjects = _objects
                    elif i == 'cmd-getmapchanges':
                        tosend = []
                        for x in range(WIDTH):
                            for y in range(HEIGHT):
                                if self.prevMap[x, y] != _map[x, y]:
                                    tosend.append([x, y, _map[x, y]])
                    elif i == 'cmd-getobjchanges':
                        tosend = []
                        for x in range(WIDTH):
                            for y in range(HEIGHT):
                                if self.prevObjects[x, y] != _objects[x, y]:
                                    tosend.append([x, y, _objects[x, y]])
                    elif i == 'cmd-getnum':
                        tosend = self.thread_id

                    tosend = str(tosend) + '--'

                    if len(tosend) < 50:
                        if show:
                            print(self.addr, ': Server response :', tosend)
                    else:
                        print('Server response is too big!')

                    self.tosend += tosend
                except Exception as e:
                    print('Failed to iterate in Thread', self.thread_id)
                    print('Exception:', e)
        except Exception as e:
            print('Failed to interact in Thread', self.thread_id)
            print('Exception:', e)

    def oneStep(self):
        self.step = True

    def getStep(self):
        return self.step

    def run(self):
        global _players

        while self.alive:
            if self.step:
                try:
                    self.data = self.conn.recv(131072).decode('utf-8')
                    print(self.addr, ':', self.data)

                    self.react(self.data)
                    self.commands += 1

                    if not [self.playerX, self.playerY, self.playerClass] == [0, 0, '']:
                        _players[self.thread_id] = [self.playerX, self.playerY, self.playerClass, self.rotation]

                    if self.tosend is not None:
                        try:
                            self.conn.send(self.tosend.encode('utf-8'))
                            self.tosend = None
                        except socket.error:
                            pass

                    if self.close:
                        self.alive = False
                except socket.error:
                    pass
                finally:
                    self.step = False

        del _players[self.thread_id]
        self.conn.close()

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

                            thread = _Client(conn, addr, 'client', len(self.clients)-1)
                            thread.start()
                            self.threads.append(thread)
                            print('Threads -', len(self.threads))

                        for thr in self.threads:
                            if not thr.getStep():
                                thr.oneStep()
                                while thr.getStep():
                                    pass
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
