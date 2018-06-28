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
MAINFONT = p.font.Font("assets/font.ttf", 20)
obj_font = p.font.Font("assets/font.ttf", 15)


# Class for all objects with mass
class Space_object:
    space_objects = []
    step_accumulation = 0.0
    center_index = 0

    def __init__(self, screen, pos, mass,
                 vel=np.zeros(2),
                 trace_color=(180, 180, 180),
                 trace_length=100, trace_time=3600*24*365):

        self.screen = screen
        self.pos = pos
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

    # Get next position and velocity
    @classmethod
    def get_next_state(cls, AWP, dt):

        # DGL for N-Objects
        def DGL(pos):
            G = s.G  # in km
            a = np.zeros_like(pos)

            # rocket
            if space_shuttle.on:
                a[-1] += space_shuttle.get_acc()

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

            print(a[-1], space_shuttle.get_acc())
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
            # # # # #
            # TRACE #
            # # # # #

            # store position for one year
            space_object1.trace_accumulation += s.SPEED_FACTORS[s.SPEED_INDEX] / s.FRAMERATE
            trace_step = (space_object1.trace_time) / space_object1.trace_length
            for i in range(int(space_object1.trace_accumulation / trace_step)):
                space_object1.trace[space_object1.trace_index % space_object1.trace_length] = space_object1.pos
                space_object1.trace_index += 1
            space_object1.trace_accumulation = space_object1.trace_accumulation % trace_step

            # draw trace
            rolled_trace = np.roll(space_object1.trace, -space_object1.trace_index, 0)
            trace_list = space_object1.convert(rolled_trace).tolist()
            p.draw.aalines(space_object1.screen, space_object1.trace_color, False, trace_list, 1)

            space_object1.draw()

    # Change center point
    @classmethod
    def centerclick(cls, click):
        for i, so in enumerate(Space_object.space_objects):
            # rect = so.img.get_rect(center=Space_object.convert(so.pos))
            rect = so.rect
            if rect.collidepoint(click):
                s.CENTER_INDEX = i

    # Draw all space_objects
    @classmethod
    def convert(self, pos):
        # Am Anfang ist die Sonne im Zenter bzw. die Anfangskoordinate der Sonne
        center_pos = self.space_objects[s.CENTER_INDEX].pos
        # Alles zum Ursprung Sonne verschieben und dann skalieren
        resourced_pos = (pos - center_pos) * s.ZOOM_FACTOR
        # Zurückverschieben
        tmp_pos = (resourced_pos + s.v_center) / s.V_SIZE * s.SIZE
        return tmp_pos.round().astype(int)


# Class for Spaceship
class space_shuttle_class(Space_object):
    def __init__(self, screen, earth_index, mass, force, img,
                 ss_factor=(1/7)):
        # init space_object
        Space_object.__init__(self, screen, self.initpos(earth_index),
                              mass, self.initvel(earth_index),
                              trace_time=24*3600*400,
                              trace_length=500)

        # specific space shuttle properties
        self.rect = None
        self.a = force / mass
        self.theta = 0
        self.on = False

        # smallet image of space_shuttle
        size = img.get_size()
        self.img_original = p.transform.scale(img, (int(size[0] * ss_factor),
                                              int(size[1] * ss_factor)))
        self.img = self.img_original

    def initpos(self, earth_index):
        e = Space_object.space_objects[earth_index]
        pos = e.pos + np.array([0, -42164])
        return pos

    def initvel(self, earth_index):
        e = Space_object.space_objects[earth_index]
        return e.vel + np.array([3.074, 0])

    def draw(self):
        self.rect = self.img.get_rect(center=self.convert(self.pos).tolist())
        self.screen.blit(self.img, self.rect)

    def get_acc(self):
        acc = np.array([0, -self.a])
        cos, sin = np.cos(self.theta), np.sin(self.theta)
        rotation_matrix = np.array([[cos, -sin], [sin, cos]])
        return np.dot(rotation_matrix, acc)

    def rotate(self, right):
        angle_rad = np.pi / 10.
        if right:
            self.theta += angle_rad
        else:
            self.theta -= angle_rad
        theta_degree = self.theta * (180.0 / np.pi)
        self.img = p.transform.rotate(self.img_original, -theta_degree)


class planet(Space_object):
    def __init__(self, screen, name, pos, mass, radius, color,
                 vel=np.zeros(2),
                 trace_color=(180, 180, 180),
                 trace_length=100, trace_time=3600*24*365):

        Space_object.__init__(self, screen, pos, mass,
                              vel,
                              trace_color,
                              trace_length,
                              trace_time)

        # specific planet properties
        self.rect = None
        self.radius = radius
        self.color = color
        self.name = obj_font.render(name, 1, (0, 255, 255))

    def draw(self):
        # draw shape
        rad = int(round(self.radius * s.ZOOM_FACTOR / s.V_WIDTH * s.WIDTH))
        rad = max(rad, 3)
        pos = self.convert(self.pos).tolist()
        self.rect = p.draw.circle(self.screen, self.color,
                                  pos, rad)

        # Draw name of planet
        texpos = (pos[0] + 5, pos[1] - 5)
        screen.blit(self.name, texpos)


# ANIMATION LOOP #
def animation_loop():
    while 1:
        for event in p.event.get():
            # QUIT
            if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
                sys.exit()
            # SET SPEED
            if event.type == p.KEYUP:

                # Increase and Decrease Speed
                if (event.key == p.K_UP and s.SPEED_INDEX < len(s.SPEED_FACTORS) - 1):
                    s.SPEED_INDEX += 1
                if (event.key == p.K_DOWN and s.SPEED_INDEX >= 1):
                    s.SPEED_INDEX -= 1

                # Increase Zoom factor => press shift and 1 simultaneously
                if (event.key == p.K_p and s.ZOOM_FACTOR <= 2**18):
                    s.ZOOM_FACTOR *= 2
                if (event.key == p.K_m and s.ZOOM_FACTOR >= 0.2):
                    s.ZOOM_FACTOR /= 2

                # Space shuttle off
                if (event.key == p.K_SPACE):
                    space_shuttle.on = False

                # Change direction of Space Shuttle
                if (event.key == p.K_RIGHT):
                    space_shuttle.rotate(True)
                if (event.key == p.K_LEFT):
                    space_shuttle.rotate(False)

            # Space Shuttle on
            if event.type == p.KEYDOWN:
                if (event.key == p.K_SPACE):
                    space_shuttle.on = True

            # Change view center
            if event.type == p.MOUSEBUTTONDOWN:
                Space_object.centerclick(event.pos)

        # Nice Background
        screen.blit(background_image, [0, 0])

        # Do Gravition Stuff
        Space_object.run_all()
        Space_object.draw_all()

        space_shuttle.draw()

        # Speed and Zoom
        SPEEDLABEL = MAINFONT.render("X {}".format(s.SPEED_FACTORS[s.SPEED_INDEX]),
                                     1, (0, 255, 255))
        ZOOMLABEL = MAINFONT.render("X {}".format(s.ZOOM_FACTOR),
                                    1, (0, 255, 255))
        screen.blit(SPEEDLABEL, (10, 20))
        screen.blit(ZOOMLABEL, (10, 40))

        ROCKET = MAINFONT.render("R {}, {}".format(space_shuttle.on,
                                 space_shuttle.theta * (180.0 / np.pi)),
                                 1, (0, 255, 255))
        screen.blit(ROCKET, (600, 20))

        p.display.update()
        clock.tick(s.FRAMERATE)


# Initialize class instances
def init_simulation(settings_menu=s):
    # Change variable constans
    global s
    s = settings_menu

    for i in range(len(s.STARTPOS)):  # len(s.STARTPOS)
        planet(screen, s.NAME[i], s.STARTPOS[i], s.MASS[i], s.RADIUS[i],
               s.COLOR[i],
               s.STARTVEL[i],
               (180, 180, 180),
               s.TRACE_LENGTH[i],
               s.TRACE_TIME[i])

    global space_shuttle
    space_shuttle = space_shuttle_class(screen, 1, s.ss_m, s.ss_f, s.ss_img)
    animation_loop()


menu.init_menu(p, screen, clock, init_simulation)
p.quit()
