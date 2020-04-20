import pygame

pygame.init()


class Main:
    def __init__(self, sc, pw, ph, gui):
        self.sc = sc
        self.font = pygame.font.Font(None, 36)  # Creating font object for future use
        self.logofont = pygame.font.SysFont('arial', 36 * gui)

        self.choice, self.msg, self.terminate, self.mw, self.mh, self.map, self.objects = None, None, None, None, None, None, None

        self.pw = pw  # Pixel width
        self.ph = ph  # Pixel height
        self.gui = gui  # GUI size multiplier
        self.guisize = 30 * gui
        self.terminate = 0

        madeChoice = False
        self.choice = 0

        while not madeChoice:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        madeChoice = True
                    elif e.key == pygame.K_LEFT:
                        if self.choice == 0:
                            self.choice = 1
                        else:
                            self.choice = 0
                    elif e.key == pygame.K_RIGHT:
                        if self.choice == 1:
                            self.choice = 0
                        else:
                            self.choice = 1

            self.sc.fill((255, 255, 255))

            self.logotext = self.logofont.render('BattleKiller', 1, (0, 0, 0))
            self.logorect = self.logotext.get_rect(topleft=(18 * self.pw, 8 * self.ph))
            self.sc.blit(self.logotext, self.logorect)

            if self.choice == 0:
                self.t1 = self.font.render('> Client', 1, (0, 0, 0))
                self.t2 = self.font.render('  Server', 1, (0, 0, 0))
            elif self.choice == 1:
                self.t1 = self.font.render('  Client', 1, (0, 0, 0))
                self.t2 = self.font.render('> Server', 1, (0, 0, 0))

            self.t1r = self.t1.get_rect(center=(8 * self.pw, 12 * self.ph))
            self.t2r = self.t2.get_rect(center=(34 * self.pw, 12 * self.ph))

            self.sc.blit(self.t1, self.t1r)
            self.sc.blit(self.t2, self.t2r)

            pygame.display.update()

        if self.choice == 0:
            from libraries import Client

            self.ip = ''
            self.port = ''
            entry_choice = 0
            madeChoice = False

            acceptedChars = ['0123456789.', '0123456789']

            while not madeChoice:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        self.terminate = True
                        madeChoice = True
                    elif i.type == pygame.KEYDOWN:
                        if i.unicode in acceptedChars[entry_choice]:
                            if entry_choice == 0:
                                self.ip += i.unicode
                            elif entry_choice == 1:
                                self.port += i.unicode
                        if i.key == pygame.K_LEFT:
                            if entry_choice == 0:
                                entry_choice = 1
                            elif entry_choice == 1:
                                entry_choice = 0
                        elif i.key == pygame.K_RIGHT:
                            if entry_choice == 1:
                                entry_choice = 0
                            elif entry_choice == 0:
                                entry_choice = 1
                        elif i.key == pygame.K_BACKSPACE:
                            if entry_choice == 0:
                                if len(self.ip) > 0:
                                    self.ip = self.ip[:len(self.ip) - 1:]
                            elif entry_choice == 1:
                                if len(self.port) > 0:
                                    self.port = self.port[:len(self.port) - 1:]
                        elif i.key == pygame.K_RETURN:
                            madeChoice = True

                self.sc.fill((255, 255, 255))

                self.t1 = self.font.render(self.ip, 1, (0, 0, 0))
                self.t2 = self.font.render(str(self.port), 1, (0, 0, 0))

                self.t1r = self.t1.get_rect(center=(14 * self.pw, 12 * self.ph))
                self.t2r = self.t2.get_rect(center=(34 * self.pw, 12 * self.ph))

                self.sc.blit(self.t1, self.t1r)
                self.sc.blit(self.t2, self.t2r)

                pygame.display.update()

            if not self.terminate:
                self.msg = Client.Main(self.ip, int(self.port))
        elif self.choice == 1:
            from libraries import Server

            self.msg = Server.Main()

            data = self.msg.getIp()
            self.ip = data[0]
            self.port = data[1]

            stopped = False

            while not stopped:
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        self.msg.stopServer()
                        self.terminate = True
                        stopped = True
                    elif i.type == pygame.KEYDOWN:
                        if i.key == pygame.K_RETURN:
                            stopped = True

                self.sc.fill((255, 255, 255))

                self.t1 = self.font.render(str(self.ip), 1, (0, 0, 0))
                self.t2 = self.font.render('2535', 1, (0, 0, 0))

                self.t1r = self.t1.get_rect(center=(14 * self.pw, 12 * self.ph))
                self.t2r = self.t2.get_rect(center=(34 * self.pw, 12 * self.ph))

                self.sc.blit(self.t1, self.t1r)
                self.sc.blit(self.t2, self.t2r)

                pygame.display.update()

            if self.choice == 1:
                self.mapchoice = ''
                acceptedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.'
                madeChoice = 0

                while madeChoice == 0:
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            self.msg.stopServer()
                            self.terminate = True
                            madeChoice = -1
                        elif i.type == pygame.KEYDOWN:
                            if i.unicode in acceptedChars:
                                self.mapchoice += i.unicode
                            if i.key == pygame.K_BACKSPACE:
                                if len(self.mapchoice) > 0:
                                    self.mapchoice = self.mapchoice[:len(self.mapchoice) - 1:]
                            elif i.key == pygame.K_RETURN:
                                madeChoice = 1

                    self.sc.fill((255, 255, 255))

                    t1 = self.font.render(self.mapchoice, 1, (0, 0, 0))
                    t1r = t1.get_rect(center=(24 * self.pw, 12 * self.ph))

                    self.sc.blit(t1, t1r)

                    pygame.display.update()
            else:
                madeChoice = 1
                self.mapchoice = None

            if madeChoice == 1:
                if self.choice == 1:
                    try:
                        f = open('maps/' + self.mapchoice, 'r')
                        m = f.read().split('\n')
                        f.close()
                        self.mw = eval(m[0])[0]
                        self.mh = eval(m[0])[1]
                        self.map = eval(m[1])
                        self.objects = eval(m[2])
                        print('LOG: Map loaded!')
                    except FileNotFoundError:
                        self.terminate = True
                elif self.choice == 0:
                    self.mw = None
                    self.mh = None
                    self.map = None
                    self.objects = None

        self.choices = ['Sniper', 'Healer', 'Swordsman', 'Builder']
        self.classChoice = self.choices[0]
        self.c5 = None
        self.madeChoice = False

        while not self.madeChoice:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    self.terminate = True
                    self.madeChoice = True
                    self.classChoice = None
                elif i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_RIGHT:
                        if self.choices.index(self.classChoice) + 1 == len(self.choices):
                            self.classChoice = self.choices[0]
                        else:
                            self.classChoice = self.choices[self.choices.index(self.classChoice) + 1]
                    elif i.key == pygame.K_LEFT:
                        if self.choices.index(self.classChoice) == 0:
                            self.classChoice = self.choices[len(self.choices) - 1]
                        else:
                            self.classChoice = self.choices[self.choices.index(self.classChoice) - 1]
                    elif i.key == pygame.K_RETURN:
                        self.madeChoice = True

            self.sc.fill((255, 255, 255))

            for text in range(len(self.choices)):
                if self.classChoice == self.choices[text]:
                    t = self.font.render('>' + self.choices[text], 1, (0, 0, 0))
                else:
                    t = self.font.render(self.choices[text], 1, (0, 0, 0))
                tr = t.get_rect(topleft=((2 + 10 * text) * self.pw, 12 * self.ph))
                self.sc.blit(t, tr)

            pygame.display.update()

    def getAll(self):
        return self.choice, self.msg, self.terminate, self.mw, self.mh, self.map, self.objects, self.classChoice
