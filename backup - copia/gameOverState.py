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
            startButton = self.joystickList[1].get_button(7) or self.joystickList[0].get_button(7)
        else:
            startButton = self.joystickList[0].get_button(7)

        pressedKey = pygame.key.get_pressed()
        
        if startButton:#pressedKey[K_SPACE]:
            self.systemState.changeState("playState")
        if pressedKey[K_TAB]:
            self.systemState.changeState("titleState")

    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))

        textSurf  = self.font1.render("GAME OVER" , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 200))
        
        textSurf2  = self.font2.render("press space to retry" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 400))

        textSurf2  = self.font2.render("press tab to retrun to title screen" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 500))
