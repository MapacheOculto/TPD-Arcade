import pygame
from pygame import *
from systemState import *
from playState import playState
from titleState import titleState
from gameOverState import gameOverState
from gameWorldState import gameWorldState
from LevelEndingState import LevelEndingState
from pauseState import PauseState


### Estos son los paths para las imagenes de las animaciones 
runPath = []
path1 = []
startJump = []
jumpPath = []
endJump = []
wallJumpRPath = []
deathPath = []

# FUNCION PRINCIPAL QUE CORRE CODIGO
class MAIN():

    # Relacionado a pygame
    pygame.init()
    screenSize = (1024,768)
    screen = pygame.display.set_mode(screenSize, 0, 32)
    pygame.display.set_caption("Missed Colours")

    # joysticks
    pygame.joystick.init()
    joystickList = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for i in range(len(joystickList)):
        joystickList[i].init()

    # Se inicializa systemState, la clase que va a apuntar a la instancia del estado en que se encuentre el juego
    systemState = systemState()
    
    # Se inicializan los distintos estados de juego posibles
    playState = playState(joystickList, screenSize, systemState)
    menuState = titleState(joystickList, screenSize, systemState)
    gameOverState = gameOverState(joystickList, screenSize, systemState)
    pauseState = PauseState(joystickList, screenSize, systemState)
    worldMapState = gameWorldState(joystickList, screenSize, systemState)
    levelEndingState = LevelEndingState(joystickList, screenSize, systemState)
    
    # Se agregan estos estados a la instancia de systemState
    systemState.append(playState, "playState")
    systemState.append(menuState, "titleState")
    systemState.append(pauseState, "pauseState")
    systemState.append(gameOverState, "gameOverState")
    systemState.append(levelEndingState, "levelEndingState")
    systemState.append(worldMapState, "gameWorldState")
    
    # Se elije el estado de juego con el que se comenzara
    systemState.changeState("titleState")
    
    # Timer para el tiempo transcurrido
    ticker = pygame.time.Clock()    


    # LOOP PRINCIPAL DEL JUEGO
    while True:

        # Timer
        elapsedTime = ticker.tick(30) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if systemState.currentState == systemState.stateDictionary["playState"]:
                        systemState.currentState.level1.player1.keyHeldPressed = False
                        systemState.currentState.level1.player2.keyHeldPressed = False
                if event.key == K_TAB:
                    pass
   
        # Se actualiza y dibuja el estado seleccionado
        systemState.update(elapsedTime)
        systemState.render()

        # se actualiza lo relativo a pygame
        pygame.display.update()


    # PARA DESPUES
    def initImagesForAnimation(self):

        runPath.append(pygame.image.load("walk//fire1.png").convert_alpha())
        runPath.append(pygame.image.load("walk//fire2.png").convert_alpha())
        runPath.append(pygame.image.load("walk//fire3.png").convert_alpha())
        runPath.append(pygame.image.load("walk//fire4.png").convert_alpha())
        runPath.append(pygame.image.load("walk//fire5.png").convert_alpha())
        runPath.append(pygame.image.load("walk//fire6.png").convert_alpha())
        
        path1.append(pygame.image.load("still//fire01.png").convert_alpha())
        path1.append(pygame.image.load("still//fire02.png").convert_alpha())
        path1.append(pygame.image.load("still//fire03.png").convert_alpha())
        path1.append(pygame.image.load("still//fire04.png").convert_alpha())
        
        startJump.append(pygame.image.load("jumpStart//jumpStart1.png").convert_alpha())
        startJump.append(pygame.image.load("jumpStart//jumpStart2.png").convert_alpha())
        startJump.append(pygame.image.load("jumpStart//jumpStart3.png").convert_alpha())
        startJump.append(pygame.image.load("jumpStart//jumpStart4.png").convert_alpha())
        
        jumpPath.append(pygame.image.load("jump//jumping1.png").convert_alpha())
        jumpPath.append(pygame.image.load("jump//jumping2.png").convert_alpha())
        jumpPath.append(pygame.image.load("jump//jumping3.png").convert_alpha())
        jumpPath.append(pygame.image.load("jump//jumping4.png").convert_alpha())
        
        endJump.append(pygame.image.load("jumpEnd//finishJump1.png").convert_alpha())
        endJump.append(pygame.image.load("jumpEnd//finishJump2.png").convert_alpha())
        endJump.append(pygame.image.load("jumpEnd//finishJump3.png").convert_alpha())
        endJump.append(pygame.image.load("jumpEnd//finishJump4.png").convert_alpha())
        endJump.append(pygame.image.load("jumpEnd//finishJump5.png").convert_alpha())
        endJump.append(pygame.image.load("jumpEnd//finishJump6.png").convert_alpha())

        wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump1.png").convert_alpha())
        wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump2.png").convert_alpha())
        wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump3.png").convert_alpha())

        deathPath.append(pygame.image.load("muerte//jumping1.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping2.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping3.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping4.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping5.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping6.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping7.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping8.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping9.png").convert_alpha())
        deathPath.append(pygame.image.load("muerte//jumping10.png").convert_alpha())

