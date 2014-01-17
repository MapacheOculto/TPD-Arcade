import pygame
from pygame import *
from pygame import mixer
from systemState import *
from playState import playState
from titleState import titleState
from gameOverState import gameOverState
from gameWorldState import gameWorldState
from LevelEndingState import LevelEndingState
from pauseState import PauseState
from container import Container


# FUNCION PRINCIPAL QUE CORRE CODIGO
class MAIN():

    # Relacionado a pygame
    pygame.init()
    mixer.init()
    screenSize = (1024,768)
    screen = pygame.display.set_mode(screenSize, 0, 32)
    pygame.display.set_caption("Missed Colours")
    container = Container()

    # joysticks
    pygame.joystick.init()
    joystickList = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for i in range(len(joystickList)):
        joystickList[i].init()

    # Se inicializa systemState, la clase que va a apuntar a la instancia del estado en que se encuentre el juego
    systemState = systemState()
    
    # Se inicializan los distintos estados de juego posibles
    playState = playState(joystickList, screenSize, systemState, container)
    menuState = titleState(joystickList, screenSize, systemState, container)
    gameOverState = gameOverState(joystickList, screenSize, systemState, container)
    pauseState = PauseState(joystickList, screenSize, systemState, container)
    worldMapState = gameWorldState(joystickList, screenSize, systemState, container)
    levelEndingState = LevelEndingState(joystickList, screenSize, systemState, container)
    
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
