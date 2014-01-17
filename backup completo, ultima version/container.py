import pygame
from pygame import *
from pygame import mixer


# CLASE QUE DEBERIA CONTENER TODAS LAS IMAGENES Y SONIDOS; Y ASI SOLO SE CARGAN UNA VEZ
class Container:


    # Constructor, crea todos los diccionarios y despues llama a metodo que los llena
    def __init__(self):

        self.imageDictionary = {}
        self.soundDictionary = {}
        
        self.lavaAnimation = []
        self.iceAnimation = []
        self.itemAnimation1 = []
        self.itemAnimation2 = []

        self.runPath = []
        self.path1 = []
        self.startJumpPath = []
        self.jumpPath = []
        self.endJump = []
        self.wallJumpRPath = []
        self.runPath2 = []
        self.path12 = []
        self.startJumpPath2 = []
        self.jumpPath2 = []
        self.endJump2 = []
        self.wallJumpRPath2 = []
        self.deadPath = []
        self.deadPath2 = []

        self.setSounds()
        self.setImages()
        

    # Deja todos los diccionarios listos con los sonidos
    def setSounds(self):
        
        self.soundDictionary.update({"jump" : mixer.Sound('sounds//jump.wav')})
        self.soundDictionary.update({"back" : mixer.Sound('sounds//back.wav.wav')})
        self.soundDictionary.update({"burn" : mixer.Sound('sounds//burn1.wav')})
        self.soundDictionary.update({"laser1" : mixer.Sound('sounds//laser.wav')})
        self.soundDictionary.update({"laser2" : mixer.Sound('sounds//laser2.wav')})
        self.soundDictionary.update({"life" : mixer.Sound('sounds//life.wav')})
        self.soundDictionary.update({"point" : mixer.Sound('sounds//points.wav')})
        self.soundDictionary.update({"select" : mixer.Sound('sounds//select.wav')})
        self.soundDictionary.update({"slide1" : mixer.Sound('sounds//slide.mp3')})
        self.soundDictionary.update({"slide2" : mixer.Sound('sounds//slide.wav')})
        self.soundDictionary.update({"walk" : mixer.Sound('sounds//walk.wav')})


    # Deja todos los diccionarios listos con sus imagenes
    def setImages(self):
        
        # Sprites de 100x100
        self.imageDictionary.update({"lowEarth" : pygame.image.load("blocks//lowEarth.png").convert()})
        self.imageDictionary.update({"topCement" : pygame.image.load("blocks//topa2.png").convert()})
        self.imageDictionary.update({"grass" : pygame.image.load("blocks//grass.png").convert()})
        self.imageDictionary.update({"topGrass" : pygame.image.load("blocks//grass2.png").convert()})
        self.imageDictionary.update({"lava" : pygame.image.load("blocks//lava4.png").convert()})  
        self.imageDictionary.update({"ice" : pygame.image.load("blocks//ice.png").convert()})
        self.imageDictionary.update({"green" : pygame.image.load("blocks//green.png").convert()})
        self.imageDictionary.update({"greenAlpha" : pygame.image.load("blocks//greenAlpha.png").convert()})   
        self.imageDictionary.update({"blue" : pygame.image.load("blocks//blue.png").convert()})
        self.imageDictionary.update({"blueAlpha" : pygame.image.load("blocks//blueAlpha.png").convert()})
        self.imageDictionary.update({"sand" : pygame.image.load("blocks//sand.png").convert()})
        self.imageDictionary.update({"goldBrick" : pygame.image.load("blocks//goldBrick.png").convert()})
        self.imageDictionary.update({"exit" : pygame.image.load("blocks//exit.png").convert()})

        # imagenes de fondo
        self.imageDictionary.update({"fondo" : pygame.image.load("blocks//asddfg.jpg").convert()})
        self.imageDictionary.update({"fondoDesierto" : pygame.image.load("blocks//fondoDesierto.png").convert()})

        # Animacion lava
        self.lavaAnimation.append(pygame.image.load("blocks//lava1.png").convert_alpha())
        self.lavaAnimation.append(pygame.image.load("blocks//lava2.png").convert_alpha()) 
        self.lavaAnimation.append(pygame.image.load("blocks//lava3.png").convert_alpha())
        self.lavaAnimation.append(pygame.image.load("blocks//lava4.png").convert_alpha())
        
        # Animacion hielo
        self.iceAnimation.append(pygame.image.load("blocks//ice0.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice1.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice2.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice3.png").convert_alpha())
        self.iceAnimation.append(pygame.image.load("blocks//ice4.png").convert_alpha())

        # Animacion item 1
        self.itemAnimation1.append(pygame.image.load("blocks//life1.png").convert_alpha())
        self.itemAnimation1.append(pygame.image.load("blocks//life1.png").convert_alpha())   
        self.itemAnimation1.append(pygame.image.load("blocks//life2.png").convert_alpha())   
        self.itemAnimation1.append(pygame.image.load("blocks//life2.png").convert_alpha())   

        # animacion item 2
        self.itemAnimation2.append(pygame.image.load("blocks//points1.png").convert_alpha())
        self.itemAnimation2.append(pygame.image.load("blocks//points1.png").convert_alpha())   
        self.itemAnimation2.append(pygame.image.load("blocks//points2.png").convert_alpha())   
        self.itemAnimation2.append(pygame.image.load("blocks//points2.png").convert_alpha())

        # Animaciones de players 1 y 2
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
        
        self.path1.append(pygame.image.load("still//fire01.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire02.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire03.png").convert_alpha())
        self.path1.append(pygame.image.load("still//fire04.png").convert_alpha())
        
        self.path12.append(pygame.image.load("still//fire012.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire022.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire032.png").convert_alpha())
        self.path12.append(pygame.image.load("still//fire042.png").convert_alpha())
        
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart1.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart2.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart3.png").convert_alpha())
        self.startJumpPath.append(pygame.image.load("jumpStart//jumpStart4.png").convert_alpha())
        
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart12.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart22.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart32.png").convert_alpha())
        self.startJumpPath2.append(pygame.image.load("jumpStart//jumpStart42.png").convert_alpha())
        
        self.jumpPath.append(pygame.image.load("jump//jumping1.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping2.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping3.png").convert_alpha())
        self.jumpPath.append(pygame.image.load("jump//jumping4.png").convert_alpha())
        
        self.jumpPath2.append(pygame.image.load("jump//jumping12.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping22.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping32.png").convert_alpha())
        self.jumpPath2.append(pygame.image.load("jump//jumping42.png").convert_alpha())
        
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
        
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump1.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump2.png").convert_alpha())
        self.wallJumpRPath.append(pygame.image.load("wallJumpR//wallJump3.png").convert_alpha())
        
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump12.png").convert_alpha())
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump22.png").convert_alpha())
        self.wallJumpRPath2.append(pygame.image.load("wallJumpR//wallJump32.png").convert_alpha())
        
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
        

    

    
