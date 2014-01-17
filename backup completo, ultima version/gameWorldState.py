import pygame
from pygame import *
from pygame import mixer
from systemState import systemState
from systemState import gameObject
from storyBoard2 import StoryBoard2
from level import level


class gameWorldState(object):


    def __init__(self, joystickList, screenSize, systemState, container):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState
        self.storyboard = StoryBoard2()
        self.container = container

        self.gameNodesList = []
        self.createNodes()

        self.playerSprite = pygame.sprite.Sprite()
        self.playerSprite.image = pygame.image.load("still//fire01.png").convert_alpha()
        self.playerSprite.image = pygame.transform.scale(self.playerSprite.image, (50,50))
        self.playerPos = self.gameNodesList[0]
        self.stillDictionary = self.container.path12
        self.walkDictionary = self.container.runPath2
    
        self.moving = False
        self.deltaX = 0
        self.deltaY = 0

        self.background = pygame.image.load("blocks//worldMap.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.screenSize[0],self.screenSize[1]))  
        self.vortex = pygame.image.load("blocks//vortex.png").convert_alpha()
        self.vortex = pygame.transform.scale(self.vortex, (60, 60))
        
        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False


    # Update a las variables relevantes
    def update(self, elapsedTime):

        self.joystickButtonManager(0)
        self.joystickButtonManager(1)
        
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
            
        if self.buttonPressed and not self.moving:    

            self.changeState("playState")
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sounds//mainTheme.mp3')
            pygame.mixer.music.play()
            
            if self.playerPos == self.gameNodesList[0]:
                actualPath = "levels//level11.txt"
            if self.playerPos == self.gameNodesList[1]:
                actualPath = "levels//level21.txt"
            if self.playerPos == self.gameNodesList[2]:
                actualPath = "levels//castle2.txt"
            if self.playerPos == self.gameNodesList[3]:
                actualPath = "levels//test.txt"
            if self.playerPos == self.gameNodesList[4]:
                actualPath = "levels//level3.txt"
            if self.playerPos == self.gameNodesList[5]:  
                actualPath = "levels//level1.txt"
            self.systemState.currentState.currentLevel = level(self.joystickList,  self.screenSize, actualPath, self.container)
            self.systemState.currentState.actualPath = actualPath

        elif self.button2Pressed:
            self.changeState("titleState")

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
            

    ## JOYSTICK
    def joystickButtonManager(self, id):
        if id == 0:
            if  (not self.joystickList[0].get_button(id) and self.joystickButtonActivated):
                self.joystickButtonActivated = False
                self.allowButtonPressing = True
            if (self.joystickList[0].get_button(id) and self.joystickButtonActivated and not self.allowButtonPressing):
                self.buttonPressed = False
            if (self.joystickList[0].get_button(id) and not self.buttonPressed and self.allowButtonPressing):
                self.allowButtonPressing = False
                self.buttonPressed = True
                self.joystickButtonActivated = True
        elif id == 1:
            if (not self.joystickList[0].get_button(id) and self.joystickButton2Activated):
                self.joystickButton2Activated = False
                self.allowButton2Pressing = True
            if (self.joystickList[0].get_button(id) and self.joystickButton2Activated and not self.allowButton2Pressing):
                self.button2Pressed = False
            if (self.joystickList[0].get_button(id) and not self.button2Pressed and self.allowButton2Pressing):
                self.allowButton2Pressing = False
                self.button2Pressed = True
                self.joystickButton2Activated = True

                
    # ChangeState
    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False
        
        
    # Dibuja sprite
    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0,0))
        
        textSurf  = self.font1.render("Mapa del mundo" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 150, 50))

        screen.blit(self.vortex, self.gameNodesList[0])
        screen.blit(self.vortex, self.gameNodesList[1])
        screen.blit(self.vortex, self.gameNodesList[2])
        screen.blit(self.vortex, self.gameNodesList[3])
        screen.blit(self.vortex, self.gameNodesList[4])
        screen.blit(self.vortex, self.gameNodesList[5])
        
        self.playerSprite.image = pygame.transform.scale(self.playerSprite.image , (50, 50))
        screen.blit(self.playerSprite.image, self.playerPos)

        if self.moving:
            self.animation(len(self.walkDictionary), self.walkDictionary)
        elif not self.moving:
            self.animation(len(self.stillDictionary), self.stillDictionary)


    # Ahora keys son las imagenes que se pasan a storyboard
    def animation(self, number, images):
        if self.storyboard.inProcess == False:
            self.storyboard.play(number, images)
        elif self.storyboard.inProcess:
            return self.storyboard.update(self.playerSprite, False)
        
    
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
    

    

