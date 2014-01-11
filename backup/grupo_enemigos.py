import pygame
from pygame import *

class Balas:
    def __init__(self):
        self.group=pygame.sprite.Group()
        self.lista=[]

    def append(self, sprite):
        self.group.add(sprite.sprite)
        self.lista.append(sprite)
    def update(self, elapsedTime, group, xAdvance, yAdvance, player):
        for bala in self.group.sprites():
            if not bala.update(elapsedTime, group, xAdvance, yAdvance, player):
                self.group.remove(bala)

                
        for bala in self.lista:
            if not bala.update(elapsedTime, group, xAdvance, yAdvance, player):
                self.lista.remove(bala)
        
        
        self.group.update()


    def render(self):
        surface = pygame.display.get_surface()
        self.group.draw(surface)

        for bala in self.lista:
            surface.blit(bala.sprite.image, bala.sprite.rect)



        
