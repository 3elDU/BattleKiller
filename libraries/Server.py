import pygame
import os
import time
print('LOG: CURRENT DIRECTORY:', os.getcwd())


class Main:
    def __init__(self, pw, ph, gui):
        pygame.init()
        self.font = pygame.font.Font(None, 36)  # Creating font object for future use
        self.logofont = pygame.font.SysFont('arial', 36 * gui)

        self.pw = pw  # Pixel width
        self.ph = ph  # Pixel height
        self.gui = gui  # GUI size multiplier
        self.guisize = 60 * gui
        self.terminate = 0
        self.prevBlocks = {}
        self.prevObjects = {}
        self.changes = {}
        self.objChanges = {}
        self.error = False
        self.pclass = None
        self.cont = False
        self.mw = 48
        self.mh = 24
        self.px = 0
        self.py = 0
        self.cx = 0
        self.cy = 0

        self.sc = pygame.display.set_mode((48 * self.pw, 24 * self.ph + self.guisize))

        from libraries import TextureManager
        self.textList = ['brick', 'stone', 'grass', 'doorw', 'doorh', 'glass', 'sniper', 'healer', 'swordsman',
                         'builder']
        self.mgr = TextureManager.Main(path='textures/', textureList=self.textList)

        from libraries import StartupSettings
        self.settings = StartupSettings.Main(self.sc, self.pw, self.ph, self.gui)
        data = self.settings.getAll()
        connected = False

        try:
            self.msg = data[1]
            while connected is False:
                connected = data[1].isConnected()
            print("LOG: Connected!")
        except Exception as e:
            self.terminate = 1
            print("LOG: ERROR:", e)

        try:
            pass
        except Exception as e:
            self.terminate = 1
            print("LOG: ERROR:", e)

        print('LOG: Continue:', self.cont)

        if self.cont:
            try:
                self.choice = data[0]
                self.msg = data[1]
                self.terminate = data[2]
                self.mw = data[3]
                self.mh = data[4]
                self.map = data[5]
                self.objects = data[6]
                self.classChoice = data[7]
            except Exception as e:
                self.terminate = 1
                print("ERROR:", e)

            if not self.terminate:
                if self.choice == 0:
                    self.msg.sendData('cmd-getmap')
                    d = self.msg.getData()
                    while d is None:
                        d = self.msg.getData()
                    try:
                        d = d.replace('--', '')
                        d = eval(d)
                        self.mw = d[0]
                        self.mh = d[1]
                        self.map = d[2]
                        self.objects = d[3]
                    except Exception as e:
                        print("LOG: ERROR:", e)
                        self.error = True

                    self.msg.sendData('cmd-getplayer')
                    pdata = self.msg.getData()
                    try:
                        p = pdata.replace('--', '')
                        p = eval(p)
                        self.px = p[0]
                        self.py = p[1]
                        self.cx = p[2]
                        self.cy = p[3]
                        self.pclass = p[4]
                    except Exception as e:
                        print("LOG: ERROR", e)
                        self.error = True
                elif self.choice == 1:
                    for x in range(self.mw):
                        for y in range(self.mh):
                            if self.map[x, y] == 'spawn_server':
                                self.px = x
                                self.py = y
                            elif self.map[x, y] == 'spawn_client':
                                self.cx = x
                                self.cy = y

                    self.msg.sendData('cmd-getclass')
                    pclass = self.msg.getData()
                    while pclass is None:
                        pclass = self.msg.getData()
                    self.pclass = pclass.replace('--', '')

                for x in range(self.mw):
                    for y in range(self.mh):
                        self.prevBlocks[x, y] = 'update'
                        self.prevObjects[x, y] = 'update'
                        self.changes[x, y] = None
                        self.objChanges[x, y] = None

                if not self.error:
                    self.sc = pygame.display.set_mode((self.mw * self.pw, self.mh * self.ph + self.guisize * self.gui))

                    self.mainLoop()
                else:
                    self.msg.sendData('cmd-stop')
                    self.msg.stopServer()
            else:
                self.msg.sendData('cmd-stop')
                self.msg.stopServer()
        else:
            self.msg.sendData('cmd-stop')
            self.msg.stopServer()

    def renderField(self):
        for x in range(self.mw):
            for y in range(self.mh):
                if self.prevBlocks[x, y] != self.map[x, y] or self.prevBlocks[x, y] == 'update':
                    if self.map[x, y] is not None:
                        t = self.mgr.getTexture(self.map[x, y])
                        t = pygame.transform.scale(t, (self.pw, self.ph))
                        tR = t.get_rect(topleft=(x * self.pw, y * self.ph))
                        self.sc.blit(t, tR)
                        self.prevBlocks[x, y] = self.map[x, y]
                    else:
                        pygame.draw.rect(self.sc, (144, 202, 249), (x * self.pw, y * self.ph, self.pw, self.ph))
                if self.objects[x, y] != self.prevObjects[x, y] or self.prevObjects[x, y] == 'update':
                    if self.objects[x, y] not in [None, 'spawn_server', 'spawn_client']:
                        t = self.mgr.getTexture(self.objects[x, y])
                        t = pygame.transform.scale(t, (self.pw, self.ph))
                        tR = t.get_rect(topleft=(x * self.pw, y * self.ph))
                        self.sc.blit(t, tR)
                        self.prevObjects[x, y] = self.objects[x, y]

    def operateData(self, data):
        tosend = ''
        if data is not None:
            print(data)
            if 'cmd-' in data:
                command = data.replace('cmd-', '').replace('--', '')
                if command == 'getmap':
                    if self.choice == 1:
                        tosend = str((self.mw, self.mh, self.map, self.objects))
                elif command == 'stop':
                    self.msg.stopServer()
                    print("LOG: Client-Side error. Stopping server.")
                elif command == 'getmapchanges':
                    tosend = str(self.changes)
                elif command == 'getobjectchanges':
                    tosend = str(self.objChanges)
                elif command == 'getplayer':
                    if self.choice == 0:
                        tosend = str((self.px, self.py, self.classChoice))
                    elif self.choice == 1:
                        tosend = str((self.cx, self.cy, self.px, self.py, self.classChoice))
                elif command == 'getclass':
                    tosend = str(self.classChoice)
        if tosend != '':
            print(tosend)
            self.msg.sendData(tosend + '--')

    def renderGUI(self):
        pass

    def renderPlayers(self):
        try:
            mt = self.mgr.getTexture(self.classChoice.lower())
            mtR = mt.get_rect(topleft=(self.px * self.pw, self.py * self.ph))
            self.sc.blit(mt, mtR)
            self.prevBlocks[self.px, self.py] = 'update'
            self.prevObjects[self.px, self.py] = 'update'

            ct = self.mgr.getTexture(self.pclass)
            ctR = ct.get_rect(topleft=(self.cx * self.pw, self.cy * self.ph))
            self.sc.blit(ct, ctR)
            self.prevBlocks[self.cx, self.cy] = 'update'
            self.prevObjects[self.cx, self.cy] = 'update'
        except Exception as e:
            print("LOG: ERROR:", e)
            self.msg.stopServer()

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    alive = False

            try:
                self.msg.sendData('cmd-getmapchanges')
                changes = self.msg.getData().replace('--', '')
                for x in range(self.mw):
                    for y in range(self.mh):
                        if changes[x, y] is not None:
                            self.map[x, y] = changes[x, y]
                            self.prevBlocks[x, y] = 'update'
                self.msg.sendData('cmd-getobjchanges')
                objchanges = self.msg.getData().replace('--', '')
                for x in range(self.mw):
                    for y in range(self.mh):
                        if objchanges[x, y] is not None:
                            self.objects[x, y] = changes[x, y]
                            self.prevObjects[x, y] = 'update'

                self.msg.sendData('cmd-getplayer')
                pl = eval(self.msg.getData())
                if self.choice == 0:
                    self.cx = pl[2]
                    self.cy = pl[3]
                    self.pclass = pl[4].lower()
                elif self.choice == 1:
                    self.cx = pl[0]
                    self.cy = pl[1]
                    self.pclass = pl[2].lower()
            except Exception as e:
                print("LOG: ERROR:", e)
                self.msg.stopServer()

            self.renderField()
            self.renderGUI()
            self.renderPlayers()
            self.operateData(self.msg.getData())

            pygame.display.update()

            if not self.msg.getAlive():
                print('LOG: Exiting game.')
                alive = False
