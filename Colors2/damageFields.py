import pygame
from pygame import *
from storyBoard2 import StoryBoard2
from platforms import Platform

class DamageField(Platform):


    # Constructor
    def __init__(self, damageDict, rect):
        super(DamageField, self).__init__()
        self.imageDictionary = damageDict
        self.storyboard = StoryBoard2()
        self.image = self.imageDictionary[1]
        self.rect = rect


    # Metodo que updatea el sprite correspondiente
    def update(self):
        self.animation(len(self.imageDictionary), self.imageDictionary)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))


    # Ahora keys son las imagenes que se pasan a storyboard
    def animation(self, number, images):
        if self.storyboard.inProcess == False:
            self.storyboard.play(number, images)
        elif self.storyboard.inProcess:
            return self.storyboard.update(self, False)
