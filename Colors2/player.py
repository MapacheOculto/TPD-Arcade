# -*- coding: cp1252 -*-
import pygame
from pygame import *
from storyBoard2 import StoryBoard2
from projectileMotion import ProjectileMotion
from freefall import FreeFall
from boxCollision import boxCollision
from pygame import mixer
#from platform import Platform
import math


class Player:
    
    def __init__(self, joystick, movParab, freefall, storyboard, container, x = 200, y = 120):

        # Paths para sonido
        self.points = container.soundDictionary["point"]
        self.points.set_volume(0.4)
        self.life = container.soundDictionary["life"]
        self.life.set_volume(0.4)
        self.burn = container.soundDictionary["burn"]
        self.burn.set_volume(1)
        self.walk1 = container.soundDictionary["walk"]
        self.walk1.set_volume(0.1)
        self.jump = container.soundDictionary["jump"]
        self.jump.set_volume(0.1)
        self.slide = container.soundDictionary["slide1"]
        self.slide.set_volume(0.1)
        
        ### Estos son los paths para las imagenes de las animaciones 
        self.runPath = container.runPath
        self.path1 = container.path1
        self.startJumpPath = container.startJumpPath
        self.jumpPath = container.jumpPath 
        self.endJump = container.endJump
        self.wallJumpRPath = container.wallJumpRPath
        self.runPath2 = container.runPath2
        self.path12 = container.path12
        self.startJumpPath2 = container.startJumpPath2
        self.jumpPath2 = container.jumpPath2
        self.endJump2 = container.endJump2 
        self.wallJumpRPath2 = container.wallJumpRPath2
        self.deadPath = container.deadPath
        self.deadPath2 = container.deadPath2
       
        #ACCESORIOS
        self.movParab = movParab
        self.freefall = freefall
        self.storyBoard = storyboard
        self.clashManager = boxCollision()
        self.sprite = pygame.sprite.Sprite()
        self.joystick = joystick
        self.colisionada = None ##INTENTAR HACERLO CON UNA LISTA Y VERIFICAR TODOS LOS QUE ESTA COLISIONANDO
        self.font = pygame.font.SysFont("arial", 16)
        self.font.set_bold(True)


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
        self.joystickButtonActivated = False
        self.allowButtonPressing = True

        # STAGE Y MUERTE
        self.exitStage = False
        self.startDeadAnimation = False
        self.dead = False
        self.deadMessage = ""

        #COLOR
        self.color = "Green"
        self.companero = None

        #INICIALIZADORES
        self.initSpriteData()


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

        


    def update(self, elapsedTime, group, exitGroup, damageGroup, itemsGroup, zGroup, groupList):

        self.colisionada = None

        clashingDown = self.clashManager.CheckCollision(self, group, self.X, self.Y + 1)
        clashingRight = self.clashManager.CheckCollision(self, group, self.X + 1, self.Y)
        clashingLeft = self.clashManager.CheckCollision(self, group, self.X - 1, self.Y) 
        self.deltaX = 0
        self.deltaY = 0
        temporalDirection = 0

        
        ## CAMBIO DE COLOR 
        if self.id == 'p1':
           self.color = "Green"
        elif self.id == 'p2':
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
                if self.lives == 10 and item.id == "life":
                    self.score += 100
                    self.points.play()
                elif self.lives < 10 and item.id == "life":
                    self.lives += 1
                    self.life.play()
                elif item.id == "points":
                    self.score += 50
                    self.points.play()
                item.kill()
            

        ## LAVA O HIELO
        if self.clashManager.CheckCollision(self, damageGroup, self.X, self.Y):
            self.falling = False
            self.freefall.stop()
            floorY = self.clashManager.topY - (self.sprite.rect.height)
            self.deltaY = self.Y - floorY
            self.startJump()
            self.takeDamage("da�o de lava o hielo")
            self.burn.play()


        ## CAMBIO ETAPA
        if self.clashManager.CheckCollision(self, exitGroup, self.X, self.Y):
            self.exitStage = True


        ## CAMINATA (ahora con joystick)
        if abs(self.joystick.get_axis(0)) > 0.3:##
            temporalDirection = self.joystick.get_axis(0)##

        self.deltaX = int( 4 * temporalDirection * elapsedTime * self.speed)
        if abs(self.deltaX) > 30:
            self.deltaX = 20 * temporalDirection
        if abs(self.deltaX) > 0:
            self.walk(group, zGroup, self.deltaX)
            self.walking = True
            self.still = False
        else:
            self.walking = False
            self.still = True

        ##CAMBIAR ACA PARA EVITAR GLITCH DE PLATAFORMAS VERTICALES
        ## DEFINE SI ESTA PEGADO A LA PARED

        if (clashingRight or clashingLeft) and ((self.falling or self.jumping)) and (not clashingDown or self.colisionada.id == "Vertical"): #or self.colisionada.id == "Vertical" or self.colisionada.color != self.companero.color:
            if clashingRight : #or (temporalDirection > 0 and self.colisionada.id == "Vertical") :
                self.rightWallSliding = True
            elif clashingLeft :
                self.leftWallSliding = True  
                ##COMO INFO
#(self.colisionada.id != "Horizontal" or self.colisionada.color != self.companero.color)
            if ((temporalDirection > 0 and clashingRight)or (temporalDirection < 0 and clashingLeft)) and self.falling and not self.jumping:

    
                self.wallStickLag = 5
                self.pressedAgainstWall = True
                self.freefall.stop()
                self.deltaY = -2 ########################
                if self.clashManager.CheckCollision(self, group, self.X, self.Y + 2):
                    floorY = self.clashManager.topY - (self.sprite.rect.height)
                    if (self.colisionada.id == "Vertical"):# or self.colisionada.color != self.companero.color):
                        floorY = self.Y
                    self.deltaY = self.Y - floorY
            else:
                self.pressedAgainstWall = False
        else:
            self.rightWallSliding = False
            self.leftWallSliding = False
            self.pressedAgainstWall = False


        ## SALTO DESDE PARED (ahora con joystick)
        if self.rightWallSliding or self.leftWallSliding:
            if self.buttonPressed:
                self.buttonPressed = False
                self.freefall.stop()
                self.wallJumpStart(self.rightWallSliding)
        if self.wallJumping:
            self.updateWallJump(group, zGroup, elapsedTime)
            

        ## SALTO NORMAL (ahora con joystick)
        if self.buttonPressed and not self.falling and not self.wallJumping and clashingDown:# and not self.jumping :##
            self.jumpStart = True
            self.startJump()
            self.buttonPressed = False
            self.jump.play()
        if self.jumping and not self.pressedAgainstWall:
            self.updateJump(group, zGroup, elapsedTime)

        
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
            self.calculateInertia(group, zGroup, self.direction, clashingDown, elapsedTime)
        
        """
        # SETEO DE BOOLS
        if self.wallJumping:
            self.walking = False
            self.still = False
        """
        
        # Al terminar de hacer update, deja listo el rectangulo con los nuevos valores
        if self.colisionada != None:
            if pygame.sprite.collide_rect(self.sprite,self.colisionada):
               if self.colisionada.id == "Horizontal":
                 self.Y = self.colisionada.rect.bottom
                 self.deltaY = 0
            else:
                    if self.colisionada.contador_movimiento_y != 0 and self.colisionada.contador_movimiento_y != self.colisionada.lim_y:
                        self.deltaY -= self.colisionada.delta_y
                    else:
                        self.deltaY += self.colisionada.delta_y

                    if self.colisionada.contador_movimiento_x != 0 and  self.colisionada.contador_movimiento_x != self.colisionada.lim_x:
                        self.deltaX += self.colisionada.delta_x
                    else:
                        self.deltaX -= self.colisionada.delta_x
        self.direction = temporalDirection
        if self.id == "p2":
            self.Y -= self.deltaY
            self.X += self.deltaX
        self.sprite.rect = pygame.Rect((self.X, self.Y), (self.sprite.rect.width, self.sprite.rect.height))

        #if self.colisionada != None:
        #    if pygame.sprite.collide_rect(self.sprite,self.colisionada):
        #       if self.colisionada.id == "Horizontal":
        #         self.Y = self.colisionada.rect.bottom
        #    else:
        #        self.deltaY -= self.colisionada.delta_y
        #        self.deltaX += self.colisionada.delta_x
            

           ## COLOR
        surface = pygame.display.get_surface()
        if self.color == "Blue":
            pygame.draw.circle(surface, (0,0,255), (int(self.X), int(self.Y) -5), 6)
        elif self.color == "Green":
            pygame.draw.circle(surface, (0,255,0), (int(self.X), int(self.Y) -5), 6)

            
                
    # De acuerdo a los bools determinados en update, dibuja la animacion correspondiente
    def render(self):
        
        tempWidth = self.sprite.image.get_width()
        tempHeight = self.sprite.image.get_height()
        actualPath = []


        if self.startDeadAnimation:
            if self.id == "p1":
                actualPath = self.deadPath2
            else:
                actualPath = self.deadPath
            if self.storyBoard.inProcess == False:
                self.dead = True
        elif self.walking:
            if self.rightWallSliding or self.leftWallSliding:
                if self.id == "p1":
                    actualPath = self.wallJumpRPath2
                else:
                    actualPath = self.wallJumpRPath
                self.animation(actualPath, len(actualPath))
            elif self.jumpStart:
                if self.id == "p1":
                    actualPath = self.startJumpPath2
                else:
                    actualPath = self.startJumpPath
                if self.storyBoard.inProcess == False:
                    self.jumpStart = False
            elif self.jumping:
                if self.id == "p1":
                    actualPath = self.jumpPath2
                else:
                    actualPath = self.jumpPath
            elif (self.jumpEnd):
                if self.id == "p1":
                    actualPath = self.endJump2
                else:
                    actualPath = self.endJump
                if self.storyBoard.inProcess == False:
                    self.jumpEnd = False
            elif self.falling:
                if self.id == "p1":
                    actualPath = self.jumpPath2
                else:
                    actualPath = self.jumpPath
            else: 
                if self.id == "p1":
                    actualPath = self.runPath2
                else:
                    actualPath = self.runPath
        else:
            if self.rightWallSliding or self.leftWallSliding:
                if self.id == "p1":
                    actualPath = self.wallJumpRPath2
                else:
                    actualPath = self.wallJumpRPath
                self.animation(actualPath, len(actualPath))
            elif self.jumpStart:
                if self.id == "p1":
                    actualPath = self.startJumpPath2
                else:
                    actualPath = self.startJumpPath
                if self.storyBoard.inProcess == False:
                    self.jumpStart = False
            elif self.jumping:
                if self.id == "p1":
                    actualPath = self.jumpPath2
                else:
                    actualPath = self.jumpPath
            elif (self.jumpEnd):
                if self.id == "p1":
                    actualPath = self.endJump2
                else:
                    actualPath = self.endJump
                if self.storyBoard.inProcess == False:
                    self.jumpEnd = False
            elif self.falling:
                if self.id == "p1":
                    actualPath = self.jumpPath2
                else:
                    actualPath = self.jumpPath
            else:
                if self.id == "p1":
                    actualPath = self.path12
                else:
                    actualPath = self.path1
        
        self.animation(actualPath, len(actualPath))

        self.updateSpriteSize(tempWidth, tempHeight)
        surface = pygame.display.get_surface()
        surface.blit(self.sprite.image, self.sprite.rect)

        textSurf = self.font.render(self.id , True,(0, 0, 0))
        surface.blit(textSurf,  (int(self.X), int(self.Y) - 25))
        
        
    #---------------------------------------------------------------------------------------------
    #-DA�O-O-GANAR-PUNTAJE-----------------------------------------------------------
    def takeDamage(self, string):
        self.lives -= 1
        if self.score > 10:
            self.score -= 10
        if self.lives == 0:
            self.startDeadAnimation = True
            if self.id == "p1":
                self.deadMessage = "Player 1 murio debido a " + string 
            elif self.id == "p2":
                self.deadMessage = "Player 2 murio debido a " + string 

    def gainScore(self, value):
        self.score += value
    
    #-CAMINATA ----------------------------------------------------------------------
    def walk(self, group, zGroup, xAdvance):

        clashed = self.clashManager.CheckCollision(self, group, self.X + xAdvance, self.Y)
        clashed2 = self.clashManager.CheckCollision(self, zGroup, self.X + xAdvance, self.Y)
              
        if not clashed and not clashed2:
            self.deltaX = xAdvance

        #Cambio pa arreglar bug
  
        elif (clashed and (self.colisionada.id != "Horizontal" or self.colisionada.color != self.companero.color)) or clashed2 :
            floorX = 2*self.X
            if xAdvance > 0:
                floorX = self.clashManager.leftX - (self.sprite.rect.width)
            elif xAdvance < 0:
                floorX = self.clashManager.rightX 
            self.deltaX = floorX - self.X
            
            self.walking = False
            self.still = True

    #-INERCIA------------------------------------------------------------------------
    def calculateInertia(self, group, zGroup, direction, clashingDown, elapsedTime):
        
        StopInertiaScale = self.inertiaCounter / self.inertiaFrames
        changeDirInertiaScale = (self.inertiaFrames - self.inertiaCounter) / self.inertiaFrames

        if self.deltaX != 0 and self.direction != 0:
            self.walk(group, zGroup, changeDirInertiaScale * self.deltaX)
            self.inertiaCounter -= 1 ## SIRVEN PARA DIFERENCIAR LAS INERCIAS
        elif self.deltaX == 0:
            previousSpeed = int( 4 * elapsedTime * self.speed)
            self.walk(group, zGroup, previousSpeed * StopInertiaScale * self.inertiaDirection)
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

    def updateJump(self, group, zGroup, elapsedTime):

        self.totalJumpTime += elapsedTime
        self.movParab.update(self.totalJumpTime)
        self.deltaY = int(self.movParab.deltaY)
        if self.deltaY <= -40:############################################################################################
            self.deltaY = -40############################################################################################

        clashed  = self.clashManager.CheckCollision(self, group, self.X, self.Y - self.deltaY)
        clashed2 = self.clashManager.CheckCollision(self, zGroup, self.X, self.Y - self.deltaY)

        # Primera opcion : Que no haya colision y el salto aun no termine (setea vel terminal)
        if not clashed and not clashed2 and self.movParab.inProcess:
            if self.deltaY < 0:
                self.movParab.stop()
                self.jumping = False
                self.still = True
                self.totalJumpTime = 0
        else:
            if clashed or clashed2:
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

    def updateWallJump(self, group, zGroup, elapsedTime):

        self.totalJumpTime += elapsedTime
        self.movParab.update(self.totalJumpTime)
        self.deltaY = int(self.movParab.deltaY)
        
        if self.deltaX != 0 and self.contador <= 0:
            self.playerTakenHorizontalControl = True
        if not self.playerTakenHorizontalControl and (self.contador >= 0 or self.deltaY > 0):
            previousSpeed = int( 6 * elapsedTime * self.speed)
            self.walk(group, zGroup, previousSpeed * self.wallJumpDirection)
            self.contador -= 1

        # Parche para evitar que delta X tome valor cero por tres iteraciones en que
        # deltaY es normalizado al valor cero por la funcion int. (y por lo tanto, se
        # evita el corte visual feo.
        if self.deltaX == 0 and self.deltaY == 0:
            self.deltaY = -1 #################################################################################################################
        
        clashed = self.clashManager.CheckCollision(self, group, self.X, self.Y - self.deltaY)
        clashed2 = self.clashManager.CheckCollision(self, zGroup, self.X, self.Y - self.deltaY)

        # Primera opcion : Que no haya colision y el salto aun no termine (setea vel terminal)
        if not clashed and not clashed2 and self.movParab.inProcess:
            if self.deltaY < 0:
                if not self.playerTakenHorizontalControl:
                    self.inertiaActivated = True ###########################
                    self.inertiaCounter = 40 ###########################
                    self.inertiaDirection = self.wallJumpDirection ###########################
                self.movParab.stop()
                self.freefall.stop()
                self.wallJumping = False
        else:
            if clashed or clashed2:
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
        if abs(self.deltaY) >= 40:#######################################################################################
            self.deltaY = -40###########################################################################

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
            if abs(self.deltaY) >= 40:#######################################################################################
                self.deltaY = -40#######################################################################################


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
        
        self.runPath2.append(pygame.image.load("walk//fire12.png").convert_alpha())
        self.runPath2.append(pygame.image.load("walk//fire22.png").convert_alpha())
        self.runPath2.append(pygame.image.load("walk//fire32.png").convert_alpha())
        self.runPath2.append(pygame.image.load("walk//fire42.png").convert_alpha())
        self.runPath2.append(pygame.image.load("walk//fire52.png").convert_alpha())
        self.runPath2.append(pygame.image.load("walk//fire62.png").convert_alpha())
        #"""
        self.path1.append(pygame.image.load("still//fire01.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire02.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire03.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire04.png").convert_alpha())
        
        self.path12.append(pygame.image.load("still//fire012.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire022.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire032.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire042.png").convert_alpha())
        #"""
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart1.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart2.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart3.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart4.png").convert_alpha())
        
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart12.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart22.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart32.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart42.png").convert_alpha())
        #"""
        self.jumpPath.append(pygame.image.load("jump//jumping1.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping2.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping3.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping4.png").convert_alpha())
        
        self.jumpPath2.append(pygame.image.load("jump//jumping12.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping22.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping32.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping42.png").convert_alpha())
        #"""
        self.endJump.append(pygame.image.load("jumpEnd//finishJump1.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump2.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump3.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump4.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump5.png").convert_alpha())
        self.endJump.append(pygame.image.load("jumpEnd//finishJump6.png").convert_alpha())
        
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump12.png").convert_alpha())
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump22.png").convert_alpha())
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump32.png").convert_alpha())
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump42.png").convert_alpha())
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump52.png").convert_alpha())
        self.endJump2.append(pygame.image.load("jumpEnd//finishJump62.png").convert_alpha())
        #"""
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump1.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump2.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump3.png").convert_alpha())
        
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump12.png").convert_alpha())
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump22.png").convert_alpha())
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump32.png").convert_alpha())
        #"""
        self.deadPath.append(pygame.image.load("muerte//dead1.png").convert_alpha())
        self.deadPath.append(pygame.image.load("muerte//dead2.png").convert_alpha())
        self.deadPath.append(pygame.image.load("muerte//dead3.png").convert_alpha())
        self.deadPath.append(pygame.image.load("muerte//dead4.png").convert_alpha())
        self.deadPath.append(pygame.image.load("muerte//dead5.png").convert_alpha())
        self.deadPath.append(pygame.image.load("muerte//dead6.png").convert_alpha())

        self.deadPath2.append(pygame.image.load("muerte//dead12.png").convert_alpha())
        self.deadPath2.append(pygame.image.load("muerte//dead22.png").convert_alpha())
        self.deadPath2.append(pygame.image.load("muerte//dead32.png").convert_alpha())
        self.deadPath2.append(pygame.image.load("muerte//dead42.png").convert_alpha())
        self.deadPath2.append(pygame.image.load("muerte//dead52.png").convert_alpha())
        self.deadPath2.append(pygame.image.load("muerte//dead62.png").convert_alpha())
        #"""
