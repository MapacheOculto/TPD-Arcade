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

    def update(self, elapsedTime):
        self.currentLevel.update(elapsedTime)
        
        if self.currentLevel.pauseGame:
            self.currentLevel.pauseGame = False
            self.systemState.changeState("pauseState")

        if self.currentLevel.gameOver:
            self.systemState.changeState("gameOverState")
            self.systemState.currentState.deadMessage = self.currentLevel.deadMessage
            self.currentLevel = level(self.joystickList, self.screenSize, self.actualPath)

        if self.currentLevel.background.endOfStageReached:
            score1 = self.currentLevel.player1.score
            score2 = self.currentLevel.player2.score
            time = self.currentLevel.totalElapsedTime
            self.systemState.changeState("levelEndingState")
            self.systemState.currentState.setParams(time, score1, score2) 


    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((0, 200, 255))
        
        self.currentLevel.render()
