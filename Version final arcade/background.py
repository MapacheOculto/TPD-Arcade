import pygame
from pygame import *
from pygame import mixer
from storyBoard2 import StoryBoard2
from projectileMotion import ProjectileMotion
from freefall import FreeFall
from _2dLevelMaker import _2dLevelMaker
from platform import Platform

mixer.init() #you must initialize the mixer
alert=mixer.Sound('sounds//jump.wav')


"""
## Path de los sprites normales
imageDictionary = {}
## Path de las animaciones de fondo
lavaAnimation = []
iceAnimation = []
itemAnimation1 = []
itemAnimation2 = []
livesAnimation = []
"""

class Background:

    def __init__(self, screenSize, initialPath):
        
        ## Path de los sprites normales
        self.imageDictionary = {}
        ## Path de las animaciones de fondo
        self.lavaAnimation = []
        self.iceAnimation = []
        self.itemAnimation1 = []
        self.itemAnimation2 = []
        self.livesAnimation = []
        
        self.width = screenSize[0]
        self.height = screenSize[1]
        self.endOfStageReached = False
        self.font = pygame.font.SysFont("arial", 20)
        
        # RELATIVO A GRUPOS Y A LEVELMAKER
        self.initImagesForBackground()
        self.group = pygame.sprite.Group()
        self.exitGroup = pygame.sprite.Group()
        self.damageGroup = pygame.sprite.Group()
        self.itemsGroup = pygame.sprite.Group()
        self.levelMaker = _2dLevelMaker(self.group, self.exitGroup, self.damageGroup, self.itemsGroup, self.imageDictionary, self.lavaAnimation, self.iceAnimation, self.itemAnimation1, self.itemAnimation2, screenSize, initialPath)
        self.groupList = [self.group, self.exitGroup, self.damageGroup] ## VER SI SE PUEDEN HACER GRUPOS DE GRUPOS

        self.moveBackGroundForward = False
        self.moveBackGroundBackward = False
        self.moveBackGroundUp = False
        self.moveBackGroundDown = False
        self.xAdvance = 0
        self.yAdvance = 0

        self.backgroundKey = "fondoDesierto"
        

    def update(self, elapsedTime, playerX, playerY):

        # Obtiene los valores de posicion de primer y ultimo sprite del grupo
        firstRect = self.levelMaker.firstRect
        lastRect = self.levelMaker.lastRect
        
        spriteList = self.group.sprites()

        # La variable advance (x e y) toma valores positivos o negativos, por lo que siempre se suma.
        # (la variable misma determina la direccion al final)
        if self.moveBackGroundForward or self.moveBackGroundBackward:
            self.moveBackGroundForward = False
            self.moveBackGroundBackward = False
            for sprite in self.group: # spriteList:
                sprite.rect = pygame.Rect((sprite.rect.left + self.xAdvance, sprite.rect.top), (sprite.rect.width, sprite.rect.height))
            for exitSprite in self.exitGroup:
                exitSprite.rect = pygame.Rect((exitSprite.rect.left + self.xAdvance, exitSprite.rect.top), (exitSprite.rect.width, exitSprite.rect.height))
            for damageSprite in self.damageGroup:
                damageSprite.rect = pygame.Rect((damageSprite.rect.left + self.xAdvance, damageSprite.rect.top), (damageSprite.rect.width, damageSprite.rect.height))
            for itemSprite in self.itemsGroup:
                itemSprite.rect = pygame.Rect((itemSprite.rect.left + self.xAdvance, itemSprite.rect.top), (itemSprite.rect.width, itemSprite.rect.height))
                   
        if self.moveBackGroundUp or self.moveBackGroundDown: 
            self.moveBackGroundUp = False
            self.moveBackGroundDown = False
            for sprite in self.group: #spriteList:
                sprite.rect = pygame.Rect((sprite.rect.left, sprite.rect.top + self.yAdvance), (sprite.rect.width, sprite.rect.height))
            for exitSprite in self.exitGroup:
                exitSprite.rect = pygame.Rect((exitSprite.rect.left, exitSprite.rect.top + self.yAdvance), (exitSprite.rect.width, exitSprite.rect.height))
            for damageSprite in self.damageGroup:
                damageSprite.rect = pygame.Rect((damageSprite.rect.left, damageSprite.rect.top + self.yAdvance), (damageSprite.rect.width, damageSprite.rect.height))
            for itemSprite in self.itemsGroup:
                itemSprite.rect = pygame.Rect((itemSprite.rect.left, itemSprite.rect.top + self.yAdvance), (itemSprite.rect.width, itemSprite.rect.height))
                 
        self.levelMaker.firstRect = pygame.Rect((firstRect.left + self.xAdvance, firstRect.top + self.yAdvance), (self.levelMaker.stageScale, self.levelMaker.stageScale))
        self.levelMaker.lastRect  = pygame.Rect((lastRect.left  + self.xAdvance, lastRect.top  + self.yAdvance) , (self.levelMaker.stageScale, self.levelMaker.stageScale))

        self.xAdvance = 0
        self.yAdvance = 0

        self.group.update()
        self.damageGroup.update()
        self.itemsGroup.update()
        

    def render(self):
        surface = pygame.display.get_surface()
        surface.blit(self.imageDictionary[self.backgroundKey], (0,0))
        #surface.fill((0,0,0))
        ##Ivan
        for sprite in self.group:
            if sprite.activada:         
                sprite.image = sprite.imagen2
            else:
                sprite.image = sprite.imagenoriginal
        self.group.draw(surface)
        self.exitGroup.draw(surface)
        self.damageGroup.draw(surface)
        self.itemsGroup.draw(surface)


    def changeBackground(self):
        if self.levelMaker.nextStagePath != "---":
            self.backgroundKey = self.levelMaker.nextBackgroundKey
            self.group.empty()
            self.exitGroup.empty()
            self.damageGroup.empty()
            self.itemsGroup.empty()
            #for group in self.groupList:
            #   group.empty()
            self.levelMaker = _2dLevelMaker(self.group, self.exitGroup, self.damageGroup, self.itemsGroup, self.imageDictionary, self.lavaAnimation, self.iceAnimation, self.itemAnimation1, self.itemAnimation2, (self.width, self.height), self.levelMaker.nextStagePath)
        elif self.levelMaker.nextStagePath == "---":
            self.endOfStageReached = True


    def initImagesForBackground(self):

        # Sprites de 100x100
        self.imageDictionary.update({"lowEarth" : pygame.image.load("blocks//lowEarth.tif").convert()})
        self.imageDictionary.update({"topCement" : pygame.image.load("blocks//topa2.png").convert()})
        self.imageDictionary.update({"grass" : pygame.image.load("blocks//grass.png").convert()})
        self.imageDictionary.update({"lava" : pygame.image.load("blocks//lava4.png").convert()})  
        self.imageDictionary.update({"ice" : pygame.image.load("blocks//ice.png").convert()})
        self.imageDictionary.update({"green" : pygame.image.load("blocks//green.png").convert()})
        self.imageDictionary.update({"greenAlpha" : pygame.image.load("blocks//greenAlpha.png").convert()})   
        self.imageDictionary.update({"blue" : pygame.image.load("blocks//blue.png").convert()})
        self.imageDictionary.update({"blueAlpha" : pygame.image.load("blocks//blueAlpha.png").convert()})
        self.imageDictionary.update({"sand" : pygame.image.load("blocks//sand.png").convert()})
        self.imageDictionary.update({"goldBrick" : pygame.image.load("blocks//goldBrick.png").convert()})
        #imageDictionary.update({"bricks" : pygame.image.load("blocks//bricks.png").convert()})

        # imagenes de fondo
        self.imageDictionary.update({"fondo" : pygame.image.load("blocks//asddfg.jpg").convert()})
        self.imageDictionary.update({"fondoDesierto" : pygame.image.load("blocks//fondoDesierto.png").convert()})

        # imagenes con animaciones
        self.lavaAnimation.append(pygame.image.load("blocks//lava1.png").convert_alpha())
        self.lavaAnimation.append(pygame.image.load("blocks//lava2.png").convert_alpha()) 
        self.lavaAnimation.append(pygame.image.load("blocks//lava3.png").convert_alpha())
        self.lavaAnimation.append(pygame.image.load("blocks//lava4.png").convert_alpha())
        
        # imagenes con animaciones
        self.iceAnimation.append(pygame.image.load("blocks//ice0.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice1.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice2.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice3.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice4.png").convert_alpha())

        # Imagenes para items
        self.itemAnimation1.append(pygame.image.load("blocks//life1.png").convert_alpha())
        self.itemAnimation1.append(pygame.image.load("blocks//life1.png").convert_alpha())   
        self.itemAnimation1.append(pygame.image.load("blocks//life2.png").convert_alpha())   
        self.itemAnimation1.append(pygame.image.load("blocks//life2.png").convert_alpha())   

        # Imagenes para items
        self.itemAnimation2.append(pygame.image.load("blocks//points1.png").convert_alpha())
        self.itemAnimation2.append(pygame.image.load("blocks//points1.png").convert_alpha())   
        self.itemAnimation2.append(pygame.image.load("blocks//points2.png").convert_alpha())   
        self.itemAnimation2.append(pygame.image.load("blocks//points2.png").convert_alpha())

