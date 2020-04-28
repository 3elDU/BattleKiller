from threading import *
import socket


class Server(Thread):
    def __init__(self, name, identifier, ip, port):
        self.ip = ip
        self.port = port

        Thread.__init__(self)
        self.name = name
        self.id = identifier
        self.connected = False
        self.tosend = None
        self.data = None
        self.alive = True
        self.tries = 500

        self.s = socket.socket()
        self.s.setblocking(False)

    def setAlive(self, b):
        self.alive = b

    def getAlive(self):
        return self.alive

    def connect(self):
        timer = 0
        while timer < self.tries:
            try:
                self.s.connect((self.ip, self.port))
                self.connected = True
                print('LOG: Connected to server!')
                break
            except socket.error as e:
                if str(e) == '[WinError 10056] A connect request was made on an already connected socket':
                    print('LOG: Connected to server!')
                    self.connected = True
                    break
                elif str(e) != '[WinError 10035] A non-blocking socket operation could not be completed immediately':
                    print('LOG: Client ERROR 42:', e)

            timer += 1

    def isConnected(self):
        return self.connected

    def getdata(self):
        toreturn = self.data.split('--')
        self.data = None
        return toreturn

    def send(self, data):
        self.tosend = data

    def run(self):
        self.connect()

        if self.connected:
            while self.alive:
                try:
                    self.data = self.s.recv(131172).decode('utf-8')
                except socket.error:
                    pass

                try:
                    if self.tosend is not None:
                        self.tosend = str(self.tosend) + '--'
                        self.s.send(self.tosend.encode('utf-8'))
                        self.tosend = None
                except socket.error:
                    pass


class Main:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.connected = False
        self.connectionTimeout = 10

        self.thread = Server('client', 0, self.ip, self.port)
        self.thread.start()

    def isConnected(self):
        return self.thread.isConnected()

    def getAlive(self):
        return self.thread.getAlive()

    def getData(self):
        return self.thread.getdata()

    def sendData(self, data):
        self.thread.send(data)

    def stopServer(self):
        self.thread.setAlive(False)
