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
        self.setLevels()
        self.currentLevel = None
        self.actualPath = None

    def setLevels(self):
        pass
        """
        self.level1 = level(self.joystickList,  self.screenSize, "levels//test.txt")
        self.level2 = level(self.joystickList,  self.screenSize, "levels//test2.txt")
        self.level3 = level(self.joystickList,  self.screenSize, "levels//castle2.txt")
        self.level4 = level(self.joystickList,  self.screenSize, "levels//level1.txt")
        self.level5 = level(self.joystickList,  self.screenSize, "levels//level3.txt")
        self.level6 = level(self.joystickList,  self.screenSize, "levels//castle.txt")
        
        self.levelDictionary.update({"level1":self.level1})
        self.levelDictionary.update({"level2":self.level2})
        self.levelDictionary.update({"level3":self.level3})
        self.levelDictionary.update({"level4":self.level4})
        self.levelDictionary.update({"level5":self.level5})
        self.levelDictionary.update({"level6":self.level6})
        """

    def update(self, elapsedTime):
        self.currentLevel.update(elapsedTime)
        
        if self.currentLevel.pauseGame:
            self.currentLevel.pauseGame = False
            self.systemState.changeState("pauseState")

        if self.currentLevel.gameOver:
            self.systemState.changeState("gameOverState")
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
