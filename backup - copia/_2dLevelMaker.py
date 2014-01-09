import pygame
from pygame.locals import *
from platform import Platform
from enemigos import Turret
from enemigos import Cannon

class _2dLevelMaker:
        
    def __init__(self, group, exitGroup, damageGroup, imageDictionary, screenSize, filePath = "levels//ex1.txt"):
        # ATRIBUTOS
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]
        self.initialXAdvance = 0
        self.initialYAdvance = 0

        # GRUPOS (general, daninos, colores)
        self.group = group
        self.exitGroup = exitGroup
        self.damageGroup = damageGroup
        self.group2 = pygame.sprite.Group()
        self.torretas=[]

        # SPRITES
        self.imageDictionary = imageDictionary

        # FILE Y SCREEN SIZE
        self.readFile(filePath)
        self.moveGroupElements(self.initialXAdvance, self.initialYAdvance)

    # INILICIALIZA NUEVA ETAPA
    def changeFile(self, filePath, group):
        self.group.empty()
        self.readFile(filePath)

    # CREA ETAPA A PARTIR DE FILE
    def readFile(self, filePath):
        
        File = open(filePath)
        lines = File.readlines()
        File.close()
        
        ## ESTANDARIZAR ESTO
        #self.height = len(lines)
        #self.width = len(lines[len(lines) - 1])
        self.height = len(lines) - 3
        self.width = len(lines[0]) - 1

        self.nextStagePath = lines[self.height + 1].rstrip()
        self.nextBackgroundKey = lines[self.height + 2].rstrip()
        
        for i in range(self.height):
            line = list(lines[i])
            for j in range(self.width):
                ## Solucionar problema que hace que ultima linea tenga un char menos
                ## (ahora mismo existe solo una solucion temporal)
                if line[j] == '@':
                    self.initPlayerPosition(j, i)
                elif line[j] == 'l':
                    self.createDamageField(j, i, 'l')
                elif line[j] == 'w':
                    self.createDamageField(j, i, 'w')
                elif line[j] == 'a':
                    self.createSprite(lines,j, i, 'a')
                elif line[j] == 'c':
                    self.createSprite(lines,j, i, 'c')
                elif line[j] == 's':
                    self.createSprite(lines,j, i, 's')
                elif line[j] == 't':
                    self.createSprite(lines,j, i, 't')
                elif line[j] == 'b':
                    self.createSprite(lines,j, i, 'b')
                elif line[j] == 'r':
                    self.createSprite(lines,j, i, 'r')
                elif line[j] == '<':
                    self.createExit(j, i)
                elif line[j] == 'P':
                    self.createSprite(lines,j, i, 'P')
                elif line[j] == 'O':
                    self.createSprite(lines,j, i, 'O')  
                elif line[j] == "F":
                    self.createSprite(lines,j,i,"F")
                elif line[j] == "Q":
                    self.createSprite(lines,j,i,"Q")

                # ATRIBUTOS Turret y Cannon(x, y, color, rafaga, movil, angulo, velocidad, timer_entre_rafaga=2, timer_entre_bala=0.7)


                elif line[j]=='%':
                    self.torretas.append(Turret(j*50,i*50, 'Blue', 4, True, 130, 800))
                elif line[j]=='&':
                    self.torretas.append(Cannon(j*50,i*50, 'Green', 8, False, 125, 250))
                    
    # METODO POSICION INICIAL PERSONAJE. 
    def initPlayerPosition(self, j, i):
        x = self.stageScale * (j)
        y = self.stageScale * (i)
        halfH = self.screenHeight / 2.0
        halfW = self.screenWidth / 2.0
        width = (self.width - 1) * self.stageScale
        height = (self.height - 1) * self.stageScale
        self.startXPosition = halfW
        self.startYPosition = halfH
        
        if x <= halfW:
            self.startXPosition = x
            self.initialXAdvance = 0
        elif ( x > halfW ) and ( width - x > halfW ):
            self.initialXAdvance =  x - halfW 
        elif width - x <= halfW:
            self.startXPosition = self.screenWidth - (width - x)
            self.initialXAdvance = width - self.screenWidth

        if y <= halfH:
            self.startYPosition = y
            self.initialYAdvance = 0
        elif ( y > halfH ) and ( height - y > halfH ):
            self.initialYAdvance =  y - halfH
        elif height - y <= halfH:
            self.startYPosition = self.screenHeight - (height - y)
            self.initialYAdvance = height - self.screenHeight


    # Al crear etapa, mueve el background para que personaje parta al centro de la pantalla (o donde se quiera que parta)
    def moveGroupElements(self, xAdvance, yAdvance):
        
        self.firstRect = pygame.Rect((self.firstRect.left - xAdvance, self.firstRect.top - yAdvance), (self.stageScale, self.stageScale))
        self.lastRect  = pygame.Rect((self.lastRect.left - xAdvance, self.lastRect.top  - yAdvance), (self.stageScale, self.stageScale))

        spriteList = self.group.sprites()
        for sprite in spriteList:
            sprite.rect = pygame.Rect((sprite.rect.left - xAdvance, sprite.rect.top - yAdvance), (sprite.rect.width, sprite.rect.height))
        for sprite in self.exitGroup:
            sprite.rect = pygame.Rect((sprite.rect.left - xAdvance, sprite.rect.top - yAdvance), (sprite.rect.width, sprite.rect.height))
        for sprite in self.damageGroup:
            sprite.rect = pygame.Rect((sprite.rect.left - xAdvance, sprite.rect.top - yAdvance), (sprite.rect.width, sprite.rect.height))

        for torreta in self.torretas:
            torreta.x-=xAdvance
            torreta.y-=yAdvance
            torreta.cannon[0]-=xAdvance
            torreta.cannon[1]-=yAdvance

    # METODO QUE CREA SALIDA
    def createExit(self, j, i):
        self.stageScale = 50
        x = self.stageScale * (j)
        y = self.stageScale * (i)
        sprite = Platform()
        sprite.rect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
        sprite.image = self.imageDictionary["goldBrick"]
        sprite.image = pygame.transform.scale(sprite.image, (self.stageScale, self.stageScale))
                                               
        self.exitGroup.add(sprite);

#METODO QUE CREA PLATAFORMAS (tipo corresponde a horizontal o vertical)
    def createPlatform(self, lines, j, i, tipo):
        #Horizontal y vertical
        color = ""
        largo = 1
        
        if tipo == "H":
            aux = j + 1
            line = list(lines[i])
            while True:
               if line[aux] == '-':
                  largo = largo + 1
                  aux = aux + 1     
               elif line[aux] == 'G':
                   color = "Green"
                   largo = largo + 1
                   return (color,largo,0.5)
               elif line[aux] == 'B':
                   color = "Blue"
                   largo = largo + 1
                   return (color,largo,0.5)
               if aux > 1000:
                   print "ERROR EN CREATEPLATFORM"
                   break
        if tipo == "V":
                    aux = i - 1
                    line = list(lines[j])
                    while True:
                       if line[aux] == '|':
                          largo = largo + 1
                          aux = aux - 1     
                       elif line[aux] == 'G':
                           color = "Green"
                           largo = largo + 1
                           return (color,1,largo)
                       elif line[aux] == 'B':
                           color = "Blue"
                           largo = largo + 1
                           return (color,1,largo)
                       if aux > 100000:
                           print "ERROR EN CREATEPLATFORM"
                           break
# METODO QUE CREA SPRITES (actualmente son todas plataformas)
    def createSprite(self,lines, j, i, character):
        self.stageScale = 50
        
        # Para que player aparezca en esquina superior izquierda
        x = self.stageScale * (j)
        y = self.stageScale * (i)

        sprite = Platform()
        sprite.i = i
        sprite.j = j

        if character == "a":
            sprite.image = self.imageDictionary["topCement"]
            sprite.imagen2 = self.imageDictionary["topCement"]
        elif character == "t":
            sprite.image = self.imageDictionary["lowEarth"]
            sprite.imagen2 = self.imageDictionary["lowEarth"]
        elif character == "b":
            sprite.image = self.imageDictionary["water"]
            sprite.imagen2 = self.imageDictionary["watert"]
            sprite.color = "Blue"     
        elif character == "l":
            sprite.image = self.imageDictionary["lavat"]
            sprite.imagen2 = self.imageDictionary["lavat"]
        elif character == "s":
            sprite.image = self.imageDictionary["sand"]
            sprite.imagen2 = self.imageDictionary["sand"]
        elif character == "w":
            sprite.image = self.imageDictionary["watert"]
            sprite.imagen2 = self.imageDictionary["watert"]
        elif character == 'r':
            sprite.image = self.imageDictionary["lava"]
            sprite.imagen2 = self.imageDictionary["lava"]
            #sprite.color = "Green"
        elif character == "O":
             sprite.image = self.imageDictionary["water"]
             sprite.imagen2 = self.imageDictionary["watert"]
             sprite.color = "Blue" 
        elif character == "P":
            sprite.image = self.imageDictionary["lava"]
            sprite.imagen2 = self.imageDictionary["lavat"]
            sprite.color = "Green"
        elif character == "Q":
            sprite.image = self.imageDictionary["water"]
            sprite.imagen2 = self.imageDictionary["watert"]
            sprite.color = "Blue" 
        elif character == "F":
            sprite.image = self.imageDictionary["lava"]
            sprite.imagen2 = self.imageDictionary["lavat"]
            sprite.color = "Green"    

        else: 
            sprite.image = self.imageDictionary["lava"]
            sprite.imagen2 = self.imageDictionary["lavat"]
            sprite.color = "Green"

        if character == "P" or character == "O":
            colorlargo = self.createPlatform(lines,j,i,"H")
            color = colorlargo[0]
            scale_x = colorlargo[1]
            scale_y = colorlargo[2]
            sprite.color = color
            #scale = 2
            x = self.stageScale * (j)
            y = self.stageScale * (i)
            sprite.scale_x = scale_x
            sprite.scale_y = scale_y
            sprite.x_scale = self.stageScale *scale_x
            sprite.y_scale = self.stageScale*scale_y
            sprite.image = pygame.transform.scale(sprite.image, (int(scale_x*self.stageScale), int(scale_y*self.stageScale)))
            sprite.imagen2 = pygame.transform.scale(sprite.imagen2, (int(scale_x*self.stageScale), int(scale_y*self.stageScale)))
            sprite.rect = pygame.Rect((x, y), (scale_x*self.stageScale, scale_y*self.stageScale))
            sprite.imagenoriginal = sprite.image
        elif character == "F" or character == "Q":
            sprite.x_scale = self.stageScale 
            sprite.y_scale = self.stageScale
            sprite.image = pygame.transform.scale(sprite.image, (int(0.5*self.stageScale), 5*self.stageScale))
            sprite.imagen2 = pygame.transform.scale(sprite.imagen2, (int(0.5*self.stageScale), 5*self.stageScale))
            sprite.rect = pygame.Rect((x, y), (int(0.5*self.stageScale), 5*self.stageScale))
            sprite.imagenoriginal = sprite.image   
            if character == "F":
                sprite.color = "Green"
            elif character == "Q":
                sprite.color = "Blue"
        else:
            sprite.x_scale = self.stageScale 
            sprite.y_scale = self.stageScale
            sprite.image = pygame.transform.scale(sprite.image, (self.stageScale, self.stageScale))
            sprite.imagen2 = pygame.transform.scale(sprite.imagen2, (self.stageScale, self.stageScale))
            sprite.rect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
            sprite.imagenoriginal = sprite.image

        # Define rectangulos que serviran para delimitar etapa y limitar movimiento de la camara
        if i == 0 and j == 0:
            self.firstRect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
        elif i == (self.height - 1) and j == (self.width - 1):
            self.lastRect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
        sprite.colororiginal = sprite.color
        self.group.add(sprite); 
    
    # METODO QUE CREA SPRITES
    def createDamageField(self, j, i, character):
        
        self.stageScale = 50
        x = self.stageScale * (j)
        y = self.stageScale * (i)

        sprite = Platform() 
        if character == "l":
            sprite.image = self.imageDictionary["lava"]
        elif character == "w":
            sprite.image = self.imageDictionary["water"]
        else: 
            sprite.image = self.imageDictionary["bricks"]

        sprite.image = pygame.transform.scale(sprite.image, (self.stageScale, self.stageScale))
        sprite.rect = pygame.Rect((x, y), (self.stageScale, self.stageScale))

        # Define rectangulos que serviran para delimitar etapa y limitar movimiento de la camara
        if i == 0 and j == 0:
            self.firstRect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
        elif i == (self.height - 1) and j == (self.width - 1):
            self.lastRect = pygame.Rect((x, y), (self.stageScale, self.stageScale))
        
        self.damageGroup.add(sprite);     

   
   
     
