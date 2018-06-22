import settings as s
import pygame
import time
pygame.init()

p = None
screen = None
clock = None

# SCHRIFTARTEN
Note = pygame.font.Font('freesansbold.ttf', 17)
smallText = pygame.font.Font('freesansbold.ttf', 25)
mediumText = pygame.font.Font('freesansbold.ttf', 43)
largeText = pygame.font.Font('freesansbold.ttf', 50)
FONT = pygame.font.Font(None, 32)

# BILDER
MainMenuimg = pygame.image.load('assets/MainMenu.jpg')
settingimg = pygame.image.load('assets/backgroundblack.jpg')
MenuParameterimg = pygame.image.load('assets/ConfMenu.jpg')


# Font of text
def text_objects(text, font):
    textSurface = font.render(text, True, s.white)
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
                s.MASS[0] = 2e30
                s.MASS[1] = 5.974e24
                s.MASS[2] = 6.419e23
                s.MASS[3] = 1.9e27
                s.MASS[4] = 5.685e26
                s.G = 6.674e-20
                s.TIME_STEP = 3600 * 24
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

        screen.fill(s.grey)
        button('Auto Launch', s.WIDTH/2 - 100, s.HEIGHT/2 -100, 200, 50, s.green, s.bright_green, 'launch')
        button('Manual Launch', s.WIDTH/2 - 100, s.HEIGHT/2, 200, 50, s.green, s.bright_green)

        p.display.update()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.text = text  # text wich is inputed
        self.color = s.c_i
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
            self.color = s.c_a if self.active else s.c_a
            # Action that occur if a key is pressed
        if event.type == p.KEYDOWN:
            if self.active:
                # Define which box_input is selected (mass of spaceship)
                """if event.key == p.K_RETURN and 450 + 140 > mouse[0] > 450 and 100 + 32 > mouse[1] > 100:
                    self.color = s.lime
                    s.spaceship = float(self.text)
                    print(s.spaceship)
                    
                if event.key == p.K_RETURN and 450 + 140 > mouse[0] > 450 and 160 + 32 > mouse[1] > 160:
                    self.color = s.lime
                    s.spaceship = float(self.text)
                    print(s.ss_acc)"""
            
                if event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 220 + 32 > mouse[1] > 220:
                    self.color = s.lime
                    s.MASS[0] = float(self.text)
                    print(s.MASS[0])
                    pygame.time.wait(100)
                    
                   
                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 280 + 32 > mouse[1] > 280:
                    self.color = s.lime
                    s.MASS[1] = float(self.text)
                    print(s.MASS[1])

                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 340 + 32 > mouse[1] > 340:
                    self.color = s.lime
                    s.G = float(self.text)
                    print(s.G)

                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 400 + 32 > mouse[1] > 400:
                    self.color = s.lime
                    s.TIME_STEP = float(self.text)
                    print(s.TIME_STEP)
            
                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 460 + 32 > mouse[1] > 460:
                    self.color = s.lime
                    s.MASS[2] = float(self.text)
                    print(s.MASS[2])

                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 520 + 32 > mouse[1] > 520:
                    self.color = s.lime
                    s.MASS[3] = float(self.text)
                    print(s.MASS[3])
                    
                elif event.key == p.K_RETURN and 450 + 300 > mouse[0] > 450 and 580 + 32 > mouse[1] > 580:
                    self.color = s.lime
                    s.MASS[4] = float(self.text)
                    print(s.MASS[4])
                    
                elif event.key == p.K_BACKSPACE:
                    main()
                elif event.key == p.K_COMMA:
                    self.text = self.text
                else:
                    self.text += event.unicode
                    
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                # convert text_input to float float(text)

    def update(self):
        # Resize the box if the text is too long.
        width = max(300, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rectangle
        p.draw.rect(screen, self.color, self.rect, 2)
        # Blit Default_Setting and Retrun buttons
        button('Default Setting', s.WIDTH/2 - 220, 650, 200, 50, s.yellow_launch, s.bright_yellow_launch, 'Default')
        button('Return', s.WIDTH/2 + 40, 650, 200, 50, s.yellow_launch, s.bright_yellow_launch, 'return')

#create InputsBoxes and possibility to change some variables
def main():

    i_b0 = InputBox(450, 100, 140, 32)
    i_b1 = InputBox(450, 160, 140, 32)
    i_b2 = InputBox(450, 220, 140, 32)
    i_b3 = InputBox(450, 280, 140, 32)
    i_b4 = InputBox(450, 340, 140, 32)
    i_b5 = InputBox(450, 400, 140, 32)
    i_b6 = InputBox(450, 460, 140, 32)
    i_b7 = InputBox(450, 520, 140, 32)
    i_b8 = InputBox(450, 580, 140, 32)
    i_b = [i_b0, i_b1, i_b2, i_b3, i_b4, i_b5,i_b6,i_b7, i_b8]

    screen.blit(settingimg, (0, 0))
    message_screen('Parameters',mediumText, s.WIDTH/2, 30)
    message_screen('After input press "Enter". Note that acceleration and mass of spaceship are invalid for yet',Note, 395, 64)
    message_screen('Valide inputs: 12 or 12.04 or 12e30, calculus are not supported',Note, 280, 81)
    message_screen('Mass of Space Ship',smallText, 320, 115)
    message_screen('Acceleration of Space Ship',smallText, 270, 175)
    message_screen('Mass of Sun',smallText, 360, 235)
    message_screen('Mass of Earth',smallText, 350, 295)
    message_screen('Constant of Gravitation',smallText, 290, 355)
    message_screen('Calculus Steps',smallText, 340, 415)
    message_screen('Mass of Mars',smallText, 340, 475)
    message_screen('Mass of Jupyter',smallText, 340, 535)
    message_screen('Mass of Saturn',smallText, 340, 595)

    enter = False
    while not enter:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                enter = True
            for box in i_b:
                box.write_input(event)
        for box in i_b:
            box.update()

        for box in i_b:
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

        button('setting', s.WIDTH/3 + 75, 460, 100, 50, s.yellow, s.bright_yellow, 'setting')
        button('start', s.WIDTH/3 - 50, 460, 100, 50, s.green, s.bright_green, 'play')
        button('quit', s.WIDTH/3 + 200, 460, 100, 50, s.red, s.bright_red, 'quit')

        pygame.display.update()
