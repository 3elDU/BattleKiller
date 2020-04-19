class MapLoader:
    def __init__(self, maps, fExtension, pathToFile=''):
        if isinstance(maps, list):
            self.allmaps = {}

            for curMap in maps:
                f = open(pathToFile + curMap + fExtension)
                self.allmaps[str(curMap)] = eval(f.read())
                f.close()

    def getMap(self, mapName):
        if self.allmaps.__contains__(mapName):
            return self.allmaps[mapName]
        else:
            return None

    def setMap(self, mapName, newMap):
        self.allmaps[mapName] = newMap

    def loadMap(self, mapName, fExtension, pathToFile=''):
        f = open(pathToFile + mapName + fExtension)
        c = eval(f.read())
        f.close()
        self.allmaps[mapName] = c
