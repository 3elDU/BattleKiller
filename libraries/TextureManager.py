import pygame

pygame.init()


class Main:
    def __init__(self, path=None, textureList=None):
        self.path = path

        if path is None:
            self.path = ''
        if textureList is None:
            textureList = []
        self.textures = {}

        if len(textureList) > 0:
            for texture in textureList:
                try:
                    self.textures[texture] = pygame.image.load(self.path + texture + '.png')
                    self.textures[texture] = self.textures[texture].convert_alpha()
                except pygame.error:
                    pass

    def getTexture(self, texture):
        try:
            return self.textures[texture]
        except KeyError:
            return None

    def loadTexture(self, texture):
        if isinstance(texture, list):

            if len(texture) > 0:

                for text in texture:

                    try:
                        self.textures[text] = pygame.image.load(self.path + text + '.txt')
                        self.textures[text] = self.textures[text].convert_alpha()
                    except pygame.error:
                        pass

        elif isinstance(texture, str):
            try:
                self.textures[texture] = pygame.image.load(self.path + texture + '.png').convert_alpha()
            except KeyError:
                pass
