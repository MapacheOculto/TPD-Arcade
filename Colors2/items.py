import pygame
from pygame import *
from platforms import Platform
from storyBoard2 import StoryBoard2


#Clase de items que dan puntajes
class Items(Platform):

    # Constructor
    def __init__(self, itemsDict, rect):
        super(Items, self).__init__()
        self.imageDictionary = itemsDict
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
