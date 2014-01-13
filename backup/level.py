import pygame
import math
from pygame import *
from player import Player
from background import Background
from pygame import mixer
from storyBoard2 import StoryBoard2
from projectileMotion import ProjectileMotion
from freefall import FreeFall


# Relativo a los sonidos
mixer.init()
murunf = mixer.Sound('sounds//Murunf.mp3')
murunf.set_volume(0.1)
walk = mixer.Sound('sounds//walk2.wav')
walk.set_volume(0.1)
alert = mixer.Sound('sounds//jump.wav')
alert.set_volume(0.1)
slide=mixer.Sound('sounds//slide.wav')
slide.set_volume(0.1)

class level:
    
    # Constructor
    def __init__(self, joystickList, screenSize, initialPath):

        self.screenSize = screenSize
        self.joystickList = joystickList
        self.font = pygame.font.SysFont("arial", 16)
        self.pauseGame = False
        self.gameOver = False
        self.playerInDeadZone = False
        self.totalElapsedTime = 0

        self.background = Background(self.screenSize, initialPath)

        x = self.background.levelMaker.startXPosition
        y = self.background.levelMaker.startYPosition

        if len(self.joystickList) == 2 and self.joystickList != None:
            self.player1  = Player(self.joystickList[1], ProjectileMotion(), FreeFall(15), StoryBoard2(), x, y)
            self.player2 = Player(self.joystickList[0], ProjectileMotion(), FreeFall(15), StoryBoard2(), x, y) #-----------------#
        else:
            self.player1 = Player(self.joystickList[0], ProjectileMotion(), FreeFall(15), StoryBoard2(), x, y)
            self.player2 = Player(self.joystickList[0], ProjectileMotion(), FreeFall(15), StoryBoard2(), x, y) #-----------------#
        self.player1.id = "p1"
        self.player2.id = "p2"
        
        self.player1.companero = self.player2
        self.player2.companero = self.player1

        # Flecha guia (para ubicar a otro player
        self.compassImageUp   = pygame.image.load("blocks//arrowUp.png").convert_alpha()
        self.compassImageDown = pygame.image.load("blocks//arrowDown.png").convert_alpha()
        self.compassImageRight = pygame.image.load("blocks//arrowRight.png").convert_alpha()
        self.compassImageLeft = pygame.image.load("blocks//arrowLeft.png").convert_alpha()
        self.compass = pygame.sprite.Sprite()
        self.compass.image = self.compassImageUp
        self.verticalCompassNeeded  = False
        self.horizontalCompassNeeded = False
        self.P1horizontalCompassNeeded = False

  
    # Update de todas las variables relevantes
    def update(self, elapsedTime):

        # Tiempo
        self.totalElapsedTime += elapsedTime
        """
        # Tiempo maximo para pasar etapa
        if self.totalElapsedTime > 100:
            self.gameOver = True
        """

        # Brujula que apunta a player 2
        if  self.player2.Y <= -50 or self.player2.Y >= self.screenSize[1]:
            self.horizontalCompassNeeded = True
        elif self.player2.X <= -50 or self.player2.X >= self.screenSize[0]:
            self.verticalCompassNeeded = True
        else:
            self.horizontalCompassNeeded = False
            self.verticalCompassNeeded = False
            
        # Brujula que apunta a player 1
        if  self.player1.Y <= -50 or self.player1.Y >= self.screenSize[1]:
            self.P1horizontalCompassNeeded = True
        else:
            self.P1horizontalCompassNeeded = False
        
        # Update a las instancias del nivel
        #for sprite in self.background.group:
        #   if sprite.activada:
        #       if not((self.player1.color == sprite.color and pygame.sprite.collide_rect(sprite,self.player1.sprite))) and  not((self.player2.color == sprite.color and pygame.sprite.collide_rect(sprite,self.player2.sprite)))  :
        #            sprite.activada = False
        #       if not((self.player2.color == sprite.color and pygame.sprite.collide_rect(sprite,self.player2.sprite))):
        #           sprite.activada = False
               #else:
               #   sprite.activada = False
        #for sprite in self.background.group:
        #    if sprite.activada:
        #        if (pygame.sprite.collide_rect(sprite,self.player1.sprite)):
        #               if(self.player1.color == sprite.color):
        #                   sprite.activada = True
        #        if (pygame.sprite.collide_rect(sprite,self.player2.sprite)):
        #               if(self.player2.color == sprite.color):
        #                   sprite.activada = True
        
        for sprite in self.background.group:
            sprite.activada = False             
        self.player2.update(elapsedTime, self.background.group, self.background.exitGroup, self.background.damageGroup, self.background.groupList)#-----------------#
        self.player1.update(elapsedTime, self.background.group, self.background.exitGroup, self.background.damageGroup, self.background.groupList)
        self.backgroundXMovementManager(self.player1, self.player2)
        self.backgroundYMovementManager(self.player1, self.player2)
        for torreta in self.background.levelMaker.torretas:
            if torreta.color=='Green':
                torreta.update(elapsedTime,self.background.group,[self.player1.X,self.player1.Y],self.background.xAdvance, self.background.yAdvance, self.player1, self.screenSize)
            elif torreta.color=='Blue':
                torreta.update(elapsedTime,self.background.group,[self.player2.X,self.player2.Y],self.background.xAdvance, self.background.yAdvance, self.player2, self.screenSize)
        self.background.update(elapsedTime, self.player1.X, self.player1.Y)
        
        """
        # DISTANCIA PERSONAJES (TEMPORAL)
        if abs(self.player1.X - self.player2.X) >= self.screenSize[0]:
            self.player2.X = self.player1.X
            self.player2.Y = self.player1.Y
        if abs(self.player1.Y - self.player2.Y) >= self.screenSize[1]:
            self.player2.X = self.player1.X
            self.player2.Y = self.player1.Y
        #"""   

        #######PAUSA(con joystick)##################################
        button = self.joystickList[0].get_button(8) #or self.joystickList[1].get_button(7)##
        #button2 = self.joystickList[1].get_button(9) #or self.joystickList[1].get_button(7)##
        if button:
            self.pauseGame = True
        pressedKey = pygame.key.get_pressed()
        if pressedKey[K_TAB]:
            self.pauseGame = True
        #if button2:
        #    self.gameOver = True


        ###########CAMBIO_DE_ETAPA##################################
        if self.player1.exitStage or self.player2.exitStage:
            self.player1.exitStage = False
            self.player2.exitStage = False
            self.background.changeBackground()
            self.player1.X = self.background.levelMaker.startXPosition
            self.player1.Y = self.background.levelMaker.startYPosition
            self.player2.X = self.background.levelMaker.startXPosition 
            self.player2.Y = self.background.levelMaker.startYPosition

        #################GAME_OVER##################################
        if self.player1.dead or self.player2.dead:
            self.gameOver = True
                 

    # Dibuja en pantalla los sprites y el escenario
    def render(self):
        
        # Instancia de la ventana de pygame
        screen = pygame.display.get_surface()

        # Render a las instancias del nivel
        self.background.render()
        self.player2.render()   #-----------------#
        self.player1.render()
        for torreta in self.background.levelMaker.torretas:
            torreta.render()

        # Brujula que apunta a otro player
        if self.horizontalCompassNeeded or self.P1horizontalCompassNeeded:
            if self.player2.Y <= -50 or self.player1.Y <= -50:
                self.compass.image = self.compassImageUp
                if self.player2.Y <= -50:
                    screen.blit(self.compass.image, (self.player2.X, 0))
                else:
                    screen.blit(self.compass.image, (self.player1.X, 0))
            if self.player2.Y >= self.screenSize[1] or self.player1.Y >= self.screenSize[1]:
                self.compass.image = self.compassImageDown
                if self.player2.Y >= self.screenSize[1]:
                    screen.blit(self.compass.image, (self.player2.X, self.screenSize[1] - 15))
                else:
                    screen.blit(self.compass.image, (self.player1.X, self.screenSize[1] - 15))
        if self.verticalCompassNeeded:
            if self.player2.X <= -50:
                self.compass.image = self.compassImageLeft
                screen.blit(self.compass.image, (0, self.player2.Y))
            if self.player2.X >= self.screenSize[0]:
                self.compass.image = self.compassImageRight
                screen.blit(self.compass.image, ((self.screenSize[0] - 15), self.player2.Y))


        # Aqui va por si se quiere escribir algo en Pantalla.
        # Actualmente : Posicion mas otros 
        textSurf  = self.font.render("("+str(int(self.player1.X))+" , "+str(int(self.player1.Y))+")" , True,(0, 0, 0))
        textSurfqwe  = self.font.render("("+str(int(self.player2.X))+" , "+str(int(self.player2.Y))+")" , True,(0, 0, 0))
        textSurf2 = self.font.render("walking : "+str(self.player1.walking) , True,(0, 0, 0))
        textSurf3 = self.font.render("jumping : "+str(self.player1.jumping) , True,(0, 0, 0))
        textSurf4 = self.font.render("falling : "+str(self.player1.falling) , True,(0, 0, 0))
        textSurf5 = self.font.render("inertiaCount: "+str(self.player1.inertiaCounter) , True,(0, 0, 0))
        textSurf6 = self.font.render("TIME: "+ str(int(self.totalElapsedTime)) , True,(0, 0, 0))
        textSurf7 = self.font.render("LIVES (P1): "+ str(self.player1.lives) , True,(0, 0, 0))
        textSurf8 = self.font.render("(P2): "+ str(self.player2.lives) , True,(0, 0, 0))
        textSurf9 = self.font.render("Score (P1): "+ str(int(self.player1.score)) , True,(0, 0, 0))
        textSurf10 = self.font.render("(P2): "+ str(int(self.player2.score)) , True,(0, 0, 0))
        screen.blit(textSurf,  (800, 70))
        screen.blit(textSurfqwe,  (800, 100))
        screen.blit(textSurf2, (800, 130))
        screen.blit(textSurf3, (800, 160))
        screen.blit(textSurf4, (800, 190))
        screen.blit(textSurf5, (800, 220))
        screen.blit(textSurf6, (800, 350))
        screen.blit(textSurf7, (800, 250))
        screen.blit(textSurf8,  (900, 250))
        screen.blit(textSurf9, (800, 300))
        screen.blit(textSurf10, (900, 300))
        
        textSurf11 = self.font.render("wallStickLag: "+ str(int(self.player1.wallStickLag)) , True,(0, 0, 0))
        screen.blit(textSurf11, (900, 400))



    # Intento de arreglar el algoritmo. Veamos como resulta
    def backgroundYMovementManager(self, player1, player2):
 
        # Obtiene los valores de posicion de primer y ultimo sprite del grupo
        firstRect = self.background.levelMaker.firstRect
        lastRect  = self.background.levelMaker.lastRect
        
        # relevante para scrolling horizontal y vertical

        leftStageX = firstRect.left
        rightStageX = lastRect.left
        topStageY = firstRect.top
        bottomStageY = lastRect.top
        halfH = self.screenSize[1]/2.0
        height = self.screenSize[1]

        levelHigherThanScreen = self.background.levelMaker.height * 50 > self.screenSize[1]
    
        _2playerUpperLimit = 0
        _2playerBottomLimit = height - 100
        _2PlayerInScreen = player2.Y >= _2playerUpperLimit and player2.Y <= _2playerBottomLimit
        # El 50 es para tomar en cuenta la altura del personaje
        _2PlayerInRealScreen = player2.Y >= -50 and player2.Y <= height
        _1PlayerInRealScreen = player1.Y >= -50 and player1.Y <= height
                
        deltaDownDeadZone = abs(firstRect.top) # Background moving down
        deltaUpDeadZone = lastRect.top - height # Background moving up

        # Caso en que etapa es demasiado pequena
        if not levelHigherThanScreen:
            player1.Y -= player1.deltaY
            
        # Si player esta centrado y player 2 se encuentra en pantalla ficticia
        # Camara seguira a player 1 hasta que player 2 salga de pantalla por delta de player 1
        # Revisar que se respeten las deadZones
        elif player1.Y == halfH and _2PlayerInScreen:
        
            # Caso en que el player2 esta dentro del area y no toca los bordes
            if (player2.Y + player1.deltaY > _2playerUpperLimit) and (player2.Y + player1.deltaY < _2playerBottomLimit):
                self.background.yAdvance = player1.deltaY
                if   player1.deltaY < 0:
                    self.background.moveBackGroundUp = True
                    self.background.yAdvance = -min(abs(player1.deltaY), deltaUpDeadZone)
                elif player1.deltaY > 0:
                    self.background.moveBackGroundDown = True
                    self.background.yAdvance = min(player1.deltaY, deltaDownDeadZone)

                player2.Y += self.background.yAdvance#---------------------------#
                player1.Y -= player1.deltaY - self.background.yAdvance

            # Si player dos se sale del limite inferior al aplicar movimiento de player 1
            # Player 1 esta subiendo
            elif player2.Y < _2playerBottomLimit and (player2.Y + player1.deltaY > _2playerBottomLimit):
                self.background.moveBackGroundDown = True
                deltaP1 = (player2.Y + player1.deltaY) - _2playerBottomLimit
                deltaBackground =  player1.deltaY - deltaP1
                deltaBackground = min(deltaBackground , deltaDownDeadZone)#######################################################33
                self.background.yAdvance = deltaBackground      
                player1.Y -= deltaP1
                player2.Y += self.background.yAdvance#---------------------------#  
            
            # Si player 2 se sale de limite superior al aplicar movimiento de player 1
            # Player 1 esta cayendo
            elif player2.Y > _2playerUpperLimit and (player2.Y + player1.deltaY < _2playerUpperLimit):
                self.background.moveBackGroundUp = True
                deltaBackground = - player2.Y 
                deltaBackground = -min(deltaBackground , deltaUpDeadZone)#######################################################33
                deltaP1 = (-1) * abs(player1.deltaY - deltaBackground)
                self.background.yAdvance = deltaBackground
                player1.Y -= deltaP1
                player2.Y += self.background.yAdvance#--------------------------#
            
        # Player esta centrado y player 2 no esta en pantalla
        # Camara sigue a player 1 de forma completa
        # Revisar que se respeten las deadZones OK
        elif player1.Y == halfH and not _2PlayerInRealScreen:
            self.background.yAdvance = player1.deltaY
            if   player1.deltaY < 0:
                self.background.moveBackGroundUp = True
                self.background.yAdvance = -min(abs(player1.deltaY), deltaUpDeadZone)
            elif player1.deltaY > 0:
                self.background.moveBackGroundDown = True
                self.background.yAdvance = min(player1.deltaY, deltaDownDeadZone)

            player1.Y -= player1.deltaY - self.background.yAdvance
            player2.Y += self.background.yAdvance
        
        # Si player esta centrado y player 2 esta en la pantalla real, pero no en la ficticia
        # En este caso se ajusta la camara para que player 2 quede en la pantalla ficticia
        # Revisar que se respeten las deadZones
        elif _2PlayerInRealScreen and _1PlayerInRealScreen and not _2PlayerInScreen and not player2.jumping and not player2.falling and not player2.wallJumping:
            
            """ ERROR DE QUE SE LLAMA A DELTAP1 ANTES DE ASIGNARLE UN VALOR """

            # Player 2 esta asomando por la parte superior de la pantalla. Background debe bajar para incluirlo
            # Player 1 debe moverse en la misma direccion que background. Cuidar que se respeten las deadzones
            if player2.Y <= 0 and player2.Y + 50 >= _2playerUpperLimit:
                deltaP1 = player2.Y
                self.background.moveBackGroundDown = True
                #deltaBackground = min(deltaP1, deltaDownDeadZone)#######################################################33
                #player1.Y -= deltaP1 - deltaBackground

            # Player 2 esta asomando por la parte inferior de la pantalla. Background debe subir para incluirlo
            # Player 1 debe moverse en la misma direccion que background. Cuidar que se respeten las deadzones
            elif player2.Y <= height and player2.Y >= _2playerBottomLimit: #_2playerBottomLimit:
                deltaP1 = player2.Y - _2playerBottomLimit
                self.background.moveBackGroundUp = True
                #deltaBackground = -min(deltaP1, deltaUpDeadZone)#######################################################33
                #player1.Y -= deltaP1 - deltaBackground
        
            #self.background.yAdvance  = deltaBackground
            self.background.yAdvance = -deltaP1
            player1.Y -= deltaP1
            player2.Y += self.background.yAdvance#------------------------------------------#

        # Si ningun player esta en pantalla, esta se centra automaticamente en player 1
        # es una prueba
        elif not _2PlayerInRealScreen and not _1PlayerInRealScreen :
            pass
        
        # Si player 1 no esta centrado : 
        # Si player 2 esta en pantalla, se centrara sujeto a que no quede fuera de pantalla ficticia
        # Si player 2 no esta en pantalla, solo se centrara
        # Revisar que se respeten las deadZones
        elif player1.Y != halfH:

            # Si player 2 esta en el area
            if player2.Y > _2playerUpperLimit and player2.Y < _2playerBottomLimit and (firstRect.top <= 0 and lastRect.top >= height):
                #player2.Y > _2playerUpperLimit and player2.Y < _2playerBottomLimit and 
                deltaP1 = player1.Y - halfH           
                    
                # Esta sobre la linea media. Escenario baja con player 1 para dejarlo centrado
                # No puede pasar que firstRect.top quede mayor que cero (al alejarse de origen)
                if player1.Y < halfH: #and _2PlayerInScreen:
                    deltaDeadZone = abs(firstRect.top)
                    #if player2.deltaY > 0:
                    deltaP1 = -min(abs(_2playerBottomLimit - player2.Y), abs(deltaP1), deltaDeadZone)
                    #elif player2.deltaY <= 0: #and player1.Y + player2.deltaY > 0:
                    #    deltaP1 = - player2.deltaY
                    self.background.moveBackGroundDown = True
                
                # Esta bajo la linea media. Escenario sube con player 1 para dejarlo centrado
                # No puede pasar que lastRect.bottom quede menor que height
                elif player1.Y > halfH: #and _2PlayerInScreen:
                    deltaDeadZone = lastRect.top - height
                    deltaP1 = min(abs(player2.Y), abs(deltaP1), deltaDeadZone)
                    self.background.moveBackGroundUp = True
                
                self.background.yAdvance = -deltaP1
                player2.Y += self.background.yAdvance#-----------------#
                player1.Y -= deltaP1
            
            ## Player 1 se encuentra bajo linea media 
            if player1.Y > halfH:
                # Si saltar lo deja arriba de linea media
                if player1.Y - player1.deltaY <= halfH:
                    deltaP1 = player1.Y - halfH
                    self.background.moveBackGroundDown = True
                    deltaBackground1 = abs(player1.deltaY) - deltaP1
                    deltaBackground2 = min(deltaBackground1, deltaDownDeadZone)#######################################################33
                    self.background.yAdvance = deltaBackground2
                    deltaP1 -= abs(deltaBackground2 - deltaBackground1)
                    player2.Y += self.background.yAdvance#-----------------#
                    player1.Y -= deltaP1
                # Si saltar lo sigue dejando abajo de la linea
                elif player1.Y - player1.deltaY > halfH:
                    player1.Y -= player1.deltaY

            ## Se encuentra sobre linea media
            elif player1.Y < halfH:
                # Si caer lo deja bajo la linea
                if player1.Y - player1.deltaY >= halfH:
                    deltaP1 = player1.Y - halfH
                    deltaBackground1 = abs(player1.deltaY) - abs(deltaP1)
                    deltaBackground2 = min(deltaBackground1, deltaUpDeadZone)#######################################################33
                    self.background.moveBackGroundUp = True
                    self.background.yAdvance = - deltaBackground2
                    deltaP1 -= abs(deltaBackground2 - deltaBackground1)
                    player2.Y += self.background.yAdvance#-----------------#
                    player1.Y -= deltaP1
                # Si caer lo sigue dejando sobre la linea
                elif player1.Y - player1.deltaY < halfH:
                    player1.Y -= player1.deltaY

            ## Se tiene que llegar a esto en caso de que todo el resto no se cumpla
            else:
                player1.Y -= player1.deltaY


    # Se encarga de movimiento horizontal para camara con dos jugadores
    def backgroundXMovementManager(self, player1, player2):

        levelWiderThanScreen = self.background.levelMaker.width * 50 > self.screenSize[0]

        # Obtiene los valores de posicion de primer y ultimo sprite del grupo
        firstRect = self.background.levelMaker.firstRect
        lastRect  = self.background.levelMaker.lastRect
        
        # relevante para scrolling horizontal y vertical
        leftStageX = firstRect.left
        rightStageX = lastRect.left
        halfW = self.screenSize[0]/2.0


        if not levelWiderThanScreen:
            player1.X += player1.deltaX

        elif  ((player1.X + player1.deltaX) - leftStageX <= halfW) and (player1.X - leftStageX > halfW) and player1.deltaX < 0:
            rightPart = player1.X - (halfW + leftStageX)
            leftPart = abs(player1.deltaX) - rightPart

            player1.X += player1.deltaX + rightPart
            self.background.moveBackGroundForward = True
            self.background.xAdvance = abs(rightPart)
        
        elif (player1.X - leftStageX <= halfW) and ((player1.X + player1.deltaX) - leftStageX > halfW) and player1.deltaX > 0 :
            leftPart = (leftStageX + halfW) - player1.X
            rightPart = player1.deltaX - leftPart
                
            player1.X += player1.deltaX - rightPart
            self.background.moveBackGroundBackward = True
            self.background.xAdvance = abs(rightPart) * (-1)
        
        elif (rightStageX - player1.X > halfW) and (rightStageX - (player1.X + player1.deltaX) <= halfW) and player1.deltaX > 0:
            leftPart = (rightStageX - halfW) - player1.X
            rightPart = player1.deltaX - leftPart

            player1.X += player1.deltaX  - leftPart
            self.background.moveBackGroundBackward = True
            self.background.xAdvance = abs(leftPart) * (-1)
        
        elif (rightStageX - player1.X <= halfW) and (rightStageX - (player1.X + player1.deltaX) > halfW) and player1.deltaX < 0:
            rightPart = player1.X - (rightStageX - halfW)
            leftPart = abs(player1.deltaX) - rightPart

            player1.X += player1.deltaX + leftPart
            self.background.moveBackGroundForward = True
            self.background.xAdvance = abs(leftPart)
        
        elif((player1.X - leftStageX) >= halfW) and ((rightStageX - player1.X) >= halfW):
            self.background.xAdvance = -int(player1.deltaX)
            if player1.deltaX > 0:
                self.background.moveBackGroundBackward = True
            elif player1.deltaX < 0:
                self.background.moveBackGroundForward = True
        else:
            player1.X += player1.deltaX


        player2.X += self.background.xAdvance#---------------------------#
        

