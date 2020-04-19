import socket


class Main:
    def __init__(self):
        self.s = socket.socket()
        self.s.setblocking(False)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 2535

    def getData(self):
        return self.ip, self.port
