import pygame


class Main:
    def __init__(self, pw, ph, gui):
        pygame.init()
        self.font = pygame.font.Font(None, 36)  # Creating font object for future use
        self.logofont = pygame.font.SysFont('arial', 36 * gui)

        self.pw = pw  # Pixel width
        self.ph = ph  # Pixel height
        self.gui = gui  # GUI size multiplier
        self.guisize = 30 * gui
        self.terminate = 0

        self.sc = pygame.display.set_mode((48 * self.pw, 24 * self.ph + self.guisize))

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

        self.mapchoice = ''
        acceptedChars = ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.']

        if not self.terminate:
            self.mainLoop()

    def renderField(self):
        pass

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    alive = False

            self.renderField()

            pygame.display.update()
