import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject

class gameOverState(gameObject):


    def __init__(self, joystickList, screenSize, systemState, container):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 30)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState
        self.container = container

        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False
        
        self.background = pygame.image.load("blocks//gameOver.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screenSize[0],self.screenSize[1]))  



    # ChangeState
    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False


    def update(self, elapsedTime):
        self.joystickButtonManager(0)
        self.joystickButtonManager(1)
        
        if len(self.joystickList) == 2:
            retryButton = self.joystickList[1].get_button(0) or self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[1].get_button(1) or self.joystickList[0].get_button(1)
        else:
            retryButton = self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[0].get_button(1)

        if self.buttonPressed:
            pygame.mixer.music.fadeout(500)
            self.changeState("playState")
            pygame.mixer.music.load('sounds//mainTheme.mp3')
            pygame.mixer.music.play(2)
        elif self.button2Pressed:
            pygame.mixer.music.fadeout(500)
            self.changeState("gameWorldState")
            pygame.mixer.music.load('sounds//test.wav')
            pygame.mixer.music.play()


    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0,0))

        #textSurf  = self.font1.render("GAME OVER" , True,(255, 0, 0))
        #screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 200))
        
        textSurf  = self.font2.render(self.deadMessage , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 220, 350))
        
        textSurf2  = self.font2.render("presione a para tratar de nuevo" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 160, 450))

        textSurf2  = self.font2.render("presione b para volver al mapa" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 160, 550))


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
