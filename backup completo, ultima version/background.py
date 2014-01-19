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


class Background:
    

    def __init__(self, screenSize, initialPath, container):
        self.container = container
        ## Path de los sprites normales
        self.imageDictionary = container.imageDictionary
        ## Path de las animaciones de fondo
        self.lavaAnimation = container.lavaAnimation
        self.iceAnimation = container.iceAnimation
        self.itemAnimation1 = container.itemAnimation1
        self.itemAnimation2 = container.itemAnimation2
        self.livesAnimation = container.itemAnimation2
        
        self.width = screenSize[0]
        self.height = screenSize[1]
        self.endOfStageReached = False
        self.font = pygame.font.SysFont("arial", 20)
        
        # RELATIVO A GRUPOS Y A LEVELMAKER
        self.group = pygame.sprite.Group()
        self.exitGroup = pygame.sprite.Group()
        self.damageGroup = pygame.sprite.Group()
        self.itemsGroup = pygame.sprite.Group()
        self.zGroup = pygame.sprite.Group()
        self.levelMaker = _2dLevelMaker(self.group, self.exitGroup, self.damageGroup, self.itemsGroup, self.zGroup, self.container, screenSize, initialPath)
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
            for sprite in self.zGroup:
                sprite.rect = pygame.Rect((sprite.rect.left + self.xAdvance, sprite.rect.top), (sprite.rect.width, sprite.rect.height))
                   
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
            for sprite in self.zGroup:
                sprite.rect = pygame.Rect((sprite.rect.left, sprite.rect.top + self.yAdvance), (sprite.rect.width, sprite.rect.height))
                 
        self.levelMaker.firstRect = pygame.Rect((firstRect.left + self.xAdvance, firstRect.top + self.yAdvance), (self.levelMaker.stageScale, self.levelMaker.stageScale))
        self.levelMaker.lastRect  = pygame.Rect((lastRect.left  + self.xAdvance, lastRect.top  + self.yAdvance) , (self.levelMaker.stageScale, self.levelMaker.stageScale))

        self.xAdvance = 0
        self.yAdvance = 0

        self.group.update()
        self.damageGroup.update()
        self.itemsGroup.update()
        

    def render(self):
        surface = pygame.display.get_surface()
        #surface.blit(self.imageDictionary[self.backgroundKey], (0,0))
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
            self.levelMaker = _2dLevelMaker(self.group, self.exitGroup, self.damageGroup, self.itemsGroup, self.zGroup, self.container, (self.width, self.height), self.levelMaker.nextStagePath)
        elif self.levelMaker.nextStagePath == "---":
            self.endOfStageReached = True
