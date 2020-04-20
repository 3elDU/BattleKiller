import pygame
import os
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
        self.error = False

        from libraries import TextureManager
        self.textList = ['brick', 'stone', 'grass', 'doorw', 'doorh', 'glass', 'sniper', 'healer', 'swordsman', 'builder']
        self.mgr = TextureManager.Main(path='textures/', textureList=self.textList)

        self.sc = pygame.display.set_mode((48 * self.pw, 24 * self.ph + self.guisize))

        from libraries import StartupSettings
        self.settings = StartupSettings.Main(self.sc, self.pw, self.ph, self.gui)
        data = self.settings.getAll()

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

            for x in range(self.mw):
                for y in range(self.mh):
                    self.prevBlocks[x, y] = 'update'
                    self.prevObjects[x, y] = 'update'

            if not self.error:
                self.sc = pygame.display.set_mode((self.mw * self.pw, self.mh * self.ph + self.guisize * self.gui))

                self.mainLoop()
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
                    if self.objects[x, y] is not None:
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
                command = data.replace('cmd-', '')
                if command == 'getmap':
                    if self.choice == 1:
                        tosend = str((self.mw, self.mh, self.map, self.objects))
                elif command == 'stop':
                    self.msg.stopServer()
                    print("LOG: Client-Side error. Stopping server.")
                elif command == 'getchanges':
                    tosend = str(self.changes)
        if tosend != '':
            print(tosend)
            self.msg.sendData(tosend + '--')

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    alive = False

            self.renderField()
            self.operateData(self.msg.getData())

            pygame.display.update()

            if not self.msg.getAlive():
                print('LOG: Exiting game.')
                alive = False
