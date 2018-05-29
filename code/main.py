#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as p

# General Settings
SIZE = WIDTH, HEIGHT = 800, 800
STEP = 1
FRAMERATE = 60

# Static Object constants
STARTPOS = [(400, 400), (400, 600)]
COLOR = [(255, 255, 0), (0, 255, 0)]
MASS = [10e2, 10]
RADIUS = [10, 5]

# Init GAME
p.init()  # Pygame initialisieren.
p.display.set_caption('Simulation')
screen = p.display.set_mode(SIZE)  # Fenstergrösse festlegen
clock = p.time.Clock()  # Brauchen wir zur Framerate-Kontrolle

running = True   # Kontrolliert die Repetition des Animations-Loops
animate = True   # Ob die Animation gerade läuft


# Class for all objects with mass
class Orb:
    orbs = []

    def __init__(self, screen, x=0, y=0, radius=10, color=(255, 255, 255)):
        self.screen = screen
        self.set_pos(x, y)
        self.color = color
        self.radius = radius

        self.orbs.append(self)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def get_force(self, partner):
        pass

    def move(self, x_step, y_step=0):
        self.x += x_step
        self.y += y_step

    def draw(self):
        p.draw.circle(self.screen, self.color, self.get_pos(), self.radius)

    @classmethod
    def force(cls):
        pass


# Init class instances
if (len(STARTPOS) != len(COLOR) or len(COLOR) != len(RADIUS)):
    print("Error in Constants")
for i in range(len(STARTPOS)):
    Orb(screen, *STARTPOS[i], RADIUS[i], COLOR[i])


##### ANIMATION LOOP #####
while running:
    screen.fill((0, 0, 0))  # black background

    clock.tick(FRAMERATE)

p.quit()
