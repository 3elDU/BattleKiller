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

        self.s = socket.socket()
        self.s.setblocking(False)

    def connect(self):
        timer = 0
        starttimer = time.perf_counter()
        while timer < 10:
            try:
                self.s.connect((self.ip, self.port))
                self.connected = True
            except socket.error:
                pass

            timer = time.perf_counter() - starttimer

    def getdata(self):
        return self.data

    def send(self, data):
        self.data = data

    def run(self):
        self.connect()
        if self.connected:
            while True:
                try:
                    self.data = self.s.recv(16384).decode('utf-8')
                    if self.tosend is not None:
                        self.s.send(self.tosend.encode('utf-8'))
                except socket.error:
                    pass


class Main:
    def __init__(self):
        self.s = socket.socket()
        self.s.setblocking(False)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 2535

        self.thread = Server('server', 0, self.ip, self.port)
        self.thread.run()

    def getIp(self):
        return self.ip, self.port

    def getData(self):
        pass
