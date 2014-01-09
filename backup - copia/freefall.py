from math import radians
from math import sin
import pygame
from pygame import *

class FreeFall:
    
    def __init__(self, g = 25):
        self.g = g
        self.inProcess = False

    def start(self, y0):
        self.tempTimer = 0
        self.Y = y0
        self.yo = y0
        self.inProcess = True
        self.deltaY = 0

    def update(self, totalElapsedTime):
        tempY = self.Y
                
        self.Y = self.yPosition(totalElapsedTime)

        self.deltaY = self.Y - tempY

    def yPosition(self, time):
        t = 10 * time

        pos = self.yo - (0.5) * (self.g) * (t**2)

        #pos = self.yo - (0.5) * (self.g) * (self.tempTimer*self.tempTimer)
        #self.tempTimer += 0.2

        return pos

    def stop(self):
        self.inProcess = False
        self.deltaY = 0
        self.Y = 0
        self.tempTimer = 0


