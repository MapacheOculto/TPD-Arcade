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
            retryButton = self.joystickList[1].get_button(0) or self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[1].get_button(1) or self.joystickList[0].get_button(1)
        else:
            retryButton = self.joystickList[0].get_button(0)
            goBackButton = self.joystickList[0].get_button(1)

        if retryButton:
            self.systemState.changeState("playState")
        elif goBackButton:
            self.systemState.changeState("gameWorldState")

    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))

        textSurf  = self.font1.render("GAME OVER" , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 200))
        
        textSurf  = self.font2.render(self.deadMessage , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 300))
        
        textSurf2  = self.font2.render("press a to retry" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 450))

        textSurf2  = self.font2.render("press b to return to title screen" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 550))
