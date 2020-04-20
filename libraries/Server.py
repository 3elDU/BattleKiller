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
        self.conn = None
        self.addr = None
        self.alive = True

        self.s = socket.socket()
        self.s.setblocking(False)

    def connect(self):
        timer = 0
        starttimer = time.perf_counter()
        while timer < 5:
            try:
                self.s.bind((self.ip, self.port))
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

    def setAlive(self, b):
        self.alive = b

    def getAlive(self):
        return self.alive

    def run(self):
        self.connect()
        if self.connected:
            self.s.listen(1)
            while self.alive:
                try:
                    self.conn, self.addr = self.s.accept()
                    print("LOG: NEW CONNECTION:", self.conn, self.addr)
                    break
                except socket.error:
                    pass

            while self.alive:
                try:
                    self.data = self.conn.recv(16384).decode('utf-8')
                except socket.error:
                    pass

                try:
                    if self.tosend is not None:
                        self.conn.send(self.tosend.encode('utf-8'))
                        self.tosend = None
                except socket.error:
                    pass


class Main:
    def __init__(self):
        self.s = socket.socket()
        self.s.setblocking(False)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 2535

        self.thread = Server('server', 0, self.ip, self.port)
        self.thread.start()

    def getAlive(self):
        return self.thread.getAlive()

    def getIp(self):
        return self.ip, self.port

    def getData(self):
        return self.thread.getdata()

    def sendData(self, data):
        self.thread.send(data)

    def stopServer(self):
        self.thread.setAlive(False)
