import pygame
from pygame import *
from boxCollision import boxCollision
from projectileMotion import ProjectileMotion
import math
import random as rd
from grupo_enemigos import Balas



mixer.init()
sonido_laser= mixer.Sound('sounds//laser.wav')
sonido_laser.set_volume(0.5)
sonido_laser2= mixer.Sound('sounds//laser2.wav')
sonido_laser2.set_volume(0.5)


class Bala():
    def __init__(self, x, y, velocidad, angulo, color, clashManager=boxCollision()):
        self.clashManager=clashManager
        self.sprite = pygame.sprite.Sprite()
        self.X = x
        self.Y = y
        self.velocidad=velocidad

        self.color=color
        self.angulo=angulo


        self.sprite.image = pygame.image.load('enemigos//laser_'+self.color+'.png').convert_alpha()
        self.sprite.image=pygame.transform.rotate(self.sprite.image,math.degrees(self.angulo))
        self.width = int(self.sprite.image.get_width())
        self.height = int(self.sprite.image.get_height())
        self.sprite.rect=pygame.Rect((self.X, self.Y), (self.width, self.height))

        if self.color=='Blue':
            sonido_laser.play()

        if self.color=='Green':
            sonido_laser2.play()

    def update(self, elapsedTime, group, xAdvance, yAdvance, player):
        clashingDown = self.clashManager.CheckCollision2(self, group, self.X, self.Y + 1)
        clashingRight = self.clashManager.CheckCollision2(self, group, self.X + 1, self.Y)
        clashingLeft = self.clashManager.CheckCollision2(self, group, self.X - 1, self.Y)
        clashingUp = self.clashManager.CheckCollision2(self, group, self.X, self.Y - 1)

        clashingDown_player = self.clashManager.IndividualCollision(player,self, self.X, self.Y + 1)
        clashingRight_player = self.clashManager.IndividualCollision(player,self,  self.X + 1, self.Y)
        clashingLeft_player = self.clashManager.IndividualCollision(player,self, self.X - 1, self.Y)
        clashingUp_player = self.clashManager.IndividualCollision(player,self, self.X, self.Y - 1)
    
        if not clashingDown and not clashingRight and not clashingUp and not clashingLeft:
            if not clashingDown_player and not clashingRight_player and not clashingLeft_player and not clashingUp_player:
                self.X+=math.cos(self.angulo)*self.velocidad*elapsedTime
                self.Y-=math.sin(self.angulo)*self.velocidad*elapsedTime
                self.X+=xAdvance
                self.Y+=yAdvance
                self.sprite.rect = pygame.Rect((self.X, self.Y), (self.sprite.rect.width, self.sprite.rect.height))
                return True
            else:
                player.takeDamage()
                return False
        
            
        else:
            return False

class Proyectil:
    def __init__(self, x, y, velocidad, angulo,color,clashManager=boxCollision()):
        self.angulo=angulo
        self.velocidad=velocidad
        self.movParab=ProjectileMotion(10, self.velocidad/6, math.degrees(self.angulo))
        self.clashManager=clashManager
        self.sprite = pygame.sprite.Sprite()
        self.X = x
        self.Y = y
 

        self.color=color


        self.sprite.image = pygame.image.load('enemigos//proyectil_'+self.color+'.png').convert_alpha()
        
        self.width = int(self.sprite.image.get_width())
        self.height = int(self.sprite.image.get_height())
        self.sprite.rect=pygame.Rect((self.X, self.Y), (self.width, self.height))

        if self.color=='Blue':
            sonido_laser.play()

        if self.color=='Green':
            sonido_laser2.play()
            
        self.movParab.start(self.Y)
        self.parabTime=0

    def update(self, elapsedTime, group, xAdvance, yAdvance, player):
        clashingDown = self.clashManager.CheckCollision2(self, group, self.X, self.Y + 1)
        clashingRight = self.clashManager.CheckCollision2(self, group, self.X + 1, self.Y)
        clashingLeft = self.clashManager.CheckCollision2(self, group, self.X - 1, self.Y)
        clashingUp = self.clashManager.CheckCollision2(self, group, self.X, self.Y - 1)

        clashingDown_player = self.clashManager.IndividualCollision(player,self, self.X, self.Y + 1)
        clashingRight_player = self.clashManager.IndividualCollision(player,self,  self.X + 1, self.Y)
        clashingLeft_player = self.clashManager.IndividualCollision(player,self, self.X - 1, self.Y)
        clashingUp_player = self.clashManager.IndividualCollision(player,self, self.X, self.Y - 1)

        self.parabTime+=elapsedTime
        
        if not clashingDown and not clashingRight and not clashingUp and not clashingLeft:
            if not clashingDown_player and not clashingRight_player and not clashingLeft_player and not clashingUp_player:
                self.X+=math.cos(self.angulo)*self.velocidad*elapsedTime
            
                self.movParab.update(self.parabTime)
                self.deltaY = int(self.movParab.deltaY)
                if self.deltaY <= -50:
                    self.deltaY = -50
                self.Y-=self.deltaY

                
                self.X+=xAdvance
                self.Y+=yAdvance
                self.sprite.rect = pygame.Rect((self.X, self.Y), (self.sprite.rect.width, self.sprite.rect.height))
                return True
            else:
                player.takeDamage()
                return False

        else:
            return False




class Turret:
    def __init__(self, x, y, color, rafaga, movil, angulo, velocidad, timer_entre_rafaga, timer_entre_bala, tipo):
        self.tipo=tipo
        self.movil=movil
        self.angulo=math.radians(angulo)
        self.balas=Balas()
        self.x=x
        self.y=y
        self.x_giro=0
        self.y_giro=0
        self.sprite=pygame.sprite.Sprite()
        if self.tipo=='Turret':
            self.sprite.image_original=pygame.image.load('enemigos//torreta1.png').convert_alpha()
            self.sprite.image=pygame.image.load('enemigos//torreta1.png').convert_alpha()
            self.cannon=[self.x-15, self.y-10]
        elif self.tipo=='Cannon':
            self.sprite.image_original=pygame.image.load('enemigos//torreta2.png').convert_alpha()
            self.sprite.image=pygame.image.load('enemigos//torreta2.png').convert_alpha()
            self.cannon=[self.x-13, self.y-13]
        self.height=int(self.sprite.image.get_height())
        self.width=int(self.sprite.image.get_width())
        
        self.velocidad=velocidad
        
        self.sprite.rect=pygame.Rect((self.x, self.y), (self.width, self.height))
        self.timer=0
        self.timer_entre_rafaga=timer_entre_rafaga
        self.timer2=0
        self.timer_entre_bala=timer_entre_bala
        self.disparos=0
        self.rafaga=rafaga
        self.color=color
        if self.color=='Multi':
            self.multi=True
            self.color='Green'
        else:
            self.multi=False
        
    def rotar_respecto_esquina(self, ima, angulo, v_x, v_y):
        w = ima.get_width()/2
        h = ima.get_height()/2
        vect_1 = self.rota_vector(v_x,-angulo)
        vect_2 = self.rota_vector(v_y,angulo+90)
        vect_suma = (vect_1[0]+vect_2[0],vect_1[1]+vect_2[1])
        au_x = vect_suma[0]
        au_y = vect_suma[1]
        self.x=self.x-w-au_x
        self.y=self.y-h-au_y
        self.x_giro=-w-au_x
        self.y_giro=-h-au_y
        


    def rota_vector(self, vector, angulo):
        au_x = vector[0]*math.cos(math.radians(angulo))-vector[1]*math.cos(math.radians(angulo))
        au_y = vector[0]*math.sin(math.radians(angulo))+vector[1]*math.sin(math.radians(angulo))
        nuevo =(au_x,au_y)
        return nuevo

    def disparar(self):
        if self.tipo=='Turret':
            self.balas.append(Bala(self.cannon[0], self.cannon[1], self.velocidad, self.angulo, self.color))
        elif self.tipo=='Cannon':
            self.balas.append(Proyectil(self.cannon[0], self.cannon[1],self.velocidad,self.angulo, self.color))
        

    def update(self,elapsedTime,group ,direccion, xAdvance, yAdvance, player, screenSize):
        self.sprite.image=self.sprite.image_original
        self.x+=xAdvance
        self.y+=yAdvance
        self.cannon[0]+=xAdvance
        self.cannon[1]+=yAdvance
        self.x-=self.x_giro
        self.y-=self.y_giro


        if self.movil:
            
            direccion[0]+=int(player.sprite.image.get_width())/2
            direccion[1]+=int(player.sprite.image.get_height())/2

            if direccion[0]<self.x:
                self.angulo=math.pi+math.atan((direccion[1]-self.y)/(self.x-direccion[0]))
            elif direccion[0]>self.x:
                self.angulo=math.atan((direccion[1]-self.y)/(self.x-direccion[0]))
            elif direccion[0]==self.x:
                if direccion[1]<self.y:
                    self.angulo=+math.pi/2
                else:
                    self.angulo=-math.pi/2
                
        

        self.sprite.image=pygame.transform.rotate(self.sprite.image,math.degrees(self.angulo))
        self.rotar_respecto_esquina(self.sprite.image, math.degrees(self.angulo), [self.width/2-(self.width-30),0], [0,self.height/2-30])
        

        self.sprite.rect = pygame.Rect((self.x, self.y), (self.sprite.rect.width, self.sprite.rect.height))
        self.balas.update(elapsedTime, group, xAdvance, yAdvance, player)
        if abs(player.X-self.x)<=screenSize[0] and abs(player.Y-self.y)<=screenSize[1]: 
            if self.timer > self.timer_entre_rafaga:
                if self.disparos < self.rafaga:
                    if self.timer2 > self.timer_entre_bala :
                        self.disparar()
                        self.timer2=0
                        self.disparos+=1
                    else:
                        self.timer2+=elapsedTime

                else:
                    self.disparos=0
                    self.timer=0
                    if self.multi:
                        if self.color=='Green':
                            self.color='Blue'
                        else:
                            self.color='Green'

                    
            else:
                self.timer+=elapsedTime

        
    def render(self):
        self.balas.render()
        surface = pygame.display.get_surface()
        surface.blit(self.sprite.image, self.sprite.rect)
    
