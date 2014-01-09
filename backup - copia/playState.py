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
        self.level1 = level(self.joystickList, screenSize)

    def update(self, elapsedTime):
        self.level1.update(elapsedTime)

        if self.level1.pauseGame:
            self.level1.pauseGame = False
            self.systemState.changeState("pauseState")
        if self.level1.gameOver:
            self.systemState.changeState("gameOverState")
            self.level1 = level(self.joystickList, self.screenSize)


    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 200, 255))

        self.level1.render()
