import settings as s
import pygame
pygame.init()

p = None
screen = None
clock = None

# SCHRIFTARTEN
smallText = pygame.font.Font('freesansbold.ttf', 25)
mediumText = pygame.font.Font('freesansbold.ttf', 43)
largeText = pygame.font.Font('freesansbold.ttf', 50)
FONT = pygame.font.Font(None, 32)

# PYGAME FARBEN
c_i = pygame.Color('lightskyblue3')
c_a = pygame.Color('dodgerblue2')
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

# BILDER
MainMenuimg = pygame.image.load('assets/MainMenu.jpg')
settingimg = pygame.image.load('assets/backgroundblack.jpg')
MenuParameterimg = pygame.image.load('assets/ConfMenu.jpg')


# Font of text
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


# draw a rectangle around the text and with the text
def message_screen(text, text_size, widht, height):
    TextSurf, TextRect = text_objects(text, text_size)
    TextRect.center = ((widht), (height))
    screen.blit(TextSurf, TextRect)

    p.display.update()


# Define an action if a button is pressed
def button(message, x, y, w, h, ic, ac, action=None):  # x,y = coord. w=width, h= height, ic=inactive color ac=active color
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()
    # Define if the mouse is in a rectangle's button
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # mouse [0] = x-coordinate of the mouse
        p.draw.rect(screen, ac, (x, y, w, h))  # create active button
        if click[0] == 1 and action is not None:  # click[0] = left click
            if action == "play":
                parameter_loop()
            elif action == "launch":
                init_simulation(s)
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
     # if the mouse isn't in a rectangle, the color will change
    else:
        p.draw.rect(screen, ic, (x, y, w, h))

    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x+(w/2)), ((y+(h/2))))
    screen.blit(textSurf, textRect)

# Define Launch Menu to begin the simulation
def parameter_loop():

    para_exit = False

    while not para_exit:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                para_exit = True
                p.quit()
                quit()

        screen.fill(grey)
        button('Auto Launch', s.WIDTH/2 - 100, s.HEIGHT/2 -100, 200, 50, green, bright_green, 'launch')
        button('Manual Launch', s.WIDTH/2 - 100, s.HEIGHT/2, 200, 50, green, bright_green)

        p.display.update()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = c_i
        self.text = text  # text wich is inputed
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def write_input(self, event):
        mouse = p.mouse.get_pos()
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
                    # Define which box_input is selected
                    if 450 + 140 > mouse[0] > 450 and 100 + 32 > mouse[1] > 100:
                        s.MASS[0] = float(self.text)
                    # Define which box_input is selected
                    elif 450 + 140 > mouse[0] > 450 and 160 + 32 > mouse[1] > 160:
                        s.MASS[1] = float(self.text)
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
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rectangle
        p.draw.rect(screen, self.color, self.rect, 2)
        # Blit Default_Setting and Retrun buttons
        button('Default Setting', s.WIDTH/2 - 220, 500, 200, 50, yellow_launch, bright_yellow_launch, 'Default')
        button('Return', s.WIDTH/2 + 40, 500, 200, 50, yellow_launch, bright_yellow_launch, 'return')

#create InputsBoxes and possibility to change some variables
def main():

    input_box1 = InputBox(450, 100, 140, 32)
    input_box2 = InputBox(450, 160, 140, 32)
    input_box3 = InputBox(450, 220, 140, 32)
    input_box4 = InputBox(450, 280, 140, 32)
    input_box5 = InputBox(450, 340, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

    enter = False
    screen.blit(settingimg, (0, 0))
    message_screen('Parameters',mediumText, s.WIDTH/2, 30)
    message_screen('Mass of Space Ship',smallText, 320, 115)
    message_screen('Acceleration of Space Ship',smallText, 270, 175)
    message_screen('Mass of Sun',smallText, 360, 235)
    message_screen('Mass of Earth',smallText, 350, 295)
    message_screen('Delta T [s]',smallText, 370, 355)

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


# # # # # # # # # #
# START FUNCTION  #
# # # # # # # # # #
def init_menu(main_p, main_screen, main_clock, main_simulation):
    global p
    p = main_p
    global screen
    screen = main_screen
    global clock
    clock = main_clock
    global init_simulation
    init_simulation = main_simulation

    game_intro()


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                p.quit()
                quit()

        screen.blit(MainMenuimg, (0, 0))
        TextSurf, TextRect = text_objects('Main Menu', largeText)
        TextRect.center = ((s.WIDTH/2), (s.HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button('setting', s.WIDTH/3 + 75, 460, 100, 50, yellow, bright_yellow, 'setting')
        button('start', s.WIDTH/3 - 50, 460, 100, 50, green, bright_green, 'play')
        button('quit', s.WIDTH/3 + 200, 460, 100, 50, red, bright_red, 'quit')

        pygame.display.update()
