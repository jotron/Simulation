import pygame as p
import numpy as np
import sys
import time

# General Settings
TIME_STEP = 3 * 24 * 3600 * 2
FRAMERATE = 45
TRACELENGTH = 50
V_SIZE = V_WIDTH, V_HEIGHT = 3.5e9, 3.5e9  # Total size of System = 3e9km
v_center = np.array([V_WIDTH/2, V_HEIGHT/2])
SIZE = WIDTH, HEIGHT = 800, 800

# pygame initalisation
p.init()
p.display.set_caption('Simulation')
screen = p.display.set_mode(SIZE)  # Fenstergrösse festlegen
clock = p.time.Clock()  # Brauchen wir zur Framerate-Kontrolle

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
yellow_launch = (245,222,179)
bright_yellow_launch = (255,235,205)
lime = (0, 255, 0)
grey = (30,30,30)

smallText = p.font.Font('freesansbold.ttf', 25)
mediumText = p.font.Font('freesansbold.ttf', 43)
largeText = p.font.Font('freesansbold.ttf', 50)


c_i = p.Color('lightskyblue3')
c_a = p.Color('dodgerblue2')
FONT = p.font.Font(None, 32)

MainMenuimg = p.image.load('MainMenu.jpg')
settingimg = p.image.load('setting.jpg')
MenuParameterimg = p.image.load('ConfMenu.jpg')
screen = p.display.set_mode((WIDTH, HEIGHT))

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_screen(text, text_size ,widht, height):
     TextSurf, TextRect = text_objects(text, text_size)
     TextRect.center = ((widht), (height)) #creer rectangle autour texte
     screen.blit(TextSurf, TextRect)

     p.display.update()

def button(message, x, y, w, h, ic, ac, action=None): #x,y = coord. w=width, h= height, ic=inactive color ac=active color
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()
# mouse [0] = x coord of mouse because python recognise mouse coordinates
    if x + w > mouse [0] > x and y + h > mouse[1] > y: #if x coordinate (button) + width (button) delimite boutton
        p.draw.rect(screen, ac, (x, y, w, h)) #create active button
        if click[0] == 1 and action != None: #click[0] = left click
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
                msonde_t1 = msonde_t0 - 2286 * 10**3 # After 150sec
                msonde_t2 = msonde_t1 - 464 * 10**3   # After 360sec
                msonde_t3 = msonde_t2 - 114 * 10**3   # After 500sec   source(nasa.wikibis.com)
                msun = 1.989 * 10**30
                mearth = 5.972 * 10**24
                G = 6.67234 * 10**(-11)
                parameter_loop()


    else:
        p.draw.rect(screen, ic, (x, y, w, h))

    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ( (x+(w/2)), ((y+(h/2))) )
    screen.blit(textSurf, textRect)

def game_intro():

    intro = True

    while intro:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

        screen.blit(MainMenuimg, (0,0))
        TextSurf, TextRect = text_objects('Main Menu', largeText)
        TextRect.center = ((WIDTH/2), (HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button('setting', WIDTH/3 + 75, 460, 100, 50, yellow, bright_yellow, 'setting')
        button('start', WIDTH/3 - 50, 460, 100, 50, green, bright_green, 'play')
        button('quit', WIDTH/3 + 200, 460, 100, 50, red, bright_red, 'quit')

        p.display.update()

def parameter_loop():

    para_exit = False

    while not para_exit:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                para_exit = True
                p.quit()
                quit()

        screen.fill(grey)
        button('Auto Launch', WIDTH/2 - 100, HEIGHT/2 -100, 200, 50, green, bright_green, 'launch')
        button('Manual Launch', WIDTH/2 - 100 , HEIGHT/2, 200, 50, green, bright_green)

        p.display.update()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = c_i
        self.text = text  #text input
        self.txt_surface = FONT.render(text, True, self.color)
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
            self.color = c_a if self.active else c_a
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
                self.txt_surface = FONT.render(self.text, True, self.color)
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
        button('Default Setting', WIDTH/2 - 220, 500, 200, 50, yellow_launch, bright_yellow_launch, 'Default')
        button('Return', HEIGHT/2 + 40, 500, 200, 50, yellow_launch, bright_yellow_launch, 'return')

def main():

    input_box1 = InputBox(400, 100, 140, 32)
    input_box2 = InputBox(400, 160, 140, 32)
    input_box3 = InputBox(400, 220, 140, 32)
    input_box4 = InputBox(400, 280, 140, 32)
    input_box5 = InputBox(400, 340, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
    screen.blit(settingimg, (0,0))
    message_screen('Parameters',mediumText, WIDTH/2, 30)
    message_screen('Mass of Space Ship',smallText, 245, 115)
    message_screen('Acceleration of Space Ship',smallText, 195, 175)
    message_screen('Mass of Sun',smallText, 285, 235)
    message_screen('Mass of Earth',smallText, 280, 295)
    message_screen('Constant of Gravitation',smallText, 220, 355)
    
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

# Space_object Constants
STARTPOS = [v_center,                             # Sun
            v_center + np.array([0, 15.21e7]),    # Earth
            v_center + np.array([0, 24.99e7]),    # Mars
            v_center + np.array([0, 81.9e7]),     # Jupyter
            v_center + np.array([0, 15.1857e8])]  # Saturn
STARTVEL = [np.array([0, 0]),      # Sun
            np.array([29.29, 0]),  # Earth
            np.array([21.97, 0]),  # Mars
            np.array([13.17, 0]),  # Jupyter
            np.array([9.2, 0])]    # Saturn
MASS = [2e30, 5.974e24, 6.419e23, 1.9e27, 5.685e26]
COLOR = [(255, 255, 0),    # Sun = Yellow
         (0, 0, 255),      # Earth = Blue
         (255, 0, 0),      # Mars = Red
         (153, 102, 51),   # Jupyter = Brown
         (140, 140, 140)]  # Saturn = Grey
RADIUS = [10, 5, 3, 8, 9]


# background_image
background_image = p.image.load("background.jpg").convert()


# Class for all objects with mass
class Space_object:
    space_objects = []

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

        self.space_objects.append(self)

    # Change Position and Velocity
    def change_state(self, pos, vel):
        self.pos = pos
        self.vel = vel

    # Draw Space Object
    def draw(self):
        # every half second store trace
        #  self.counter += 1
        #  if (self.counter >= FRAMERATE/2):
        #    self.counter = 0
        #    self.trace[:-1] = self.trace[1:]
        #    self.trace[-1] = self.pos
        p.draw.circle(self.screen, self.color,
                      self.convert(self.pos), self.radius)

    # Draw trace behind Space object
    def draw_trace(self):
        tuple_list = list(map(self.convert, self.trace))
        p.draw.aalines(self.screen, self.trace_color, True, tuple_list, 1)

    # Get next position and velocity
    @classmethod
    def get_next_state(cls):

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

        # DT
        dt = TIME_STEP
        # AWP
        AWP = np.array([[space_object1.pos for space_object1
                       in cls.space_objects],
                       [space_object1.vel for space_object1
                       in cls.space_objects]])

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
        # Runge Kutta with physics
        rk = Space_object.get_next_state()
        # Apply to all ojects as tupple
        for i, space_object1 in enumerate(cls.space_objects):
            next_pos = rk[0][i]
            next_vel = rk[1][i]
            space_object1.change_state(next_pos, next_vel)

    # Draw all space_objects
    @classmethod
    def draw_all(cls):
        for space_object1 in cls.space_objects:
            space_object1.draw()
            #  space_object1.draw_trace_converted()

    # Draw all space_objects
    @staticmethod
    def convert(pos):
        tmp_pos = pos / V_SIZE * SIZE
        #  print(pos, tmp_pos, tuple(tmp_pos.astype(int)))
        return tuple(tmp_pos.astype(int))

# ANIMATION LOOP #
def animation_loop():
    while 1:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                sys.exit()

        # Nice Background
        screen.blit(background_image, [0, 0])

        # Do Gravition Stuff
        Space_object.run_all()
        Space_object.draw_all()

        p.display.update()
        clock.tick(FRAMERATE)

# Initialize class instances
def init_class():
    for i in range(len(STARTPOS)):
        Space_object(screen, STARTPOS[i], RADIUS[i], MASS[i], STARTVEL[i], COLOR[i])
    animation_loop()

game_intro()
p.quit()
quit()
