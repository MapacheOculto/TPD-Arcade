import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject

class gameOverState(gameObject):


    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 30)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState

    def update(self, elapsedTime):
        
        if len(self.joystickList) == 2:
            retryButton = self.joystickList[1].get_button(7) or self.joystickList[0].get_button(7)
            goBackButton = self.joystickList[1].get_button(3) or self.joystickList[0].get_button(3)
        else:
            retryButton = self.joystickList[0].get_button(7)
            goBackButton = self.joystickList[0].get_button(3)

        if retryButton:
            self.systemState.changeState("playState")
        elif goBackButton:
            self.systemState.changeState("gameWorldState")

    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))

        textSurf  = self.font1.render("GAME OVER" , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 200))
        
        textSurf2  = self.font2.render("press space to retry" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 400))

        textSurf2  = self.font2.render("press tab to retrun to title screen" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 500))
