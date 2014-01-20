# -*- coding: cp1252 -*-
import pygame
from pygame import *
from pygame import mixer
from systemState import systemState
from systemState import gameObject


class titleState(gameObject):


    def __init__(self, joystickList, screenSize, systemState, container):
        self.font1 = pygame.font.SysFont("Xcelsion", 70)
        self.font2 = pygame.font.SysFont("arial", 20)
        self.font2.set_bold(True)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState
        self.container = container

        self.selectSound = self.container.soundDictionary["select"]
        self.goBackSound = self.container.soundDictionary["back"]
        pygame.mixer.music.load('sounds//test.wav')
        
        self.pointer = 0
        self.playChoice = (0,0,0)
        self.readChoice = (0,0,0)
        self.readChoice2 = (0,0,0)
        self.joystickActivated = False
        
        self.instructionsHub = pygame.image.load("blocks//hub.png").convert_alpha()
        self.instructionsHub = pygame.transform.scale(self.instructionsHub, (screenSize[0] - 100, screenSize[1] - 100))
        self.titleBackground = pygame.image.load("blocks//titleBackground2.png").convert()
        self.titleBackground = pygame.transform.scale(self.titleBackground, (screenSize[0], screenSize[1]))
        self.activateHub = False
        self.activateHub2 = False

        self.buttonPressed = False##
        self.joystickButtonActivated = True
        self.allowButtonPressing = False
        self.button2Pressed = False##
        self.joystickButton2Activated = True
        self.allowButton2Pressing = False
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        

    def update(self, elapsedTime):
        
        self.joystickButtonManager(0)
        self.joystickButtonManager(1)
        
        screen = pygame.display.get_surface()
        direction = 0

        if abs(self.joystickList[0].get_axis(1)) < 0.2:
            self.joystickActivated = False
        elif abs(self.joystickList[0].get_axis(1)) >= 0.4 and not self.activateHub and not self.joystickActivated:
            direction = self.joystickList[0].get_axis(1)

        if direction < 0 and self.pointer > 0:
            self.pointer -= 1
            self.joystickActivated = True
        elif direction > 0 and self.pointer < 2:
            self.pointer += 1
            self.joystickActivated = True
        
        if self.buttonPressed and self.pointer == 0 and not self.activateHub:
            self.selectSound.play()
            self.changeState("gameWorldState")
        elif self.buttonPressed and self.pointer == 1 and not self.activateHub:
            self.selectSound.play()
            self.activateHub = True
        elif self.buttonPressed and self.pointer == 2 and not self.activateHub2:
            self.selectSound.play()
            self.activateHub2 = True
        elif self.button2Pressed:
            self.goBackSound.play()
            self.activateHub = False
            self.activateHub2 = False
            self.font2.set_bold(True)


    def render(self):
        screen = pygame.display.get_surface()
        screen.blit(self.titleBackground, (0,0))

        if self.pointer == 0:
            self.playChoice = (0,0,255)
            self.readChoice = (0,0,0)
            self.readChoice2 = (0,0,0)
        elif self.pointer == 1:
            self.playChoice = (0,0,0)
            self.readChoice = (0,0,255)
            self.readChoice2 = (0,0,0)
        elif self.pointer == 2:
            self.playChoice = (0,0,0)
            self.readChoice = (0,0,0)
            self.readChoice2 = (0,0,255)

        textSurf  = self.font1.render("MISSED COLOURS" , True,(0 , 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 220, 40))
        
        textSurf2  = self.font2.render("Jugar" , True, self.playChoice)
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 100, 400))
        
        textSurf3  = self.font2.render("Instrucciones" , True, self.readChoice)
        screen.blit(textSurf3, (self.screenSize[0] / 2 - 100, 500))
        
        textSurf3  = self.font2.render("Creditos" , True, self.readChoice2)
        screen.blit(textSurf3, (self.screenSize[0] / 2 - 100, 600))

        if self.activateHub2:
            screen.blit(self.instructionsHub,  (50, 30))
            self.font2.set_bold(True)
            textSurf4  = self.font2.render("CREDITOS" , True, (0,0,0))
            screen.blit(textSurf4, (self.screenSize[0] / 2 - 100, 100))

            textSurf5  = self.font2.render("Joe Reynolds  (Professorlamp) - Space_Idea.mp3 - jrtheories.webs.com" , True, (0,0,255)) 
            textSurf6  = self.font2.render("Przemyslaw Sikorski (Rezoner) - happy.mp3 - http://opengameart.org/" , True, (0,0,255))
            textSurf7  = self.font2.render("mrpoly - awesomeness.wav - http://opengameart.org/" , True, (0,0,255))
            textSurf8  = self.font2.render("Joseph Gilbert  (Kistol) - Game Over.ogg - http://opengameart.org/" , True, (0,0,255))
            textSurf9  = self.font2.render("Sonido de pausa : http://soundjax.com/pause-1.html", True, (0,0,255))

            screen.blit(textSurf5, (100, 150))
            screen.blit(textSurf6, (100, 200))
            screen.blit(textSurf7, (100, 250))
            screen.blit(textSurf8, (100, 300))
            screen.blit(textSurf9, (100, 350))

        elif self.activateHub:
            screen.blit(self.instructionsHub,  (50, 30))
            self.font2.set_bold(False)
            textSurf4  = self.font2.render("La meta del juego es llegar al fin de la etapa en cooperación con tu compañero, antes de que se les acabe el tiempo" , True, (0,0,0))

            textSurf5  = self.font2.render("Cada jugador estará representado por un color, y podrá activar plataformas del mismo color al entrar en contacto" , True, (0,0,0)) 
            textSurf6  = self.font2.render("con ellas. Mientras estén inactivas, no podrán ser utilizadas por el jugador del color contrario a estas." , True, (0,0,0))

            textSurf7  = self.font2.render("Al final de cada etapa, se vera el puntaje de cada jugador y  el tiempo en que se termino el nivel." , True, (0,0,0))
            textSurf8  = self.font2.render("Estos 3 datos se guardaran para cada uno de los niveles del juego." , True, (0,0,0))

            textSurf9  = self.font2.render("Habrán dos tipos Orbs en el juego, rojos y rosados. Los rojos recuperaran HP al jugador que los consiga, mientras" , True, (0,0,0))
            textSurf10  = self.font2.render("que los rosados servirán para aumentar el puntaje. Si un jugador con todo su HP absorbe un Orb rojo, ganara puntaje." , True, (0,0,0))

            textSurf11  = self.font2.render("Las balas solo harán daño al jugador del color contrario a estas. Ambos jugadores pueden protegerse mutuamente" , True, (0,0,0))
            textSurf12  = self.font2.render("absorbiendo las balas de su mismo color (y ganaran 10 pts por bala absorbida)" , True, (0,0,0))

            textSurf13  = self.font2.render("El juego usa el stick para moverse de izquierda a derecha, el botón de salto, y el botón de pausa." , True, (0,0,0))
            textSurf14  = self.font2.render("Estos serán los botones que se usaran en los menús secundarios, así como en el juego mismo)" , True, (0,0,0))
            
            screen.blit(textSurf4, (100, 100))
            screen.blit(textSurf5, (100, 150))
            screen.blit(textSurf6, (100, 170))
            screen.blit(textSurf7, (100, 220))
            screen.blit(textSurf8, (100, 240))
            screen.blit(textSurf9, (100, 290))
            screen.blit(textSurf10, (100, 310))
            screen.blit(textSurf11, (100, 360))
            screen.blit(textSurf12, (100, 380))
            screen.blit(textSurf13, (100, 420))
            screen.blit(textSurf14, (100, 440))
            

    # ChangeState
    def changeState(self, stateName):
        self.systemState.changeState(stateName)
        self.systemState.currentState.buttonPressed = False##
        self.systemState.currentState.joystickButtonActivated = True
        self.systemState.currentState.allowButtonPressing = False
        self.systemState.currentState.button2Pressed = False##
        self.systemState.currentState.joystickButton2Activated = True
        self.systemState.currentState.allowButton2Pressing = False


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
            

    
           
