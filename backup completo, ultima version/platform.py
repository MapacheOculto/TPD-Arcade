import pygame
from pygame import *

class Platform(pygame.sprite.Sprite):
    
    blue = True
    player = None
 
    change_x = 0
    change_y = 0
    tipo = "Color"
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    blue = True
    color = "Todos"
    i = 0
    j = 0
    imagenoriginal = None
    imagen2 = None
    activada = False
    x_scale = 0
    y_scale = 0
    delta_x = 0
    delta_y = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = spriteimage
        #self.rect = self.image.get_rect()

    def changecolor(self):
        if self.color=="Green":
            self.color = "Blue"
        elif self.color == "Blue":
            self.color = "Green"

