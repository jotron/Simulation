import pygame as p
import time

clock = p.time.Clock()
SIZE = WIDTH, HEIGHT = 800, 800

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

smallText = p.font.Font('freesansbold.ttf', 20)
mediumText = p.font.Font('freesansbold.ttf', 33)
largeText = p.font.Font('freesansbold.ttf', 40)


c_i = p.Color('lightskyblue3')
c_a = p.Color('dodgerblue2')
FONT = p.font.Font(None, 32)

MainMenuimg = p.image.load('MainMenu.jpg')
settingimg = p.image.load('setting.jpg')
MenuParameterimg = p.image.load('ConfMenu.jpg')
screen = p.display.set_mode((WIDTH, HEIGHT))


# Font of text
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

# draw a rectangle around the text and with the text
def message_screen(text, text_size ,widht, height):
     TextSurf, TextRect = text_objects(text, text_size)
     TextRect.center = ((widht), (height))
     screen.blit(TextSurf, TextRect)

     p.display.update()

# Define an action if a button is pressed
def button(message, x, y, w, h, ic, ac, action=None): #x,y = coord. w=width, h= height, ic=inactive color ac=active color
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()
                                                       # mouse [0] = x-coordinate of the mouse
    if x + w > mouse [0] > x and y + h > mouse[1] > y: # Delimit the button field
        p.draw.rect(screen, ac, (x, y, w, h)) #create an active button
        if click[0] == 1 and action != None: #click[0] = left click
            if action == "play":
                parameter_loop()
            elif action == "quit":
                p.quit()
                quit()
            #elif action == "launch":
             #   init_class() # it's a class in main()
            elif action == "setting":
                main()
            elif action == "return":
                game_intro()
            elif action == "Default":
                msonde_t0 = 3038 * 10**3 # Take-off weight of the probe
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

        button('setting', 250, 460, 100, 50, yellow, bright_yellow, 'setting')
        button('start', 100, 460, 100, 50, green, bright_green, 'play')
        button('quit', 400, 460, 100, 50, red, bright_red, 'quit')

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
            # Action that occur if return key is pressed
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
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        p.draw.rect(screen, self.color, self.rect, 2)
        # Blit Default_Setting button
        button('Default Setting', WIDTH/2 - 220, 500, 200, 50, yellow_launch, bright_yellow_launch, 'Default')
        button('Return', WIDTH/2 + 40, 500, 200, 50, yellow_launch, bright_yellow_launch, 'return')

def main():

    input_box1 = InputBox(300, 100, 140, 32)
    input_box2 = InputBox(300, 160, 140, 32)
    input_box3 = InputBox(300, 220, 140, 32)
    input_box4 = InputBox(300, 280, 140, 32)
    input_box5 = InputBox(300, 340, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

    enter = False

    while not enter:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                enter = True
            for box in input_boxes:
                box.write_input(event)
        for box in input_boxes:
            box.update()

        screen.blit(settingimg, (0,0))
        message_screen('Parameters',mediumText, WIDTH/2, 30)
        message_screen('Mass of Space Ship',smallText, 200, 115)
        message_screen('Acceleration of Space Ship',smallText, 160, 175)
        message_screen('Mass of Sun',smallText, 227, 235)
        message_screen('Mass of Earth',smallText, 220, 295)
        message_screen('Constant of Gravitation',smallText, 170, 355)
        for box in input_boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(12)

"""def game_loop():

    game_loop = False

    while not game_loop:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                run = True
                p.quit()
                quit()

        p.display.update()"""

game_intro()
p.quit()
quit()
