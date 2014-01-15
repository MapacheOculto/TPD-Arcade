import pygame
from pygame import *
from pygame import mixer
from systemState import systemState
from systemState import gameObject
from level import level

mixer.init()
pygame.mixer.music.load('sounds//desert.mp3')

class playState(gameObject):

    def __init__(self, joystickList, screenSize, systemState):
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState

        self.levelDictionary = {}
        self.currentLevel = None
        self.actualPath = None

        self.buttonPressed = False
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False

        
    def update(self, elapsedTime):
        self.joystickButtonManager(0)
        self.joystickButtonManager(1)
        
        self.currentLevel.update(elapsedTime)
        
        if self.button2Pressed:
            #self.currentLevel.pauseGame = False
            self.changeState("pauseState")

        if self.currentLevel.gameOver:
            self.changeState("gameOverState")
            self.systemState.currentState.deadMessage = self.currentLevel.deadMessage
            self.currentLevel = level(self.joystickList, self.screenSize, self.actualPath)

        if self.currentLevel.background.endOfStageReached:
            score1 = self.currentLevel.player1.score
            score2 = self.currentLevel.player2.score
            time = self.currentLevel.totalElapsedTime
            self.changeState("levelEndingState")
            self.systemState.currentState.setParams(time, score1, score2) 


    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 200, 255))
        
        self.currentLevel.render()


    # ChangeState
    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False


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

