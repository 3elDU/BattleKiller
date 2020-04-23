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
        self.objChanges = {}
        self.map = {}
        self.objects = {}
        self.error = False
        self.pclass = None
        self.cont = False
        self.choice = 0
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

        from libraries import StartupSettingsClient
        self.settings = StartupSettingsClient.Main(self.sc, self.pw, self.ph, self.gui)
        data = self.settings.getAll()
        connected = False

        try:
            self.msg = data[0]
            self.terminate = data[1]
            self.classChoice = data[2]
            while connected is False:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        self.terminate = 1
                        self.error = True
                        self.msg.sendData('cmd-stop')
                        self.msg.stopServer()
                        exit()

                self.sc.fill((255, 255, 255))

                t = self.font.render('Connecting...', 1, (0, 0, 0))
                tR = t.get_rect(center=((self.mw // 2) * 16, (self.mh // 2) * 16))
                self.sc.blit(t, tR)

                pygame.display.update()

                connected = self.msg.isConnected()
            print("LOG: Connected!")
        except Exception as e:
            self.terminate = 1
            print("LOG: ERROR:", e)

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
        pass

    def renderGUI(self):
        pass

    def renderPlayers(self):
        pass

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    alive = False

            self.renderField()
            self.renderGUI()
            self.renderPlayers()

            pygame.display.update()
