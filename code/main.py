#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as p
import numpy as np
import sys

# General Settings
SIZE = WIDTH, HEIGHT = 800, 800
TIME_STEP = 3600 * 100
FRAMERATE = 30
TRACE_TIME = 365 * 24 * 3600  # TIME_LENGTH of TRACE
TRACE_LENGTH = 100
V_SIZE = V_WIDTH, V_HEIGHT = 3.5e9, 3.5e9  # Total size of System = 3e9km
SPEED_FACTORS = [1, 10000, 1000000, 5000000, 10000000,
                 20000000, 50000000, 100000000]
SPEED_INDEX = 1
v_center = np.array([V_WIDTH/2, V_HEIGHT/2])

# Space_object Constants
STARTPOS = [v_center,                             # Sun
            v_center + np.array([0, 15.21e7]),    # Earth
            v_center + np.array([0, 24.99e7]),    # Mars
            v_center + np.array([0, 81.9e7]),     # Jupyter
            v_center + np.array([0, 15.1857e8])]  # Saturn
STARTVEL = [np.array([0, 0]),      # Sun
            np.array([29.29, 0]),  # Earth 29.29
            np.array([21.97, 0]),  # Mars
            np.array([12.45, 0]),  # Jupyter
            np.array([9.11, 0])]    # Saturn
MASS = [2e30, 5.974e24, 6.419e23, 1.9e27, 5.685e26]
COLOR = [(255, 255, 0),    # Sun = Yellow
         (0, 0, 255),      # Earth = Blue
         (255, 0, 0),      # Mars = Red
         (153, 102, 51),   # Jupyter = Brown
         (140, 140, 140)]  # Saturn = Grey
RADIUS = [10, 5, 3, 8, 9]

# Init GAME
p.init()

# Set Pygame setting
p.display.set_caption('Simulation')
screen = p.display.set_mode(SIZE)  # Fenstergrösse festlegen
clock = p.time.Clock()  # Brauchen wir zur Framerate-Kontrolle
# background_image
background_image = p.image.load("assets/background.jpg").convert()
MAINFONT = p.font.SysFont("monospace", 25)


# Class for all objects with mass
class Space_object:
    space_objects = []
    step_accumulation = 0.0
    trace_accumulation = 0.0

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
        self.trace_true = np.tile(pos, (TRACE_LENGTH, 1))
        self.trace_index = 0

        self.space_objects.append(self)

    # Change Position and Velocity
    def change_state(self, pos, vel):
        self.pos = pos
        self.vel = vel

    # Draw Space Object
    def draw(self, trace_accumulation):
        # store position for one year
        trace_step = (365*24*3600) / TRACE_LENGTH
        for i in range(int(trace_accumulation / trace_step)):
            print("trace")
            self.trace_true[self.trace_index % TRACE_LENGTH] = self.pos
            self.trace_index += 1

        # draw shape
        p.draw.circle(self.screen, self.color,
                      self.convert(self.pos).tolist(), self.radius)

        # draw trace
        rolled_trace = np.roll(self.trace_true, -self.trace_index, 0)
        trace_list = self.convert(rolled_trace).tolist()
        p.draw.aalines(self.screen, self.trace_color, False, trace_list, 1)

    # Get next position and velocity
    @classmethod
    def get_next_state(cls, AWP, dt):

        # DGL for N-Objects
        def DGL(pos):
            G = 6.674e-20  # in km
            a = np.zeros_like(pos)

            for i in range(0, len(pos)):
                for j in range(i+1, len(pos)):
                    # Space Object Position
                    soi = cls.space_objects[i]
                    soj = cls.space_objects[j]
                    # Vector from i to j
                    rij = soj.pos - soi.pos
                    # Force from i to j
                    Fij = (G * soi.mass * soj.mass * rij) / np.linalg.norm(rij)**3
                    # Acceleration on soi and soj
                    a[i] += Fij / soi.mass
                    a[j] -= Fij / soj.mass
            return a

        # # # # # # # #
        # Runge Kutta #
        # # # # # # # #

        k1 = np.array([AWP[1], DGL(AWP[0])])

        # Halber Euler-Schritt
        v_tmp = AWP + k1*dt/2
        k2 = np.array([v_tmp[1], DGL(v_tmp[0])])

        # Halber Euler-Schritt mit der neuen Steigung
        v_tmp = AWP + k2*dt/2
        k3 = np.array([v_tmp[1], DGL(v_tmp[0])])

        # ganzer Euler-Schritt mit k3
        v_tmp = AWP + k3*dt
        k4 = np.array([v_tmp[1], DGL(v_tmp[0])])

        # NEXT_STATE = Postion, Velocity
        rk = AWP + dt*(k1 + 2*k2 + 2*k3 + k4)/6
        return rk

    # Move all Space_object's according to gravitational force
    @classmethod
    def run_all(cls):
        # Do multiple small steps per FRAME
        # Set DELTAT smaller
        dt = TIME_STEP
        # set AWP to temporarily store state
        state = np.array([[space_object1.pos for space_object1
                         in cls.space_objects],
                         [space_object1.vel for space_object1
                         in cls.space_objects]])
        # Loop for all MINI_STEPS, if ministep smaller 0 save for later
        mini_steps = SPEED_FACTORS[SPEED_INDEX] / (FRAMERATE * TIME_STEP)
        cls.step_accumulation += mini_steps
        for i in range(int(cls.step_accumulation)):
            # Runge Kutta with physics
            state = Space_object.get_next_state(state, dt)
        cls.step_accumulation -= int(cls.step_accumulation)

        # Apply to all ojects as tupple
        for i, space_object1 in enumerate(cls.space_objects):
            next_pos = state[0][i]
            next_vel = state[1][i]
            space_object1.change_state(next_pos, next_vel)

        # set trace accumulation
        print(cls.trace_accumulation)
        cls.trace_accumulation += SPEED_FACTORS[SPEED_INDEX] / FRAMERATE

    # Draw all space_objects
    @classmethod
    def draw_all(cls):
        for space_object1 in cls.space_objects:
            space_object1.draw(cls.trace_accumulation)

        # reset trace_accumulation
        trace_step = (365*24*3600) / TRACE_LENGTH
        cls.trace_accumulation = cls.trace_accumulation % trace_step

    # Draw all space_objects
    @staticmethod
    def convert(pos):
        tmp_pos = pos / V_SIZE * SIZE
        #  print(pos, tmp_pos, tuple(tmp_pos.astype(int)))
        return tmp_pos.round().astype(int)


# Initialize class instances
for i in range(len(STARTPOS)):
    Space_object(screen, STARTPOS[i], RADIUS[i], MASS[i], STARTVEL[i], COLOR[i])


# ANIMATION LOOP #
while 1:
    for event in p.event.get():
        # QUIT
        if event.type == p.QUIT:
            sys.exit()
        # SET SPEED
        if event.type == p.KEYUP:
            if (event.key == p.K_UP and SPEED_INDEX < len(SPEED_FACTORS) - 1):
                SPEED_INDEX += 1
            if (event.key == p.K_DOWN and SPEED_INDEX >= 1):
                SPEED_INDEX -= 1

    # Nice Background
    screen.blit(background_image, [0, 0])

    # Do Gravition Stuff
    Space_object.run_all()
    Space_object.draw_all()

    # Display current SPEED
    SPEEDLABEL = MAINFONT.render(f"X {SPEED_FACTORS[SPEED_INDEX]}", 1, (0, 255, 255))
    screen.blit(SPEEDLABEL, (680, 20))

    p.display.update()
    clock.tick(FRAMERATE)
