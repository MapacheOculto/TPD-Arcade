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

    # Relacionado a pygame
def main():

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
        system_State = systemState()
            
        # Se inicializan los distintos estados de juego posibles
        play_State = playState(joystickList, screenSize, system_State, container)
        menu_State = titleState(joystickList, screenSize, system_State, container)
        game_OverState = gameOverState(joystickList, screenSize, system_State, container)
        pause_State = PauseState(joystickList, screenSize, system_State, container)
        world_MapState = gameWorldState(joystickList, screenSize, system_State, container)
        level_EndingState = LevelEndingState(joystickList, screenSize, system_State, container)
            
        # Se agregan estos estados a la instancia de systemState
        system_State.append(play_State, "playState")
        system_State.append(menu_State, "titleState")
        system_State.append(pause_State, "pauseState")
        system_State.append(game_OverState, "gameOverState")
        system_State.append(level_EndingState, "levelEndingState")
        system_State.append(world_MapState, "gameWorldState")
            
        # Se elije el estado de juego con el que se comenzara
        system_State.changeState("titleState")
            
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
                        if system_State.currentState == system_State.stateDictionary["playState"]:
                            system_State.currentState.level1.player1.keyHeldPressed = False
                            system_State.currentState.level1.player2.keyHeldPressed = False
                    if event.key == K_TAB:
                        pass
           
            # Se actualiza y dibuja el estado seleccionado
            system_State.update(elapsedTime)
            system_State.render()

            # se actualiza lo relativo a pygame
            pygame.display.update()
            
if __name__ == "__main__":
    main()
