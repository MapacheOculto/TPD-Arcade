import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject
from storyBoard2 import StoryBoard2

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

        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False

        self.storyboard = StoryBoard2()
        self.player1Dictionary = []
        self.player2Dictionary = []
        self.initImageDict()

        self.player1 = pygame.sprite.Sprite()
        self.player2 = pygame.sprite.Sprite()
        self.player1.image = pygame.image.load("still//fire01.png").convert_alpha()
        self.player2.image = pygame.image.load("still//fire01.png").convert_alpha()
        
        self.background = pygame.image.load("blocks//levelEnd3.png").convert()
        self.background = pygame.transform.scale(self.background, (self.screenSize[0],self.screenSize[1])) 


    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False

            
    def setParams(self, time, score1, score2):
        self.time = time
        self.score1 = score1
        self.score2 = score2


    def update(self, elapsedTime):

        self.joystickButtonManager(0)
        self.joystickButtonManager(1)

        if self.buttonPressed:
            self.time = 0
            self.score1 = 0
            self.score2 = 0
            self.changeState("gameWorldState")


    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0,0))

        textSurf  = self.font1.render("Nivel completado!" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 50))

        textSurf2  = self.font2.render("presione b para volver al mapa" , True,(0, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 180, 685))
        
        textSurf3  = self.font2.render("Nivel completado en = " + str(int(self.time)) + " segundos" ,True,(0, 0, 0))
        screen.blit(textSurf3, (self.screenSize[0] / 2 - 200, 620))
        
        textSurf4  = self.font2.render("Puntaje player 1: " + str(self.score1) + " puntos" , True, (0, 0, 0))
        screen.blit(textSurf4, (100, 500))
        textSurf5  = self.font2.render("Puntaje player 2: " + str(self.score2) + " puntos" , True, (0, 0, 0))
        screen.blit(textSurf5, (600, 500))
        
        self.animation(len(self.player1Dictionary), self.player1Dictionary, self.player1)
        self.animation(len(self.player2Dictionary), self.player2Dictionary, self.player2)
        self.player1.image = pygame.transform.scale(self.player1.image, (100,100))
        self.player2.image = pygame.transform.scale(self.player2.image, (100,100))

        screen.blit(self.player1.image,  (150, 350))
        screen.blit(self.player2.image,  (650, 350))


    # Ahora keys son las imagenes que se pasan a storyboard
    def animation(self, number, images, sprite):
        if self.storyboard.inProcess == False:
            self.storyboard.play(number, images)
        elif self.storyboard.inProcess:
            return self.storyboard.update(sprite, False)

        
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

                
    def initImageDict(self):

        self.player1Dictionary.append(pygame.image.load("still//fire01.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("still//fire02.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("still//fire03.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("still//fire04.png").convert_alpha())

        self.player2Dictionary.append(pygame.image.load("still//fire012.png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("still//fire022.png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("still//fire032.png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("still//fire042.png").convert_alpha())

        """
        self.player1Dictionary.append(pygame.image.load("end//dance2.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance3.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance4.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance5.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance6.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance7.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance8.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance9.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance10.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance11.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance12.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance13.png").convert_alpha())
        self.player1Dictionary.append(pygame.image.load("end//dance14.png").convert_alpha())
        
        self.player2Dictionary.append(pygame.image.load("end//dance22 (1).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (2).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (3).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (4).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (5).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (6).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (7).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (8).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (9).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (10).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (11).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (12).png").convert_alpha())
        self.player2Dictionary.append(pygame.image.load("end//dance22 (13).png").convert_alpha())
        """
