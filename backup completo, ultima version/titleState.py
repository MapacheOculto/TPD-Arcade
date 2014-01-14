# -*- coding: cp1252 -*-
import pygame
from pygame import *
from pygame import mixer
from systemState import systemState
from systemState import gameObject

mixer.init()
select = mixer.Sound('sounds//select.wav')
select.set_volume(0.4)
goBack = mixer.Sound('sounds//back.wav')
goBack.set_volume(0.4)
pygame.mixer.music.load('sounds//titleSong.mp3')

class titleState(gameObject):


    def __init__(self, joystickList, screenSize, systemState):
        self.font1 = pygame.font.SysFont("arial", 50)
        self.font2 = pygame.font.SysFont("arial", 20)
        self.joystickList = joystickList
        self.screenSize = screenSize
        self.systemState = systemState
        self.pointer = 0
        self.playChoice = (0,0,0)
        self.readChoice = (0,0,0)
        
        self.instructionsHub = pygame.image.load("blocks//hub.png").convert_alpha()
        self.instructionsHub = pygame.transform.scale(self.instructionsHub, (screenSize[0] - 100, screenSize[1] - 100))
        self.activateHub = False
        

    def update(self, elapsedTime):

        screen = pygame.display.get_surface()
        direction = 0
        
        if len(self.joystickList) == 2:
            startButton = self.joystickList[1].get_button(0) or self.joystickList[0].get_button(0)
            backButton = self.joystickList[1].get_button(2) or self.joystickList[0].get_button(2)
        else:
            startButton = self.joystickList[0].get_button(0)
            backButton = self.joystickList[0].get_button(2)

        if abs(self.joystickList[0].get_axis(1)) > 0.3 and not self.activateHub:
            direction = self.joystickList[0].get_axis(1)

        if direction < 0 and self.pointer == 1:
            self.pointer = 0
        elif direction > 0 and self.pointer == 0:
            self.pointer = 1
        
        if startButton and self.pointer == 0 and not self.activateHub:
            select.play()
            self.systemState.changeState("gameWorldState")
        elif startButton and self.pointer == 1 and not self.activateHub:
            select.play()
            self.activateHub = True
        elif backButton:
            goBack.play()
            self.activateHub = False
            self.font2.set_bold(True)
    
     
    def render(self):
        screen = pygame.display.get_surface()
        screen.fill((123,87,21))

        if self.pointer == 0:
            self.playChoice = (0,0,255)
            self.readChoice = (0,0,0)
        elif self.pointer == 1:
            self.playChoice = (0,0,0)
            self.readChoice = (0,0,255)

        textSurf  = self.font1.render("MISSED COLOURS" , True,(0, 0, 0))
        screen.blit(textSurf, (self.screenSize[0] / 2 - 200, 100))
        
        textSurf2  = self.font2.render("Jugar" , True, self.playChoice)
        screen.blit(textSurf2, (self.screenSize[0] / 2 - 50, 400))
        
        textSurf3  = self.font2.render("Instrucciones" , True, self.readChoice)
        screen.blit(textSurf3, (self.screenSize[0] / 2 - 50, 500))
            
        if self.activateHub:
            screen.blit(self.instructionsHub,  (50, 50))
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
            
           
