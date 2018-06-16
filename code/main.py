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


def message_screen(text, text_size, widht, height):
    TextSurf, TextRect = menu.text_objects(text, text_size)
    TextRect.center = ((widht), (height))
    screen.blit(TextSurf, TextRect)

    p.display.update()


def button(message, x, y, w, h, ic, ac, action=None):  # x,y = coord. w=width, h= height, ic=inactive color ac=active color
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()
    # mouse [0] = x coord of mouse because python recognise mouse coordinates
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # if x coordinate (button) + width (button) delimite boutton
        p.draw.rect(screen, ac, (x, y, w, h))  # create active button
        if click[0] == 1 and action is not None:  # click[0] = left click
            if action == "play":
                parameter_loop()
            elif action == "launch":
                init_class()
            elif action == "quit":
                p.quit()
                quit()
            elif action == "setting":
                main()
            elif action == "return":
                game_intro()
            elif action == "Default":
                msonde_t0 = 3038 * 10**3
                msonde_t1 = msonde_t0 - 2286 * 10**3  # After 150sec
                msonde_t2 = msonde_t1 - 464 * 10**3   # After 360sec
                msonde_t3 = msonde_t2 - 114 * 10**3   # After 500sec   source(nasa.wikibis.com)
                msun = 1.989 * 10**30
                mearth = 5.972 * 10**24
                G = 6.67234 * 10**(-11)
                parameter_loop()

    else:
        p.draw.rect(screen, ic, (x, y, w, h))

    textSurf, textRect = menu.text_objects(message, menu.smallText)
    textRect.center = ((x+(w/2)), ((y+(h/2))))
    screen.blit(textSurf, textRect)


def game_intro():

    intro = True

    while intro:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

        screen.blit(menu.MainMenuimg, (0, 0))
        TextSurf, TextRect = menu.text_objects('Main Menu', menu.largeText)
        TextRect.center = ((s.WIDTH/2), (s.HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button('setting', s.WIDTH/3 + 75, 460, 100, 50, s.yellow, s.bright_yellow, 'setting')
        button('start', s.WIDTH/3 - 50, 460, 100, 50, s.green, s.bright_green, 'play')
        button('quit', s.WIDTH/3 + 200, 460, 100, 50, s.red, s.bright_red, 'quit')

        p.display.update()


def parameter_loop():

    para_exit = False

    while not para_exit:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                para_exit = True
                p.quit()
                quit()

        screen.fill(s.grey)
        button('Auto Launch', s.WIDTH/2 - 100, s.HEIGHT/2 -100, 200, 50, s.green, s.bright_green, 'launch')
        button('Manual Launch', s.WIDTH/2 - 100, s.HEIGHT/2, 200, 50, s.green, s.bright_green)

        p.display.update()


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = menu.c_i
        self.text = text  # text input
        self.txt_surface = menu.FONT.render(text, True, self.color)
        self.active = False

    def write_input(self, event):
        if event.type == p.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = menu.c_a if self.active else menu.c_a
            # Action that occur if a key is pressed
        if event.type == p.KEYDOWN:
            if self.active:
                if event.key == p.K_RETURN:
                    self.color = lime
                elif event.key == p.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == p.K_COMMA:
                    self.text = self.text
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = menu.FONT.render(self.text, True, self.color)
                # convert text_input to float float(text)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+8)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        p.draw.rect(screen, self.color, self.rect, 2)
        # Blit Default_Setting button
        button('Default Setting', s.WIDTH/2 - 220, 500, 200, 50, s.yellow_launch, s.bright_yellow_launch, 'Default')
        button('Return', s.HEIGHT/2 + 40, 500, 200, 50, s.yellow_launch, s.bright_yellow_launch, 'return')


def main():

    input_box1 = InputBox(400, 100, 140, 32)
    input_box2 = InputBox(400, 160, 140, 32)
    input_box3 = InputBox(400, 220, 140, 32)
    input_box4 = InputBox(400, 280, 140, 32)
    input_box5 = InputBox(400, 340, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
    screen.blit(menu.settingimg, (0, 0))
    message_screen('Parameters', menu.mediumText, s.WIDTH/2, 30)
    message_screen('Mass of Space Ship', menu.smallText, 245, 115)
    message_screen('Acceleration of Space Ship', menu.smallText, 195, 175)
    message_screen('Mass of Sun', menu.smallText, 285, 235)
    message_screen('Mass of Earth', menu.smallText, 280, 295)
    message_screen('Constant of Gravitation', menu.smallText, 220, 355)

    enter = False

    while not enter:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                enter = True
            for box in input_boxes:
                box.write_input(event)
        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(60)


# Class for all objects with mass
class Space_object:
    space_objects = []
    step_accumulation = 0.0
    trace_accumulation = 0.0

    def __init__(self, screen, pos, img, mass=5.9*10**24,
                 vel=np.zeros(2),
                 trace_color=(180, 180, 180)):
        self.screen = screen
        self.pos = pos
        self.img = img
        self.mass = mass
        self.vel = vel

        self.trace_color = trace_color
        self.trace_true = np.tile(pos, (s.TRACE_LENGTH, 1))
        self.trace_index = 0

        self.space_objects.append(self)

    # Change Position and Velocity
    def change_state(self, pos, vel):
        self.pos = pos
        self.vel = vel

    # Draw Space Object
    def draw(self, trace_accumulation):
        # store position for one year
        trace_step = (365*24*3600) / s.TRACE_LENGTH
        for i in range(int(trace_accumulation / trace_step)):
            self.trace_true[self.trace_index % s.TRACE_LENGTH] = self.pos
            self.trace_index += 1

        # draw trace
        rolled_trace = np.roll(self.trace_true, -self.trace_index, 0)
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

        # set trace accumulation
        cls.trace_accumulation += s.SPEED_FACTORS[s.SPEED_INDEX] / s.FRAMERATE

    # Draw all space_objects
    @classmethod
    def draw_all(cls):
        for space_object1 in cls.space_objects:
            space_object1.draw(cls.trace_accumulation)

        # reset trace_accumulation
        trace_step = (365*24*3600) / s.TRACE_LENGTH
        cls.trace_accumulation = cls.trace_accumulation % trace_step

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
def init_class():
    for i in range(len(s.STARTPOS)):
        Space_object(screen, s.STARTPOS[i], s.OBJECT_IMG[i], s.MASS[i],
                     s.STARTVEL[i])
    animation_loop()


game_intro()
p.quit()
quit()
