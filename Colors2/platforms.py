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
    contador_movimiento_x = 0
    contador_movimiento_y = 0
    tipo_movimiento = "0"
    lim_x = 0
    lim_y = 10
    id = ""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = spriteimage
        #self.rect = self.image.get_rect()

    def changecolor(self):
        if self.color=="Green":
            self.color = "Blue"
        elif self.color == "Blue":
            self.color = "Green"
    def update(self):
        self.movement(self.tipo_movimiento, self.lim_x, self.lim_y)
        #self.rect.left = self.rect.left + self.delta_x
        self.rect.right = self.rect.right + self.delta_x
        self.rect.top = self.rect.top + self.delta_y
        #self.rect.bottom = self.rect.bottom + self.delta_y

    def movement(self, tipo_movimiento,lim_x,lim_y):
        #Sin movimiento
        if tipo_movimiento == "0":
            return
        ##Movimiento 
        elif tipo_movimiento == "1":
            
            

            if self.contador_movimiento_x == self.lim_x:
                self.delta_x *= -1
                self.contador_movimiento_x *= -1
            elif self.contador_movimiento_x == 0:
                self.delta_x *= -1
            
            if self.contador_movimiento_y == self.lim_y:
                self.delta_y *= -1
                self.contador_movimiento_y *= -1
            elif self.contador_movimiento_y == 0:
                self.delta_y *= -1
            
            self.contador_movimiento_x = self.contador_movimiento_x + 1
            self.contador_movimiento_y = self.contador_movimiento_y + 1

        #elif tipo_movimiento == "2":
        #    as