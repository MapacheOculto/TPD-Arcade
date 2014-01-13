# -*- coding: cp1252 -*-
import pygame
from pygame import *
from storyBoard2 import StoryBoard2
from projectileMotion import ProjectileMotion
from freefall import FreeFall
from boxCollision import boxCollision
from pygame import mixer
from platform import Platform
import math

# Relativo a los sonidos
mixer.init()
murunf = mixer.Sound('sounds//Murunf.mp3')
murunf.set_volume(0.5)
walk = mixer.Sound('sounds//walk2.wav')
walk.set_volume(0.1)
alert = mixer.Sound('sounds//jump.wav')
alert.set_volume(0.1)
slide=mixer.Sound('sounds//slide.wav')
slide.set_volume(0.8)
burn=mixer.Sound('sounds//burn1.wav')
burn.set_volume(1)


class Player:
    
    def __init__(self, joystick, movParab, freefall, storyboard, x = 200, y = 120):
        
        ### Estos son los paths para las imagenes de las animaciones 
        self.runPath = []
        self.path1 = []
        self.startJumpPath = []
        self.jumpPath = []
        self.endJump = []
        self.wallJumpRPath = []
        self.deathPath = []
       
        #ACCESORIOS
        self.movParab = movParab
        self.freefall = freefall
        self.storyBoard = storyboard
        self.clashManager = boxCollision()
        self.sprite = pygame.sprite.Sprite()
        self.joystick = joystick
        self.colisionada = None ##INTENTAR HACERLO CON UNA LISTA Y VERIFICAR TODOS LOS QUE ESTA COLISIONANDO

        #POSICION Y OTROS INT
        self.X = x
        self.Y = y
        self.deltaY = 0.0
        self.deltaX = 0.0
        self.direction = 0
        self.speed = 100
        self.lives = 10
        self.score = 0

        # BOOLS
        self.falling = False
        self.jumpStart = False
        self.jumping = False
        self.jumpEnd = False
        self.walking = False
        self.still = False
        self.goingRight = False
        self.goingLeft = False

        # WALL JUMP
        self.rightWallSliding = False
        self.leftWallSliding = False
        self.pressedAgainstWall = False
        self.wallJumping = False
        self.wallStickLag = 0
        
        # INERCIA
        self.inertiaActivated = False
        self.inertiaCounter = 0
        self.inertiaDirection = 0
        self.inertiaFrames = 40.0

        # Botones del joystick
        self.keyHeldPressed = False
        self.buttonPressed = False##
        self.buttonHeldPressed = False##
        self.joystickButtonActivated = False
        self.allowButtonPressing = True

        # STAGE Y MUERTE
        self.exitStage = False
        self.dead = False

        #COLOR
        self.color = "Green"
        self.companero = None

        #INICIALIZADORES
        self.initSpriteData()
        self.initImagesForAnimation()


    def initSpriteData(self):
        surface = pygame.display.get_surface()
        self.sprite.image = pygame.image.load("still//fire01.png").convert_alpha()

        width = int(self.sprite.image.get_width())
        height = int(self.sprite.image.get_height())
        
        self.sprite.image = pygame.transform.scale(self.sprite.image, (width,height)) 
        self.sprite.rect = pygame.Rect((self.X, self.Y), (width,height))              


    def updateSpriteSize(self, prevWidth, prevHeight):
        self.sprite.image = pygame.transform.scale(self.sprite.image, (50,50)) 
        self.sprite.rect = pygame.Rect((self.X, self.Y), (50, 50))              


    # Metodo ve si esta cayendo, caminando, saltando, etc. Luego, actualiza bools y valores correspondientes
    def update(self, elapsedTime, group, exitGroup, damageGroup, itemsGroup, groupList):
        
        ##IVAN
            ##Plataformas no activadas (agregarlas a una lista de plataformas tocadas pa ver si siguen estando activadas o no
        
        #for sprite in group:
        #    if sprite.activada == True:
        #        #Verificar que sigue activada

        #        #Si lo esta
        #        if (pygame.sprite.collide_rect(self.sprite,sprite) and sprite.color == self.color): #o hay colision con el otro personaje
        #            sprite.color = "Todos"
        #        #Si no
        #        else:
        #            sprite.color = sprite.colororiginal
        #            sprite.activada = False

        #    else: sprite.activada = False
        ##Colision de compañero
        #newPos = pygame.Rect(self.companero.X+self.companero.deltaX, self.companero.Y+self.companero.deltaY, self.companero.sprite.rect.width, self.companero.sprite.rect.height)
        #playerMoved = pygame.sprite.Sprite()
        #playerMoved.rect = newPos



        clashingDown = self.clashManager.CheckCollision(self, group, self.X, self.Y + 1)
        clashingRight = self.clashManager.CheckCollision(self, group, self.X + 1, self.Y)
        clashingLeft = self.clashManager.CheckCollision(self, group, self.X - 1, self.Y) 
        self.deltaX = 0
        self.deltaY = 0
        temporalDirection = 0

        
        ## CAMBIO DE COLOR 
        if self.joystick.get_button(4):
           self.color = "Green"
        if self.joystick.get_button(5):
           self.color = "Blue"
        pressedKey = pygame.key.get_pressed()
        if pressedKey[K_v]:
           self.color = "Green"
        if pressedKey[K_b]:
           self.color = "Blue"
        

        ## JOYSTICK
        if not self.joystick.get_button(0) and self.joystickButtonActivated:
            self.joystickButtonActivated = False
            self.allowButtonPressing = True
        if self.joystick.get_button(0) and self.joystickButtonActivated and not self.allowButtonPressing:
            self.buttonPressed = False
        if self.joystick.get_button(0) and not self.buttonPressed and self.allowButtonPressing:
            self.allowButtonPressing = False
            self.buttonPressed = True
            self.joystickButtonActivated = True


        ## CAIDA LIBRE
        if not clashingDown: 
            if not self.jumping and not self.wallJumping and not (self.rightWallSliding or self.leftWallSliding):
                self.falling = True
        elif clashingDown:
            self.falling = False
            
        if self.falling:
            self.fall(group, self.freefall, elapsedTime)
        else:
            self.freefall.stop()
            
            
        ## ITEMS
        if self.clashManager.CheckCollision(self, itemsGroup, self.X, self.Y):
            itemList = pygame.sprite.spritecollide(self.sprite, itemsGroup, False)
            for item in itemList:
                if item.id == "life":
                    self.lives += 1
                elif item.id == "points":
                    self.score += 100
                item.kill()
            

        ## MUERTE
        if self.clashManager.CheckCollision(self, damageGroup, self.X, self.Y):
            self.falling = False
            self.freefall.stop()
            self.startJump()
            self.takeDamage()
            burn.play()


        ## CAMBIO ETAPA
        if self.clashManager.CheckCollision(self, exitGroup, self.X, self.Y):
            self.exitStage = True


        ## CAMINATA (ahora con joystick)
        if abs(self.joystick.get_axis(0)) > 0.3:##
            temporalDirection = self.joystick.get_axis(0)##

        self.deltaX = int( 4 * temporalDirection * elapsedTime * self.speed)
        if abs(self.deltaX) > 0:
            self.walk(group, self.deltaX)
            self.walking = True
            self.still = False
        else:
            self.walking = False
            self.still = True


        ## DEFINE SI ESTA PEGADO A LA PARED
        if (clashingRight or clashingLeft) and ((self.falling or self.jumping)) and not clashingDown:
            if clashingRight:
                self.rightWallSliding = True
            elif clashingLeft:
                self.leftWallSliding = True  

            if (temporalDirection > 0 and clashingRight)or (temporalDirection < 0 and clashingLeft):
                self.wallStickLag = 5
                self.pressedAgainstWall = True
                self.jumping = False
                self.freefall.stop()
                self.deltaY = -2 ########################
                if self.clashManager.CheckCollision(self, group, self.X, self.Y + 2):
                    floorY = self.clashManager.topY - (self.sprite.rect.height)
                    self.deltaY = self.Y - floorY
            else:
                self.pressedAgainstWall = False
        else:
            self.rightWallSliding = False
            self.leftWallSliding = False
            self.pressedAgainstWall = False


        ## SALTO DESDE PARED (ahora con joystick)
        if self.rightWallSliding or self.leftWallSliding:##
            if self.buttonPressed:##
                self.buttonPressed = False
                self.freefall.stop()##
                self.wallJumpStart(self.rightWallSliding)##
        if self.wallJumping:
            self.updateWallJump(group, elapsedTime)
            

        ## SALTO NORMAL (ahora con joystick)
        if self.buttonPressed and not self.falling and not self.wallJumping and not self.jumping:##
            self.jumpStart = True##
            self.startJump()##
            self.buttonPressed = False
            
        if self.jumping and not self.pressedAgainstWall:
            self.updateJump(group, elapsedTime)

        
        ## INERCIA
        if self.direction == 0:
            if temporalDirection > 0 or temporalDirection < 0:
                self.inertiaCounting = True
        if (temporalDirection != 0) and (self.direction / temporalDirection < 0):
            self.inertiaCounting = False
        if (temporalDirection != 0) and (self.direction / temporalDirection > 0):
            self.inertiaCounting = True
        if temporalDirection == 0 and self.direction == 0:
            self.inertiaCounting = False
        if self.inertiaCounter == 0 and self.direction != 0 and temporalDirection != 0:
            self.inertiaCounting = True

        if self.inertiaCounting and not self.inertiaActivated and not self.pressedAgainstWall:
            if self.inertiaCounter < self.inertiaFrames:
                self.inertiaCounter += 4
        elif self.rightWallSliding or self.leftWallSliding:
            self.inertiaCounter = 0
            self.inertiaActivated = False


        ## CAMBIO DIRECCION
        if temporalDirection > 0:
            if self.goingLeft:
                self.goingLeft = False
                self.inertiaActivated = True
            self.goingRight = True
        elif temporalDirection < 0:
            if self.goingRight:
                self.goingRight = False
                self.inertiaActivated = True
            self.goingLeft = True
        elif temporalDirection == 0 and self.direction != 0:
            self.inertiaActivated = True
            self.inertiaDirection = self.direction


        # INERCIA DE NUEVO
        if self.inertiaActivated and self.inertiaCounter >= 0:
            self.calculateInertia(group, self.direction, clashingDown, elapsedTime)
        

        # SETEO DE BOOLS
        if self.wallJumping:
            self.walking = False
            self.still = False
     
        
        # Al terminar de hacer update, deja listo el rectangulo con los nuevos valores
        self.direction = temporalDirection
        if self.id == "p2":
            self.Y -= self.deltaY
            self.X += self.deltaX
        self.sprite.rect = pygame.Rect((self.X, self.Y), (self.sprite.rect.width, self.sprite.rect.height))


           ## COLOR
        surface = pygame.display.get_surface()
        if self.color == "Blue":
            pygame.draw.circle(surface, (0,0,255), (int(self.X), int(self.Y) -5), 6)
        elif self.color == "Green":
            pygame.draw.circle(surface, (0,255,0), (int(self.X), int(self.Y) -5), 6)

        #BORRAR-----------------------------------------------------------------------------------------------------------BORRAR
        self.score += 0.5
            
                
    # De acuerdo a los bools determinados en update, dibuja la animacion correspondiente
    def render(self):
        
        tempWidth = self.sprite.image.get_width()
        tempHeight = self.sprite.image.get_height()

        if self.walking:
            if self.rightWallSliding:
                self.animation(self.wallJumpRPath, len(self.wallJumpRPath))
            elif self.leftWallSliding:
                self.animation(self.wallJumpRPath, len(self.wallJumpRPath))
            elif self.jumpStart:
                self.animation(self.startJumpPath, len(self.startJumpPath))
                if self.storyBoard.inProcess == False:
                    self.jumpStart = False
            elif self.jumping:
                self.animation(self.jumpPath, len(self.jumpPath))
            elif (self.jumpEnd):
                self.animation(self.endJump, len(self.endJump))
                if self.storyBoard.inProcess == False:
                    self.jumpEnd = False
            elif self.falling:
                self.animation(self.jumpPath, len(self.jumpPath))
            elif not self.jumping: 
                self.animation(self.runPath, len(self.runPath))

        elif self.still:
            
            if self.rightWallSliding:
                self.animation(self.wallJumpRPath, len(self.wallJumpRPath))
            elif self.leftWallSliding:
                self.animation(self.wallJumpRPath, len(self.wallJumpRPath))
            elif self.jumpStart:
                self.animation(self.startJumpPath, len(self.startJumpPath))
                if self.storyBoard.inProcess == False:
                    self.jumpStart = False
            elif self.jumping:
                self.animation(self.jumpPath, len(self.jumpPath))
            elif (self.jumpEnd):
                self.animation(self.endJump, len(self.endJump))
                if self.storyBoard.inProcess == False:
                    self.jumpEnd = False      
            elif self.falling:
                self.animation(self.jumpPath, len(self.jumpPath))
            else:  #Se queda quieto
                self.animation(self.path1, len(self.path1))


        self.updateSpriteSize(tempWidth, tempHeight)
        surface = pygame.display.get_surface()
        surface.blit(self.sprite.image, self.sprite.rect)

        ## COLOR RENDER
        surface = pygame.display.get_surface()
        if self.color == "Blue":
            pygame.draw.circle(surface, (0,0,255), (int(self.X), int(self.Y) -5), 6)
        elif self.color == "Green":
            pygame.draw.circle(surface, (0,255,0), (int(self.X), int(self.Y) -5), 6)
        
        
    #---------------------------------------------------------------------------------------------
    #-DAÑO-O-GANAR-PUNTAJE-----------------------------------------------------------
    def takeDamage(self):
        self.lives -= 1
        if self.score > 10:
            self.score -= 10
        if self.lives == 0:
            self.dead = True

    def gainScore(self, value):
        self.score += value
    
    #-CAMINATA ----------------------------------------------------------------------
    def walk(self, group, xAdvance):

        clashed = self.clashManager.CheckCollision(self, group, self.X + xAdvance, self.Y)
              
        if not clashed:
            self.deltaX = xAdvance
        elif clashed:
            if xAdvance > 0:
                floorX = self.clashManager.leftX - (self.sprite.rect.width)
            elif xAdvance < 0:
                floorX = self.clashManager.rightX 
            self.deltaX = floorX - self.X
            
            self.walking = False
            self.still = True

    #-INERCIA------------------------------------------------------------------------
    def calculateInertia(self, group, direction, clashingDown, elapsedTime):
        
        StopInertiaScale = self.inertiaCounter / self.inertiaFrames
        changeDirInertiaScale = (self.inertiaFrames - self.inertiaCounter) / self.inertiaFrames

        if self.deltaX != 0 and self.direction != 0:
            self.walk(group, changeDirInertiaScale * self.deltaX)
            self.inertiaCounter -= 1 ## SIRVEN PARA DIFERENCIAR LAS INERCIAS
        elif self.deltaX == 0:
            previousSpeed = int( 4 * elapsedTime * self.speed)
            self.walk(group, previousSpeed * StopInertiaScale * self.inertiaDirection)
            if clashingDown:
                self.inertiaCounter -= 3 ## SIRVEN PARA DIFERENCIAR LAS INERCIAS
            
        self.inertiaCounter -= 1
        if self.inertiaCounter <= 0:
            self.inertiaCounter = 0
            self.inertiaActivated = False

    #-SALTO -------------------------------------------------------------------------
    def startJump(self):
        self.movParab.start(self.Y)
        self.jumping = True
        self.totalJumpTime = 0

    def updateJump(self, group, elapsedTime):

        self.totalJumpTime += elapsedTime
        self.movParab.update(self.totalJumpTime)
        self.deltaY = int(self.movParab.deltaY)
        if self.deltaY <= -50:############################################################################################
            self.deltaY = -50############################################################################################

        clashed = self.clashManager.CheckCollision(self, group, self.X, self.Y - self.deltaY)

        # Primera opcion : Que no haya colision y el salto aun no termine (setea vel terminal)
        if not clashed and self.movParab.inProcess:
            if self.deltaY <= -50:############################################################################################
                self.deltaY = -50 ############################################################################################
        else:
            if clashed:
                # Chequea si el choque fue contra algun techo.
                if self.deltaY > 0:
                    roofY = self.clashManager.bottomY
                    self.deltaY = int(self.Y - roofY)
                        
                # Chequea si el choque fue contra algun piso.
                elif (not self.checkIfFalling(self.X, self.Y - self.deltaY, group)) and (self.deltaY < 0): 
                    floorY = self.clashManager.topY - (self.sprite.rect.height)
                    self.deltaY = int(self.Y - floorY)
                    self.jumpEnd = True

            self.movParab.stop()
            self.jumping = False
            self.still = True
            self.totalJumpTime = 0

    
    #-SALTO-DE-PARED----------------------------------------------------------------
    def wallJumpStart(self, jumpingFromRightWall):
        self.movParab.start(self.Y)
        self.totalJumpTime = 0
        self.wallJumping = True
        self.jumping = False
        
        # Variable ql q no se como llamar. Sirve pa q no se contradigan los dos movimientos de deltaX
        self.playerTakenHorizontalControl = False
        self.contador = 4
        
        self.wallJumpDirection = 0
        if jumpingFromRightWall:
            self.wallJumpDirection = -1
        else:
            self.wallJumpDirection = 1

    def updateWallJump(self, group, elapsedTime):

        self.totalJumpTime += elapsedTime
        self.movParab.update(self.totalJumpTime)
        self.deltaY = int(self.movParab.deltaY)
        
        if self.deltaX != 0 and self.contador <= 0:
            self.playerTakenHorizontalControl = True
        if not self.playerTakenHorizontalControl and (self.contador >= 0 or self.deltaY > 0):
            previousSpeed = int( 6 * elapsedTime * self.speed)
            self.walk(group, previousSpeed * self.wallJumpDirection)
            self.contador -= 1

        # Parche para evitar que delta X tome valor cero por tres iteraciones en que
        # deltaY es normalizado al valor cero por la funcion int. (y por lo tanto, se
        # evita el corte visual feo.
        if self.deltaX == 0 and self.deltaY == 0:
            self.deltaY = -1 #################################################################################################################
        
        clashed = self.clashManager.CheckCollision(self, group, self.X, self.Y - self.deltaY)

        # Primera opcion : Que no haya colision y el salto aun no termine (setea vel terminal)
        if not clashed and self.movParab.inProcess:
            if self.deltaY < 0:
                if not self.playerTakenHorizontalControl:
                    self.inertiaActivated = True ###########################
                    self.inertiaCounter = 40 ###########################
                    self.inertiaDirection = self.wallJumpDirection ###########################
                self.movParab.stop()
                self.freefall.stop()
                self.wallJumping = False
        else:
            if clashed:
                # Chequea si el choque fue contra algun techo.
                if self.deltaY > 0:
                    roofY = self.clashManager.bottomY
                    self.deltaY = int(self.Y - roofY)
                    self.freefall.stop()
                
            self.movParab.stop()
            self.wallJumping = False
            self.totalJumpTime = 0

    #-CAIDA LIBRE ---------------------------------------------------------------------------------------------
    def fall(self, group, freefall, elapsedTime):
        
        if not self.freefall.inProcess:
            self.freefall.start(self.Y)
            self.totalJumpTime = 0
        
        self.totalJumpTime += elapsedTime
        self.freefall.update(self.totalJumpTime) 
        self.deltaY = int(self.freefall.deltaY) 
        if abs(self.deltaY) >= 50:#######################################################################################
            self.deltaY = -50###########################################################################

        ## Ver si al actualizar con freefall.Y se produce o no choque
        if self.clashManager.CheckCollision(self, group, self.X, self.Y - self.deltaY):

            ## valor de Y que toma al impactar el suelo
            floorY = self.clashManager.topY - (self.sprite.rect.height)
            self.deltaY = int(self.Y - floorY)

            ## Resetear valores asociados a la caida
            self.freefall.stop()
            falling = False
            self.jumpEnd = True
            self.totalJumpTime = 0
        else:
            if abs(self.deltaY) >= 50:#######################################################################################
                self.deltaY = -50#######################################################################################


    #Chequea si esta en caida libre o no
    def checkIfFalling(self, X2, Y2, group):
        if (not self.clashManager.CheckCollision(self, group, X2, Y2)) and Y2 >= self.Y :
            return True
        else:
            return False


    def checkIfClashing(self, X2, Y2, groupList):
        for group in groupList:
            if self.clashManager.CheckCollision(self, group, X2, Y2) :
                return True
            else:
                return False

            
    # Ahora keys son las imagenes que se pasan a storyboard
    def animation(self, keys, number):
        # Corta la animacion antigua en pos de la nueva
        if number != self.storyBoard.frameNumber:
            self.storyBoard.inProcess = False
        if self.storyBoard.inProcess == False:
            self.storyBoard.play(number, keys)
        elif self.storyBoard.inProcess:
            self.storyBoard.update(self.sprite, self.goingLeft)


    # Carga las imagenes y las convierte para no tener que volver a hacerlo despues
    def initImagesForAnimation(self):

        self.runPath.append(pygame.image.load("walk//fire1.png").convert_alpha())
        self.runPath.append(pygame.image.load("walk//fire2.png").convert_alpha())
        self.runPath.append(pygame.image.load("walk//fire3.png").convert_alpha())
        self.runPath.append(pygame.image.load("walk//fire4.png").convert_alpha())
        self.runPath.append(pygame.image.load("walk//fire5.png").convert_alpha())
        self.runPath.append(pygame.image.load("walk//fire6.png").convert_alpha())
        
        self.path1.append(pygame.image.load("still//fire01.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire02.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire03.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire04.png").convert_alpha())
        
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart1.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart2.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart3.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart4.png").convert_alpha())
        
        self.jumpPath.append(pygame.image.load("jump//jumping1.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping2.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping3.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping4.png").convert_alpha())
        
        self.endJump.append(pygame.image.load("jumpEnd//finishJump1.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump2.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump3.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump4.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump5.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump6.png").convert_alpha())

        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump1.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump2.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump3.png").convert_alpha())

        self.deathPath.append(pygame.image.load("muerte//jumping1.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping2.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping3.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping4.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping5.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping6.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping7.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping8.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping9.png").convert_alpha())
        self.deathPath.append(pygame.image.load("muerte//jumping10.png").convert_alpha())
