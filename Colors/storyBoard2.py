import pygame
from pygame.locals import *

class StoryBoard2:
    
    textureKeys = []
    
    totalElapsedTime = 0
    contador = 0
    actualFrame = int()
    frameNumber = int()
    inProcess = False

    def __init__(self):
        self.inProcess = False

    def setTexture(self, index, actualSprite, flip):
        if flip:
            actualSprite.image = pygame.transform.flip(self.textureKeys[index], True, False)
        else:
            actualSprite.image = self.textureKeys[index]

    def play(self, frameNumber, textureKeys = []):
        self.textureKeys = textureKeys
        self.frameNumber = frameNumber
        self.inProcess = True
        self.actualFrame = 0

    def update(self, actualSprite, flip):
        self.actualFrame += 1
        index = self.actualFrame - 1
        if self.inProcess and self.actualFrame != self.frameNumber:
            self.setTexture(index, actualSprite, flip)
        if self.actualFrame == self.frameNumber:
            self.inProcess = False
            return
        
    def stop(self):
        self.inProcess = False
