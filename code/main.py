#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as p
import numpy as np
import sys

# General Settings
SIZE = WIDTH, HEIGHT = 800, 800
TIME_STEP = 3 * 24 * 3600 * 2
FRAMERATE = 45
TRACELENGTH = 50
V_SIZE = V_WIDTH, V_HEIGHT = 3.5e9, 3.5e9  # Total size of System = 3e9km
v_center = np.array([V_WIDTH/2, V_HEIGHT/2])

# Orb Constants
STARTPOS = [v_center,                             # Sun
            v_center + np.array([0, 15.21e7]),    # Earth
            v_center + np.array([0, 24.99e7]),    # Mars
            v_center + np.array([0, 81.9e7]),     # Jupyter
            v_center + np.array([0, 15.1857e8])]  # Saturn
STARTVEL = [np.array([0, 0]),      # Sun
            np.array([29.29, 0]),  # Earth
            np.array([21.97, 0]),  # Mars
            np.array([13.17, 0]),  # Jupyter
            np.array([9.2, 0])]   # Saturn
MASS = [2e30, 5.974e24, 6.419e23, 1.9e27, 5.685e26]
COLOR = [(255, 255, 0),    # Sun = Yellow
         (0, 0, 255),      # Earth = Blue
         (255, 0, 0),      # Mars = Red
         (153, 102, 51),   # Jupyter = Brown
         (140, 140, 140)]  # Saturn = Grey
RADIUS = [10, 5, 3, 8, 9]

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

    def __init__(self, screen, pos=np.zeros(2), radius=10, mass=5.9*10**24,
                 vel=np.zeros(2),
                 color=(255, 255, 255),
                 trace_color=(180, 180, 180)):
        self.screen = screen
        self.pos = pos
        self.color = color
        self.radius = radius
        self.mass = mass
        self.vel = vel

        self.trace_color = trace_color
        self.trace = np.tile(pos, (TRACELENGTH, 1))
        self.counter = 0

        self.orbs.append(self)

    # Change Position and Velocity
    def change_state(self, pos, vel):
        self.pos = pos
        self.vel = vel

    # Draw Orb
    def draw(self):
        # every half second store trace
        #  self.counter += 1
        #  if (self.counter >= FRAMERATE/2):
        #    self.counter = 0
        #    self.trace[:-1] = self.trace[1:]
        #    self.trace[-1] = self.pos
        p.draw.circle(self.screen, self.color,
                      self.convert(self.pos), self.radius)

    # Draw trace behind Orb
    def draw_trace(self):
        tuple_list = list(map(self.convert, self.trace))
        p.draw.aalines(self.screen, self.trace_color, True, tuple_list, 1)

    # Get next position and velocity
    def get_next_state(self):

        # DGL
        def SIMPLE_DGL(pos1, orb2):
            G = 6.674e-20  # in km
            r = orb2.pos - pos1
            return (G * orb2.mass * r) / np.linalg.norm(r)**3

        def N_DGL(pos1):
            a = np.zeros(2)
            for orb2 in self.orbs:
                if (id(self) == id(orb2)):
                    continue
                a += SIMPLE_DGL(pos1, orb2)
            return a

        # DT
        dt = TIME_STEP
        # AWP
        AWP = np.array([self.pos, self.vel])

        # # # # # # # #
        # Runge Kutta #
        # # # # # # # #

        k1 = np.array([AWP[1], N_DGL(AWP[0])])

        # Halber Euler-Schritt
        v_tmp = AWP + k1*dt/2
        k2 = np.array([v_tmp[1], N_DGL(v_tmp[0])])

        # Halber Euler-Schritt mit der neuen Steigung
        v_tmp = AWP + k2*dt/2
        k3 = np.array([v_tmp[1], N_DGL(v_tmp[0])])

        # ganzer Euler-Schritt mit k3
        v_tmp = AWP + k3*dt
        k4 = np.array([v_tmp[1], N_DGL(v_tmp[0])])

        # NEXT_STATE = Postion, Velocity
        rk = AWP + dt*(k1 + 2*k2 + 2*k3 + k4)/6
        return rk[0], rk[1]

    # Move all orbs according to gravitational force
    @classmethod
    def run_all(cls):
        for orb1 in cls.orbs:
            # Runge Kutta with physics
            next_pos, next_vel = orb1.get_next_state()
            # Move
            orb1.change_state(next_pos, next_vel)

    # Draw all orbs
    @classmethod
    def draw_all(cls):
        for orb1 in cls.orbs:
            orb1.draw()
            #  orb1.draw_trace_converted()

    # Draw all orbs
    @staticmethod
    def convert(pos):
        tmp_pos = pos / V_SIZE * SIZE
        #  print(pos, tmp_pos, tuple(tmp_pos.astype(int)))
        return tuple(tmp_pos.astype(int))


# Initialize class instances
for i in range(len(STARTPOS)):
    Orb(screen, STARTPOS[i], RADIUS[i], MASS[i], STARTVEL[i], COLOR[i])


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
