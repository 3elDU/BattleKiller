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
        self.prevBlocks = {}
        self.prevObjects = {}

        self.sc = pygame.display.set_mode((48 * self.pw, 24 * self.ph + self.guisize))

        from libraries import StartupSettings
        self.settings = StartupSettings.Main(self.sc, self.pw, self.ph, self.gui)
        data = self.settings.getAll()

        try:
            self.choice = data[0]
            self.msg = data[1]
            print(self.msg)
            self.terminate = data[2]
            self.mw = data[3]
            self.mh = data[4]
            self.map = data[5]
            self.objects = data[6]
        except Exception as e:
            self.terminate = 1
            print(e)

        if not self.terminate:
            self.mainLoop()
        else:
            self.msg.sendData('cmd-stop')
            self.msg.stopServer()

    def renderField(self):
        pass

    def mainLoop(self):
        alive = True

        while alive:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.msg.stopServer()
                    alive = False

            self.sc.fill((255, 255, 255))

            self.renderField()
            d = self.msg.getData()
            if d is not None:
                print(d)
                self.msg.sendData('wow, cool!')

            pygame.display.update()
