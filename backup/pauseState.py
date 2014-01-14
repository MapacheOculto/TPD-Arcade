import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject

class PauseState(gameObject):

    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 30)
        self.screenSize = screenSize
        self.joystickList = joystickList
        self.systemState = systemState

    def update(self, elapsedTime):
        pressedKey = pygame.key.get_pressed()
        button = self.joystickList[0].get_button(0) #or self.joystickList[1].get_button(7)##
        if button:
            self.systemState.changeState("playState")
        if pressedKey[K_q]:
            self.systemState.changeState("playState")

    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))

        textSurf  = self.font1.render("PAUSE" , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 200))
        
        textSurf2  = self.font2.render("press tab to return" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 400))
