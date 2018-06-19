import pygame as p
import numpy as np
import sys

import settings as s
import menu as menu

# PYGAME INITIALISIEREN UND EINSTELLEN
pygame = p.init()
p.display.set_caption('Simulation')
screen = p.display.set_mode(s.SIZE)  # Fenstergrösse festlegen
clock = p.time.Clock()  # Brauchen wir zur Framerate-Kontrolle

# background_image
background_image = p.image.load("assets/background.jpg").convert()
MAINFONT = p.font.SysFont("monospace", 25)


# Class for all objects with mass
class Space_object:
    space_objects = []
    step_accumulation = 0.0

    def __init__(self, screen, pos, mass, img,
                 vel=np.zeros(2),
                 trace_color=(180, 180, 180),
                 trace_length=100, trace_time=3600*24*365):
        self.screen = screen
        self.pos = pos
        self.img = img
        self.mass = mass
        self.vel = vel

        self.trace_color = trace_color
        self.trace_length = trace_length
        self.trace_time = trace_time
        self.trace_accumulation = 0.0
        self.trace = np.tile(pos, (trace_length, 1))
        self.trace_index = 0

        self.space_objects.append(self)

    # Change Position and Velocity
    def change_state(self, pos, vel):
        self.pos = pos
        self.vel = vel

    # Draw Space Object
    def draw(self):
        # store position for one year
        self.trace_accumulation += s.SPEED_FACTORS[s.SPEED_INDEX] / s.FRAMERATE
        trace_step = (self.trace_time) / self.trace_length
        for i in range(int(self.trace_accumulation / trace_step)):
            self.trace[self.trace_index % self.trace_length] = self.pos
            self.trace_index += 1
        self.trace_accumulation = self.trace_accumulation % trace_step

        # draw trace
        rolled_trace = np.roll(self.trace, -self.trace_index, 0)
        trace_list = self.convert(rolled_trace).tolist()
        p.draw.aalines(self.screen, self.trace_color, False, trace_list, 1)

        # draw shape
        self.screen.blit(self.img,
                         self.img.get_rect(center=self.convert(self.pos).tolist()))

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
                    mi = cls.space_objects[i].mass
                    mj = cls.space_objects[j].mass
                    # Vector from i to j
                    rij = pos[j] - pos[i]
                    # Force from i to j
                    Fij = (G * mi * mj * rij) / np.linalg.norm(rij)**3
                    # Acceleration on soi and soj
                    a[i] += Fij / mi
                    a[j] -= Fij / mj
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
        dt = s.TIME_STEP
        # set AWP to temporarily store state
        state = np.array([[space_object1.pos for space_object1
                         in cls.space_objects],
                         [space_object1.vel for space_object1
                         in cls.space_objects]])
        # Loop for all MINI_STEPS, if ministep smaller 0 save for later
        mini_steps = s.SPEED_FACTORS[s.SPEED_INDEX] / (s.FRAMERATE * s.TIME_STEP)
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

    # Draw all space_objects
    @classmethod
    def draw_all(cls):
        for space_object1 in cls.space_objects:
            space_object1.draw()

    # Draw all space_objects
    @staticmethod
    def convert(pos):
        tmp_pos = pos / s.V_SIZE * s.SIZE
        #  print(pos, tmp_pos, tuple(tmp_pos.astype(int)))
        return tmp_pos.round().astype(int)


# ANIMATION LOOP #
def animation_loop():
    while 1:
        for event in p.event.get():
            # QUIT
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                sys.exit()
            # SET SPEED
            if event.type == p.KEYUP:
                if (event.key == p.K_UP and s.SPEED_INDEX < len(s.SPEED_FACTORS) - 1):
                    s.SPEED_INDEX += 1
                if (event.key == p.K_DOWN and s.SPEED_INDEX >= 1):
                    s.SPEED_INDEX -= 1

        # Nice Background
        screen.blit(background_image, [0, 0])

        # Do Gravition Stuff
        Space_object.run_all()
        Space_object.draw_all()

        SPEEDLABEL = MAINFONT.render(f"X {s.SPEED_FACTORS[s.SPEED_INDEX]}",
                                     1, (0, 255, 255))
        screen.blit(SPEEDLABEL, (680, 20))

        p.display.update()
        clock.tick(s.FRAMERATE)


# Initialize class instances
def init_simulation():
    for i in range(len(s.STARTPOS)):  # len(s.STARTPOS)
        Space_object(screen, s.STARTPOS[i], s.MASS[i], s.OBJECT_IMG[i],
                     s.STARTVEL[i], trace_length=s.TRACE_LENGTH[i],
                     trace_time=s.TRACE_TIME[i])
    animation_loop()


menu.init_menu(p, screen, clock, init_simulation)
p.quit()
