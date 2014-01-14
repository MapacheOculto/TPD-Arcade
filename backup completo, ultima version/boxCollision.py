import pygame
from pygame.locals import *
from pygame import mixer
from platform import Platform
import math

mixer.init() #you must initialize the mixer
alert=mixer.Sound('sounds//walk.wav')


class boxCollision:


    def __init__(self):
        self.bottomY = 0
        self.topY = 0
        self.rightX = 0
        self.leftX = 0
        self.spriteList = []
        self.lastsprite = None


    # Chequea Colision con grupo. Si la hay, investiga de que direccion se dio. Una vez hecho esto, devuelve un valor
    def CheckCollision2(self, player, group, x1, y1):

        newPos = pygame.Rect(x1, y1, player.sprite.rect.width, player.sprite.rect.height)
        playerMoved = pygame.sprite.Sprite()
        playerMoved.rect = newPos

        spriteListaux = pygame.sprite.spritecollide(playerMoved, group, False)
        self.spriteList = spriteListaux

        if len(spriteListaux) >= 1:
            for sprite in spriteListaux:
                if sprite.color == player.color or sprite.color == "Todos" or sprite.activada :
                    rect = sprite.rect
                    self.topY = rect.top
                    self.bottomY = rect.top + rect.height
                    self.rightX = rect.left + rect.width
                    self.leftX = rect.left
                    if sprite.color == player.color:
                        sprite.activada = True
                    player.colisionada = sprite
                    return True
            sprite.activada = False       
            return False
        else:
           return False  

      # Chequea Colision con grupo. Si la hay, investiga de que direccion se dio. Una vez hecho esto, devuelve un valor
    def CheckCollision(self, player, group, x1, y1):

        newPos = pygame.Rect(x1, y1, player.sprite.rect.width, player.sprite.rect.height)
        playerMoved = pygame.sprite.Sprite()
        playerMoved.rect = newPos

        spriteListaux = pygame.sprite.spritecollide(playerMoved, group, False)
        self.spriteList = spriteListaux

        if len(spriteListaux) >= 1:
            for sprite in spriteListaux:
                if sprite.color == player.color or sprite.color == "Todos" or sprite.activada :
                    rect = sprite.rect
                    self.topY = rect.top + sprite.delta_y
                    self.bottomY = rect.top + rect.height - sprite.delta_y
                    self.rightX = rect.left + rect.width + sprite.delta_x
                    self.leftX = rect.left - sprite.delta_x
                    if sprite.color == player.color:
                        sprite.activada = True
                    player.colisionada = sprite
                    player.deltaX = player.deltaX + sprite.delta_x
                    return True
                elif sprite.activada == False and sprite.tipo =="Color":
                    companeroPos = pygame.Rect(player.companero.X, player.companero.Y+1, player.companero.sprite.rect.width, player.companero.sprite.rect.height)
                    companeroMoved = Platform()
                    companeroMoved.color = player.companero.color
                    companeroMoved.rect = companeroPos
                    if companeroMoved.color == sprite.color and pygame.sprite.collide_rect(sprite,companeroMoved):
                        rect = sprite.rect
                        self.topY = rect.top + sprite.delta_y
                        self.bottomY = rect.top + rect.height - sprite.delta_y
                        self.rightX = rect.left + rect.width + sprite.delta_x
                        self.leftX = rect.left - sprite.delta_x                   
                        sprite.activada = True
                        player.colisionada = sprite
                        player.deltaX = player.deltaX + sprite.delta_x
                        return True
                    else:
                     sprite.activada = False
                    companeroPos = pygame.Rect(player.companero.X+1, player.companero.Y, player.companero.sprite.rect.width, player.companero.sprite.rect.height)
                    companeroMoved = Platform()
                    companeroMoved.color = player.companero.color
                    companeroMoved.rect = companeroPos
                    if companeroMoved.color == sprite.color and pygame.sprite.collide_rect(sprite,companeroMoved):
                        rect = sprite.rect
                        self.topY = rect.top + sprite.delta_y
                        self.bottomY = rect.top + rect.height - sprite.delta_y
                        self.rightX = rect.left + rect.width + sprite.delta_x
                        self.leftX = rect.left - sprite.delta_x                
                        sprite.activada = True
                        player.colisionada = sprite
                        player.deltaX = player.deltaX + sprite.delta_x
                        return True
                    else:
                      sprite.activada = False
                    companeroPos = pygame.Rect(player.companero.X-1, player.companero.Y+1, player.companero.sprite.rect.width, player.companero.sprite.rect.height)
                    companeroMoved = Platform()
                    companeroMoved.color = player.companero.color
                    companeroMoved.rect = companeroPos
                    if companeroMoved.color == sprite.color and pygame.sprite.collide_rect(sprite,companeroMoved):
                        rect = sprite.rect
                        self.topY = rect.top + sprite.delta_y
                        self.bottomY = rect.top + rect.height - sprite.delta_y
                        self.rightX = rect.left + rect.width + sprite.delta_x
                        self.leftX = rect.left - sprite.delta_x                
                        sprite.activada = True
                        player.colisionada = sprite
                        player.deltaX = player.deltaX + sprite.delta_x
                        return True
                    else:
                     sprite.activada = False
            sprite.activada = False       
            return False
        else:
            
            return False  
            
    def getVertex(self, rectangle):
        topRight = (rectangle.left + rectangle.width, rectangle.top)
        topLeft = (rectangle.left, rectangle.top)
        bottomRight = (rectangle.left + rectangle.width, rectangle.top + rectangle.height)
        bottomLeft = (rectangle.left, rectangle.top + rectangle.height)
        return vertexList[topLeft, topRight, bottomRight, bottomLeft]

    def IndividualCollision(self, player,sprite, x1, y1):
        if pygame.sprite.collide_rect(player.sprite, sprite.sprite):
            rect = sprite.sprite.rect
            uncolor=sprite.color
            if uncolor != player.color and uncolor != "Todos":
                return 'Damage'
            
            
            return 'Points'
        return False
        

            
        


    



    
