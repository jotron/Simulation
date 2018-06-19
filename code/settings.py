import numpy as np
import pygame as p
p.init()

# VISUAL
SIZE = WIDTH, HEIGHT = 800, 800
FRAMERATE = 30

# GENERAL SIMULATION
TIME_STEP = 3600 * 24
V_SIZE = V_WIDTH, V_HEIGHT = 3.5e9, 3.5e9  # Total size of System = 3e9km
SPEED_FACTORS = [1, 10000, 1000000, 5000000, 10000000,
                 20000000, 50000000, 100000000]
SPEED_INDEX = 1
ZOOM_FACTOR = 1.0
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
OBJECT_IMG = [p.image.load('assets/sun.png'),
              p.image.load('assets/earth.png'),
              p.image.load('assets/mars.png'),
              p.image.load('assets/jupiter.png'),
              p.image.load('assets/saturn.png')]
COLOR = [(255, 255, 0),    # Sun = Yellow
         (0, 0, 255),      # Earth = Blue
         (255, 0, 0),      # Mars = Red
         (153, 102, 51),   # Jupyter = Brown
         (140, 140, 140)]  # Saturn = Grey
RADIUS = [695700.0, 6378.0, 3396.0, 69911.0, 60268.0]
TRACE_LENGTH = [5, 50, 50, 150, 150]
TRACE_TIME = [24*3600*365*29.5, 24*3600*365, 24*3600*687, 24*3600*365*11.8, 24*3600*365*29.5]

# COLORS
black = (0, 0, 0)
grey = (50, 131, 134)
white = (255, 255, 255)
white_cyan = (255, 250, 240)
red = (200, 0, 0)
green = (0, 200, 0)
yellow = (255, 193, 37)
bright_yellow = (255, 215, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
yellow_launch = (245, 222, 179)
bright_yellow_launch = (255, 235, 205)
lime = (0, 255, 0)
grey = (30, 30, 30)
