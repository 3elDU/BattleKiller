
class Map:
    def __init__(self, mapName, directory=''):
        self.mapName = mapName
        self.map = None
        self.objects = None

        try:
            m = self.load(directory + mapName)
            self.map = eval(m[1])
            self.objects = eval(m[2])
        except Exception as e:
            print('Error:', e)

    @staticmethod
    def load(mapName):
        f = open(mapName)
        c = f.read()
        c = c.split('\n')
        return c

    def getMap(self):
        return self.map

    def getObjects(self):
        return self.objects

    def setMap(self, new):
        self.map = new

    def setObjects(self, new):
        self.map = new

    def setBlockAtMap(self, x, y, block):
        self.map[x, y] = block

    def setBlockAtObjects(self, x, y, block):
        self.objects[x, y] = block
