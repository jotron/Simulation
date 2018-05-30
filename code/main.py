#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as p
import numpy as np
import sys

# General Settings
SIZE = WIDTH, HEIGHT = 800, 800
STEP = 0.5
FRAMERATE = 30
TRACELENGTH = 50

# ORB Constants
# Sun, Venus, Earth, Mars, Jupyter Saturn
center = np.array([WIDTH/2, HEIGHT/2])
STARTPOS = [center, center + np.array([0, 200]), center + np.array([300, 0])]
STARTVEL = [0, 0, 0]
COLOR = [(255, 255, 0), (0, 255, 0), (0, 255, 255)]
MASS = [10e2, 10, 1]
RADIUS = [10, 5, 20]

# Init GAME
p.init()  # Pygame initialisieren.
p.display.set_caption('Simulation')
screen = p.display.set_mode(SIZE)  # Fenstergrösse festlegen
clock = p.time.Clock()  # Brauchen wir zur Framerate-Kontrolle

# background_image
background_image = p.image.load("assets/background.jpg").convert()


# Class for all objects with mass
class Orb:
    orbs = []

    def __init__(self, screen, pos=np.zeros(2), radius=10, color=(255, 255, 255),
                 trace_color=(180, 180, 180)):
        self.screen = screen
        self.pos = pos
        self.color = color
        self.radius = radius

        self.trace_color = trace_color
        self.trace = np.tile(pos, (TRACELENGTH, 1))
        self.counter = 0

        self.orbs.append(self)

    # Basic Functions
    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def move(self, pos_step=np.zeros(2)):
        self.pos += pos_step

    def draw(self):
        # every half second store trace
        self.counter += 1
        if (self.counter >= FRAMERATE/2):
            self.counter = 0
            self.trace[:-1] = self.trace[1:]
            self.trace[-1] = self.pos

        p.draw.circle(self.screen, self.color,
                      tuple(self.pos.astype(int)), self.radius)

    def draw_trace(self):
        tuple_list = list(map(tuple, self.trace))
        p.draw.aalines(self.screen, self.trace_color, True, tuple_list, 1)

    # gives acceleration that an orb recieves from another
    def get_a(self, another):
        a = another.pos-self.pos
        a_normed = a / np.linalg.norm(a)
        return a_normed

    # Move all orbs according to gravitational force
    @classmethod
    def run_all(cls):
        for orb1 in cls.orbs:
            # Sum up forces exerted from all other orbs
            orb1_a = np.zeros(2)
            for orb2 in cls.orbs:
                # No division through 0
                if not (orb1.pos[0] == orb2.pos[0] and orb1.pos[1] == orb2.pos[1]):
                    orb1_a += orb1.get_a(orb2)

            # Get velocity from acceleration
            orb1_v = orb1_a * STEP
            orb1_dr = orb1_v * STEP
            orb1.move(orb1_dr)

    # Draw all orbs
    @classmethod
    def draw_all(cls):
        for orb1 in cls.orbs:
            orb1.draw()
            orb1.draw_trace()


# Initialize class instances
if (len(STARTPOS) != len(COLOR) or len(COLOR) != len(RADIUS)):
    print("Error in Constants")
for i in range(len(STARTPOS)):
    Orb(screen, STARTPOS[i], RADIUS[i], COLOR[i])


# ANIMATION LOOP #
while 1:
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()

    # Nice Background
    screen.blit(background_image, [0, 0])

    # Do Gravition Stuff
    Orb.run_all()
    Orb.draw_all()

    p.display.update()
    clock.tick(FRAMERATE)
