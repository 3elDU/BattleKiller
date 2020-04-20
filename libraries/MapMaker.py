import libraries.TextureManager
import pygame
from tkinter import *

pygame.init()


class SaveDialog:
    def __init__(self, mapw, maph, gamemap, objects, mode='save', directory='maps/'):
        self.root = Tk()
        self.root.title('Save / Load map')
        self.root.resizable = False

        self.stopped = False
        self.mode = mode
        self.directory = directory
        self.mapw = mapw
        self.maph = maph
        self.gamemap = gamemap
        self.objects = objects
        self.content = None
        self.verified = False

        self.rmapw = 0
        self.rmaph = 0
        self.rmap = {}
        self.robjects = {}

        self.labelsframe = Frame()
        self.entriesframe = Frame()

        self.lbl1 = Label(self.labelsframe, text='Filename: ')
        self.lbl2 = Label(self.labelsframe, text='Filetype: ')

        self.filename = Entry(self.entriesframe, width=32)
        self.filetype = Entry(self.entriesframe, width=32)
        if self.mode == 'save':
            self.savebutton = Button(text="Save map!")
        else:
            self.savebutton = Button(text="Load map!")

        self.packall()

        self.root.mainloop()

    def verify(self, content):
        try:
            parts = content.split('\n')
            wandh = eval(parts[0])
            gamemap = eval(parts[1])
            gameobjects = eval(parts[2])
            if isinstance(wandh, list):
                self.rmapw = wandh[0]
                self.rmaph = wandh[1]
                if isinstance(gamemap, dict):
                    self.rmap = gamemap
                    if isinstance(gameobjects, dict):
                        self.robjects = gameobjects
                        verified = True
                    else:
                        verified = False
                else:
                    verified = False
            else:
                verified = False
        except TypeError and NameError:
            verified = False
        self.verified = verified
        return verified

    def getcontent(self):
        if self.verified:
            toreturn = [[self.rmapw, self.rmaph], self.rmap, self.robjects]
            return toreturn
        else:
            return None

    def getstopped(self):
        return self.stopped

    def loadall(self):
        fName = str(self.filename.get())
        fType = str(self.filetype.get())

        try:
            f = open(self.directory + fName + '.' + fType, 'r')
            self.content = f.read()
            f.close()
        except FileNotFoundError:
            self.content = 'error'

        self.verify(self.content)

        self.root.destroy()
        self.stopped = True

    def saveall(self):
        fName = str(self.filename.get())
        fType = str(self.filetype.get())

        f = open(self.directory + fName + '.' + fType, 'w')

        towrite = ''
        towrite += str([self.mapw, self.maph]) + '\n'
        towrite += str(self.gamemap) + '\n'
        towrite += str(self.objects) + '\n'

        f.write(towrite)
        f.close()

        self.root.destroy()
        self.stopped = True

    def packall(self):
        self.lbl1.pack(side=TOP)
        self.lbl2.pack(side=TOP)
        self.labelsframe.pack(side=LEFT)

        self.filename.pack(side=TOP)
        self.filetype.pack(side=TOP)
        self.filetype.insert(0, 'battleMap')
        self.entriesframe.pack(side=LEFT)

        self.savebutton.pack(side=TOP)
        if self.mode == 'save':
            self.savebutton['command'] = self.saveall
        else:
            self.savebutton['command'] = self.loadall


class Main:
    def __init__(self, mWidth, mHeight, pixSize, fillBlock=None):
        self.mWidth = mWidth
        self.mHeight = mHeight
        self.pixSize = pixSize

        tList = ['brick', 'stone', 'grass', 'doorw', 'doorh', 'glass']
        self.tList = tList
        self.mgr = libraries.TextureManager.Main(path='textures/', textureList=tList)

        self.keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_0, pygame.K_7,
                     pygame.K_8]

        self.map = {}
        self.objects = {}
        self.slots = ['brick', 'stone', 'grass', 'doorw', 'doorh', 'glass', None, 'spawn_client', 'spawn_server']
        self.curslot = 1
        self.prevblocks = {}
        self.prevobjects = {}
        self.fillblock = fillBlock

        self.sc = pygame.display.set_mode((self.mWidth * self.pixSize, self.mHeight * self.pixSize))
        pygame.display.set_caption("Map Maker")

        self.fillMap(fillBlock)
        self.mainLoop()

    def fillMap(self, block):
        for x in range(self.mWidth):
            for y in range(self.mHeight):
                if block not in ['glass', 'doorw', 'doorh']:
                    self.map[x, y] = block
                else:
                    self.map[x, y] = None

                if block in ['glass', 'doorw', 'doorh']:
                    self.objects[x, y] = block
                else:
                    self.objects[x, y] = None
                self.prevblocks[x, y] = None
                self.prevobjects[x, y] = None

    def renderMap(self):
        for x in range(self.mWidth):
            for y in range(self.mHeight):
                if self.prevblocks[x, y] != self.map[x, y] or self.prevblocks[x, y] == 'update':
                    if self.map[x, y] is not None:
                        texture = pygame.transform.scale(self.mgr.getTexture(self.map[x, y]),
                                                         (self.pixSize, self.pixSize))
                        textureRect = texture.get_rect(topleft=(x * self.pixSize, y * self.pixSize))
                        self.sc.blit(texture, textureRect)
                    else:
                        pygame.draw.rect(self.sc, (144, 202, 249),
                                         (x * self.pixSize, y * self.pixSize, self.pixSize, self.pixSize))
                    self.prevblocks[x, y] = self.map[x, y]

                if self.prevobjects[x, y] != self.objects[x, y] or self.prevobjects[x, y] == 'update':
                    if self.objects[x, y] is not None and self.objects[x, y] not in ['spawn_client', 'spawn_server']:
                        texture = pygame.transform.scale(self.mgr.getTexture(self.objects[x, y]),
                                                         (self.pixSize, self.pixSize))
                        textureRect = texture.get_rect(topleft=(x * self.pixSize, y * self.pixSize))
                        self.sc.blit(texture, textureRect)
                    self.prevobjects[x, y] = self.objects[x, y]
                elif self.objects[x, y] == 'spawn_client':
                    pygame.draw.rect(self.sc, (0, 0, 255),
                                     (x * self.pixSize, y * self.pixSize, self.pixSize, self.pixSize))
                elif self.objects[x, y] == 'spawn_server':
                    pygame.draw.rect(self.sc, (255, 0, 0),
                                     (x * self.pixSize, y * self.pixSize, self.pixSize, self.pixSize))

    def click(self, x, y):
        if self.slots[self.curslot - 1] is None:
            self.map[x, y] = None
            self.objects[x, y] = None
        else:
            if self.slots[self.curslot - 1] not in ['glass', 'doorw', 'doorh', 'spawn_client', 'spawn_server']:
                self.map[x, y] = self.slots[self.curslot - 1]
            else:
                self.objects[x, y] = self.slots[self.curslot - 1]

    def updateall(self):
        for x in range(self.mWidth):
            for y in range(self.mHeight):
                self.prevblocks[x, y] = 'update'
                self.prevobjects[x, y] = 'update'

    def resetAll(self):
        self.slots = ['brick', 'stone', 'grass', 'doorw', 'doorh', 'glass', None, 'spawn_client', 'spawn_server']
        self.curslot = 1
        self.prevblocks = {}
        self.prevobjects = {}

        self.sc = pygame.display.set_mode((self.mWidth * self.pixSize, self.mHeight * self.pixSize))
        pygame.display.set_caption("Map Maker")

        for x in range(self.mWidth):
            for y in range(self.mHeight):
                self.prevblocks[x, y] = 'update'
                self.prevobjects[x, y] = 'update'

    def mainLoop(self):
        while 1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN:
                    if i.key in self.keys:
                        self.curslot = self.keys.index(i.key) + 1
                    elif i.key == pygame.K_s:
                        SaveDialog(self.mWidth, self.mHeight, self.map, self.objects)
                    elif i.key == pygame.K_l:
                        s = SaveDialog(self.mWidth, self.mHeight, self.map, self.objects, mode='load')
                        content = s.getcontent()
                        if content is not None:
                            self.mWidth = content[0][0]
                            self.mHeight = content[0][1]
                            self.map = content[1]
                            self.objects = content[2]
                            self.resetAll()
                    elif i.key == pygame.K_f:
                        fBlock = input("Fill block: ")
                        self.fillMap(fBlock)
                    elif i.key == pygame.K_u:
                        self.updateall()
                    elif i.key == pygame.K_r:
                        self.fillMap(self.fillblock)
                    elif i.key == pygame.K_q:
                        exit()

            pos = pygame.mouse.get_pos()
            x = pos[0] // self.pixSize * self.pixSize
            y = pos[1] // self.pixSize * self.pixSize

            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                self.click(x // self.pixSize, y // self.pixSize)

            self.renderMap()

            pygame.draw.rect(self.sc, (0, 0, 0), (x + 1, y + 1, self.pixSize - 1, self.pixSize - 1), 1)
            self.prevblocks[x // self.pixSize, y // self.pixSize] = 'update'
            self.prevobjects[x // self.pixSize, y // self.pixSize] = 'update'

            pygame.display.update()


if __name__ == '__main__':
    try:
        mW = int(input("Map width: "))
        mH = int(input("Map height: "))
        pS = int(input("Block size: "))
        fB = input("Fill block ( texture name ): ")
    except ValueError:
        pass

    try:
        print(mW)
    except NameError:
        mW = 48

    try:
        print(mH)
    except NameError:
        mH = 24

    try:
        print(pS)
    except NameError:
        pS = 16

    try:
        print(fB)
    except NameError:
        fB = 'grass'

    if fB == '':
        fB = 'grass'

    Main(mW, mH, pS, fB)
