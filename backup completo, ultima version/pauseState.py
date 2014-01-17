import pygame
from pygame import *
from systemState import systemState
from systemState import gameObject
from storyBoard2 import StoryBoard2
from items import Items
from pygame import mixer

class PauseState(gameObject):


    def __init__(self, joystickList, screenSize, systemState, container):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 30)
        self.screenSize = screenSize
        self.joystickList = joystickList
        self.systemState = systemState
        self.container = container
        
        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False
        
        self.player1 = pygame.sprite.Sprite()
        self.player2 = pygame.sprite.Sprite()
        self.player1.image = pygame.image.load("still//fire01.png").convert_alpha()
        self.player2.image = pygame.image.load("still//fire01.png").convert_alpha()

        self.storyboard = StoryBoard2()
        self.stillDictionary1 = self.container.path1
        self.stillDictionary2 = self.container.path12
        self.itemDictionary = self.container.itemAnimation2
        
        self.score1 = 0
        self.score2 = 0
        self.hp1 = 0
        self.hp2 = 0
        self.time = 0
        
        self.lifeSprite = Items(self.itemDictionary, pygame.Rect((0,0), (20,20)))
        self.background = pygame.image.load("blocks//pausa.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screenSize[0],self.screenSize[1]))  


    # Setea los datos que se imprimiran en pantalla
    def setParams(self, time, score1, score2, hp1, hp2):
        self.time = time
        self.score1 = score1
        self.score2 = score2
        self.hp1 = hp1
        self.hp2 = hp2

            
    # Update del estado
    def update(self, elapsedTime):
        self.joystickButtonManager(0)
        self.joystickButtonManager(1)
            
        if self.button2Pressed:
            self.changeState("playState")
            pygame.mixer.music.set_volume(1)


    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0,0))

        textSurf  = self.font1.render("PAUSA" , True,(255, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 100, 30))
        
        textSurf2  = self.font2.render("presione b para volver" , True,(255, 0, 0))
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 145, 400))

        self.animation(len(self.stillDictionary1), self.stillDictionary1, self.player1)
        self.animation(len(self.stillDictionary2), self.stillDictionary2, self.player2)
        self.player1.image = pygame.transform.scale(self.player1.image, (50,50))
        self.player2.image = pygame.transform.scale(self.player2.image, (50,50))

        screen.blit(self.player1.image,  (50, 500))
        screen.blit(self.player2.image,  (670, 200))

        for i in range(self.hp2):
            screen.blit(self.lifeSprite.image,  (120 + (i * 25), 500))
        for i in range(self.hp1):
            screen.blit(self.lifeSprite.image,  (720 + (i * 25), 200))
        self.lifeSprite.update()

        
        textSurf3  = self.font2.render("Puntaje player 1: " + str(self.score1) , True,(0, 0, 0))
        screen.blit(textSurf3, (720, 250))
        
        textSurf4  = self.font2.render("Puntaje player 2: " + str(self.score2), True,(0, 0, 0))
        screen.blit(textSurf4, (120, 550))
        
        textSurf5  = self.font2.render("Tiempo restante : "  + str(int(200 - self.time)), True,(255, 0, 0))
        screen.blit(textSurf5, (self.screenSize[0] / 2 - 143, 690))


    # ChangeState
    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False


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
