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

    def setParams(self, time, score1, score2):
        self.time = time
        self.score1 = score1
        self.score2 = score2

    def update(self, elapsedTime):
        
        if len(self.joystickList) == 2:
            goBackButton = self.joystickList[1].get_button(7) or self.joystickList[0].get_button(7)
        else:
            goBackButton = self.joystickList[0].get_button(7)

        if goBackButton:
            self.time = 0
            self.score1 = 0
            self.score2 = 0
            self.systemState.changeState("gameWorldState")

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



