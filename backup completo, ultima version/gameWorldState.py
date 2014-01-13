import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject
from level import level


class gameWorldState(object):


    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState

        self.gameNodesList = []
        self.createNodes()

        self.playerSprite = pygame.sprite.Sprite()
        self.playerSprite.image = pygame.image.load("still//fire01.png").convert_alpha()
        self.playerSprite.image = pygame.transform.scale(self.playerSprite.image, (50,50))
        self.playerPos = self.gameNodesList[0]
    
        self.moving = False
        self.deltaX = 0
        self.deltaY = 0

    # Update a las variables relevantes
    def update(self, elapsedTime):

        # Parametros de iteracion
        playerInNode = self.playerInNode()
        temporalXDirection = 0
        temporalYDirection = 0
        
        # Botones de eleccion
        if len(self.joystickList) == 2:
            levelSelectionButton = self.joystickList[1].get_button(0) or self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[1].get_button(1) or self.joystickList[0].get_button(1)
        else:
            levelSelectionButton = self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[0].get_button(1)
        if levelSelectionButton and not self.moving:
            self.systemState.changeState("playState") 
            if self.playerPos == self.gameNodesList[0]:
                actualPath = "levels//test.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//test.txt"
            if self.playerPos == self.gameNodesList[1]:
                actualPath = "levels//ex1.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//ex1.txt"
            if self.playerPos == self.gameNodesList[2]:
                actualPath = "levels//castle2.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//castle2.txt"
            if self.playerPos == self.gameNodesList[3]:
                actualPath = "levels//level1.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//level1.txt"
            if self.playerPos == self.gameNodesList[4]:
                actualPath = "levels//level3.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//level3.txt"
            if self.playerPos == self.gameNodesList[5]:  
                actualPath = "levels//castle.txt"
                self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath)
                self.systemState.currentState.actualPath = "levels//castle.txt"
        elif goBackButton:
            self.systemState.changeState("titleState")

        # Obtiene si player apreto boton para desplazarse
        if abs(self.joystickList[0].get_axis(0)) > 0.3 and not self.moving and playerInNode:##
            temporalXDirection = self.joystickList[0].get_axis(0)##
        elif abs(self.joystickList[0].get_axis(1)) > 0.3 and not self.moving and playerInNode:##
            temporalYDirection = self.joystickList[0].get_axis(1)##

        # Se encarga de los desplazamientos
        if temporalXDirection > 0 and self.playerPos[0] != self.gameNodesList[2][0]:
            self.startMoving(self.playerPos, (self.playerPos[0] + 300, self.playerPos[1]))
        elif temporalXDirection < 0 and self.playerPos[0] != self.gameNodesList[0][0]:
            self.startMoving(self.playerPos, (self.playerPos[0] - 300, self.playerPos[1] + 1))

        if temporalYDirection < 0 and self.playerPos[1] != self.gameNodesList[0][1]:
            self.startMoving(self.playerPos, (self.playerPos[0], self.playerPos[1] - 200))
        elif temporalYDirection > 0 and self.playerPos[1] != self.gameNodesList[5][1]:
            self.startMoving(self.playerPos, (self.playerPos[0], self.playerPos[1] + 200))

        # Si se esta moviendo de un nodo a otro
        if self.moving:
            self.updateMovement()


    # Dibuja sprite
    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((244, 164, 69))
        
        textSurf  = self.font1.render("GAME WORLD" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 150, 50))

        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[0], 20)
        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[1], 20)
        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[2], 20)
        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[3], 20)
        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[4], 20)
        pygame.draw.circle(screen, (0,0,255), self.gameNodesList[5], 20)

        screen.blit(self.playerSprite.image, self.playerPos)
    
    # Nodos donde se ubicaran visualmente los iconos a seleccionar
    def createNodes(self): 
        self.gameNodesList = [(200, 300), (500, 300), (800, 300), (800, 500), (500, 500), (200, 500)]

    def playerInNode(self):
        if self.playerPos == self.gameNodesList[0] or self.playerPos == self.gameNodesList[1] or self.playerPos == self.gameNodesList[2] or self.playerPos == self.gameNodesList[3] or self.playerPos == self.gameNodesList[4] or self.playerPos == self.gameNodesList[5]:
            return True
        return False

    def startMoving(self, initialNode, finalNode):
        self.moving = True
        if finalNode[0] != initialNode[0]:
            self.deltaX = (finalNode[0] - initialNode[0]) / 10
        elif finalNode[1] != initialNode[1]:
            self.deltaY = (finalNode[1] - initialNode[1]) / 10

    def updateMovement(self):

        self.playerPos = (self.playerPos[0] + self.deltaX, self.playerPos[1] + self.deltaY)
        
        if self.playerInNode():
            self.deltaX = 0
            self.deltaY = 0
            self.moving = False

    

