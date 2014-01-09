import pygame
from pygame import *
from pygame import mixer
from systemState import systemState
from systemState import gameObject

mixer.init()
pygame.mixer.music.load('sounds//titleSong.mp3')

class titleState(gameObject):


    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 20)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState


    def update(self, elapsedTime):
        if len(self.joystickList) == 2:
            startButton = self.joystickList[1].get_button(7) or self.joystickList[0].get_button(7)
        else:
            startButton = self.joystickList[0].get_button(7)
        pressedKey = pygame.key.get_pressed()
        if startButton:#pressedKey[K_p]:
            self.systemState.changeState("playState")
    
     
    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((123,87,21))

        textSurf  = self.font1.render("MISSED COLOURS" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 100))
        
        textSurf2  = self.font2.render("press start" , True,(0, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 50, 400))
