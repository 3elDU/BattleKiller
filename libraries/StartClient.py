from threading import *
import pygame
import os
import time

print('LOG: CURRENT DIRECTORY:', os.getcwd())


class _Responser(Thread):
    def __init__(self, msg, classChoice):
        self.msg = msg
        self.clientNum = None
        self.px = None
        self.py = None
        self.spawnx = None
        self.spawny = None
        self.classChoice = classChoice

        self.rotation = 0

        Thread.__init__(self)

        self.isStarted = False
        self.alive = True

        self.lastTime = 0

        self.map = {}
        self.objects = {}
        self.players = []
        self.prev = [0, 0, '', 0]

    def startMessaging(self):
        error = 0

        try:
            self.msg.sendData('cmd-getmap')
            m = self.msg.getData()[0]
            i = 0
            while m is None:
                m = self.msg.getData()
                i += 1
                if i % 100000 == 0:
                    error = 1

            self.map = eval(m)

            time.sleep(1)

            self.msg.sendData('cmd-getobjects')
            o = self.msg.getData()[0]
            i = 0
            while o is None:
                o = self.msg.getData()
                i += 1
                if i % 100000 == 0:
                    error = 1

            self.objects = eval(o)

            time.sleep(1)

            self.msg.sendData("cmd-setplayer[1, 1, 'Healer', 0]")
            time.sleep(1)

            self.msg.sendData('cmd-getnum')
            n = self.msg.getData()[0]
            i = 0
            while n is None:
                n = self.msg.getData()
                i += 1
                if i % 100000 == 0:
                    error = 1

            self.clientNum = int(n)

            if self.clientNum == 0:
                check = 'client'
            elif self.clientNum == 1:
                check = 'client1'

            for x in range(48):
                for y in range(24):
                    if self.objects[x, y] == check:
                        self.spawnx = x
                        self.spawny = y

            self.px = self.spawnx
            self.py = self.spawny

            time.sleep(1)

            print("cmd-setplayer" + str([self.px, self.py, self.classChoice, self.rotation]))
            self.msg.sendData("cmd-setplayer" + str([self.px, self.py, self.classChoice, self.rotation]))

            time.sleep(1)
        except Exception as e:
            error = 1
            print('LOG: startMessaging Error:', e)
        finally:
            if not error:
                self.isStarted = True

    def getStarted(self):
        return self.isStarted

    def getMap(self):
        return [self.map, self.objects]

    def setMap(self, toSet):
        self.map = toSet[0]
        self.objects = toSet[1]

    def setPlayer(self, player):
        self.px, self.py, self.classChoice, self.rotation = player

    def getPlayers(self):
        return self.players

    def getSpawn(self):
        return self.spawnx, self.spawny

    def stop(self):
        self.alive = False

    def run(self):
        print('Thread started!')
        self.startMessaging()
        while not self.isStarted:
            self.startMessaging()

        self.lastTime = time.perf_counter()

        if self.isStarted:
            while self.alive:
                if time.perf_counter() - self.lastTime >= 0.5:
                    try:
                        failed = False

                        self.msg.sendData('cmd-getplayers')
                        p = self.msg.getData()
                        i = 0
                        while p is None:
                            p = self.msg.getData()
                            i += 1
                            if i % 100000 == 0:
                                failed = True
                                break

                        if not failed:
                            for it in p:
                                try:
                                    if eval(it):
                                        self.players = eval(it)
                                        print(self.players)
                                except:
                                    pass
                    except Exception as e:
                        print('cmd-getplayers error:', e)

                    time.sleep(0.1)

                    try:
                        failed = False

                        self.msg.sendData('cmd-getmapchanges')
                        m = self.msg.getData()
                        i = 0
                        while m is None:
                            m = self.msg.getData()
                            i += 1
                            if i % 100000 == 0:
                                failed = True
                                break
                    except Exception as e:
                        print(e)

                    time.sleep(0.1)

                    if not failed:
                        for it in m:
                            try:
                                for block in eval(it):
                                    self.map[block[0], block[1]] = block[2]
                            except:
                                pass

                    failed = False

                    self.msg.sendData('cmd-getobjchanges')
                    o = self.msg.getData()
                    i = 0
                    while o is None:
                        o = self.msg.getData()
                        i += 1
                        if i % 100000 == 0:
                            break

                    if not failed:
                        for it in o:
                            try:
                                for obj in eval(it):
                                    self.objects[obj[0], obj[1]] = obj[2]
                            except:
                                pass

                    time.sleep(0.1)

                    if [self.px, self.py, self.classChoice, self.rotation] != self.prev:
                        self.msg.sendData("cmd-setplayer" + str([self.px, self.py, self.classChoice, self.rotation]))
                        self.prev = [self.px, self.py, self.classChoice, self.rotation]

                    time.sleep(0.1)

                self.lastTime = time.perf_counter()


class Main:
    sc: pygame.Surface

    def __init__(self, pw, ph, gui):
        self.sc: pygame.display

        pygame.init()
        self.font = pygame.font.Font(None, 36)  # Creating font object for future use
        self.logofont = pygame.font.SysFont('arial', 36 * gui)

        self.pw = pw  # Pixel width
        self.ph = ph  # Pixel height
        self.gui = gui  # GUI size multiplier
        self.guisize = 60 * gui
        self.terminate = 0
        self.enemy = []
        self.prevBlocks = {}
        self.prevObjects = {}
        self.changes = {}
        self.objChanges = {}
        self.map = {}
        self.objects = {}
        self.error = False
        self.pclass = None
        self.cont = False
        self.playerAlive = True
        self.opponentAlive = True
        self.clientNum = -1
        self.spawnx = 0
        self.spawny = 0
        self.mw = 48
        self.mh = 24
        self.px = 0
        self.py = 0
        self.rotation = 0
        self.cx = 0
        self.cy = 0

        self.sc = pygame.display.set_mode((48 * self.pw, 24 * self.ph + self.guisize))
        pygame.display.set_caption('BattleKiller ( v. 0.26.10 )')
        self.icon = pygame.image.load('textures/icon.png').convert_alpha()
        pygame.display.set_icon(self.icon)

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

            self.msg.sendData('cmd-start')

            while connected is False:
                if self.msg.getData() == 'start':
                    connected = True

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
            print("LOG: Started responsing!")
        except Exception as e:
            self.terminate = 1
            print("LOG: Game ERROR 72:", e)
            self.msg.sendData('cmd-stop')

        for x in range(self.mw):
            for y in range(self.mh):
                self.prevBlocks[x, y] = 'update'
                self.prevObjects[x, y] = 'update'

        self.ms = _Responser(self.msg, self.classChoice)
        print('Starting thread!')
        self.ms.start()

        started = self.ms.getStarted()
        while not started:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.sendData('cmd-stop')
                    self.msg.stopServer()
                    self.ms.stop()

            self.sc.fill((255, 255, 255))

            t = self.font.render('Handling connection with server...', 1, (0, 0, 0))
            tR = t.get_rect(center=(24 * self.pw, 12 * self.ph))
            self.sc.blit(t, tR)

            pygame.display.update()

            started = self.ms.getStarted()

        s = self.ms.getSpawn()
        self.spawnx = s[0]
        self.spawny = s[1]

        self.px = self.spawnx
        self.py = self.spawny

        print('Handled connection!')

        self.mainLoop()
        pygame.display.quit()
        if self.ms.is_alive():
            self.ms.alive = False
        if self.msg.getAlive():
            self.msg.thread.alive = False
        exit()

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
                    if self.objects[x, y] not in ['None', None, 'client', 'client1']:
                        t = self.mgr.getTexture(self.objects[x, y])
                        t = pygame.transform.scale(t, (self.pw, self.ph))
                        tR = t.get_rect(topleft=(x * self.pw, y * self.ph))
                        self.sc.blit(t, tR)
                        self.prevObjects[x, y] = self.objects[x, y]

    def renderGUI(self):
        pygame.draw.rect(self.sc, (255, 255, 255), (0, 24 * self.ph, 48 * self.pw, self.guisize))

    def fillUpdate(self, fromx, fromy, tox, toy):
        for x in range(fromx, tox):
            for y in range(fromy, toy):
                self.prevBlocks[x, y] = 'update'
                self.prevObjects[x, y] = 'update'

    def renderPlayers(self):
        try:
            t = pygame.transform.scale(self.mgr.getTexture(self.classChoice.lower()), (self.pw * 2, self.ph * 2))
            t = pygame.transform.rotate(t, self.rotation)
            tR = t.get_rect(topleft=((self.px * self.pw) - self.pw // 2, (self.py * self.ph) - self.ph // 2))
            self.sc.blit(t, tR)

            self.fillUpdate(self.px - 1, self.py - 1, self.px + 2, self.py + 2)

            enemy = self.ms.getPlayers()

            e = pygame.transform.scale(self.mgr.getTexture(enemy[2].lower()), (self.pw * 2, self.ph * 2))
            e = pygame.transform.rotate(e, enemy[3])
            eR = e.get_rect(topleft=((enemy[0] * self.pw) - self.pw // 2, enemy[1] * self.ph))
            self.sc.blit(e, eR)

            self.fillUpdate(enemy[0] - 1, enemy[1] - 1, enemy[0] + 2, enemy[1] + 2)
        except:
            pass

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.ms.stop()
                    time.sleep(1)
                    self.msg.sendData('cmd-stop')
                    self.msg.stopServer()
                    alive = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.rotation = 0
            elif keys[pygame.K_a]:
                self.rotation = 90
            elif keys[pygame.K_s]:
                self.rotation = 180
            elif keys[pygame.K_d]:
                self.rotation = -90

            if not alive:
                break

            try:
                self.map = self.ms.getMap()[0]
                self.objects = self.ms.getMap()[1]

                self.ms.setPlayer([self.px, self.py, self.classChoice, self.rotation])
            except:
                pass

            try:
                self.renderField()
                self.renderGUI()
                self.renderPlayers()
            except Exception as e:
                print('Rendering error:', e)

            pygame.display.update()
