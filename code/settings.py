import numpy as np

# VISUAL
SIZE = WIDTH, HEIGHT = 800, 800
FRAMERATE = 30

# GENERAL SIMULATION
TIME_STEP = 3600 * 100
FRAMERATE = 30
TRACE_TIME = 365 * 24 * 3600  # TIME_LENGTH of TRACE
TRACE_LENGTH = 100
V_SIZE = V_WIDTH, V_HEIGHT = 3.5e9, 3.5e9  # Total size of System = 3e9km
SPEED_FACTORS = [1, 10000, 1000000, 5000000, 10000000,
                 20000000, 50000000, 100000000]
SPEED_INDEX = 1
v_center = np.array([V_WIDTH/2, V_HEIGHT/2])

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
