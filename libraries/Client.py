from threading import *
import socket
import time


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

        self.s = socket.socket()
        self.s.setblocking(False)

    def setAlive(self, b):
        self.alive = b

    def getAlive(self):
        return self.alive

    def connect(self):
        timer = 0
        starttimer = time.perf_counter()
        while timer < 5:
            try:
                self.s.connect((self.ip, self.port))
                self.connected = True
            except socket.error:
                pass

            timer = time.perf_counter() - starttimer

    def getdata(self):
        toreturn = self.data
        self.data = None
        return toreturn

    def send(self, data):
        self.tosend = data

    def run(self):
        self.connect()
        if self.connected:
            while self.alive:
                try:
                    self.data = self.s.recv(16384).decode('utf-8')
                except socket.error as e:
                    print(e)

                try:
                    if self.tosend is not None:
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
        self.thread.run()

    def getData(self):
        return self.thread.getdata()

    def sendData(self, data):
        self.thread.send(data)

    def stopServer(self):
        self.thread.setAlive(False)
