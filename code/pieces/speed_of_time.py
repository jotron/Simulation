import pygame, sys
from pygame.locals import *
import numpy as np
factors = np.array([1, 100, 1000, 5000])
def changespeed(liste, event):
    i = 0
    if event.type == KEYUP:
        if event.key == K_UP:
            i+=1
        if event.key == K_DOWN:
            i-=1
    speed = liste[i]
    return speed
speed = 1
#alles da unten kommt in while Schleife

for event in pygame.event.get():
    speed = changespeed(factors,event)

myfont = pygame.font.SysFont("monospace", 25)
label = myfont.render("speed:" + " " + speed + "X" , 1, (0, 0, 255))
screen.blit(label, (700, 50))
