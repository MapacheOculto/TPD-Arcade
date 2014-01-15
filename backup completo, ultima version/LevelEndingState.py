import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject

class LevelEndingState(object):

    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 30)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState

        self.score1 = 0
        self.score2 = 0
        self.time = 0

        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False


    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False

            
    def setParams(self, time, score1, score2):
        self.time = time
        self.score1 = score1
        self.score2 = score2


    def update(self, elapsedTime):

        self.joystickButtonManager(0)
        self.joystickButtonManager(1)

        if self.buttonPressed:
            self.time = 0
            self.score1 = 0
            self.score2 = 0
            self.changeState("gameWorldState")


    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((235, 100, 169))

        textSurf  = self.font1.render("Level accomplished!" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 100))

        textSurf2  = self.font2.render("press other button to retrun to world maps" , True,(0, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 200, 250))
        
        textSurf3  = self.font2.render("Stage completed in = " + str(self.time) + " seconds" ,True,(0, 0, 0))
        screen.blit(textSurf3, (100, 400))
        textSurf4  = self.font2.render("Player 1 score = " + str(self.score1) + "points" ,True,(0, 0, 0))
        screen.blit(textSurf4, (100, 500))
        textSurf5  = self.font2.render("Player 1 score = " + str(self.score2) + "points" ,True,(0, 0, 0))
        screen.blit(textSurf5, (100, 600))


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
