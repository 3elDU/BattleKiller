
class Map:
    def __init__(self, mapName, directory=''):
        self.mapName = mapName

        try:
            self.load(directory + mapName)
        except Exception as e:
            print('Error:', e)

    @staticmethod
    def load(mapName):
        f = open(mapName)
        c = f.read()
        c = c.split('\n')
        return c
