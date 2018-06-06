# If you click setting, you have to click once on escape because there is a bug and the "Setting Scene" open twice.
#I didn't find the bug so if you want you can try. The bug is somewehre in class InputBoxes or in Setting_Screen()
import pygame as p
import time

usernam = input("Enter username: ")
color = input("Enter password: ")
if usernam == "***" and color == "qwdb44rrr_fhfhrtrh334535rfsdfsdfwrvwavadqwdvgbjun7mnu45v3v34b34 :)" :
   print('launching...')
else :
    print('retry')
p.init()

clock = p.time.Clock()

screen_width = 600
screen_height = 600

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


COLOR_INACTIVE = p.Color('lightskyblue3')
COLOR_ACTIVE = p.Color('dodgerblue2')
FONT = p.font.Font(None, 32)

MainMenuimg = p.image.load('MainMenu.jpg')
settingimg = p.image.load('setting.jpg')
MenuParameterimg = p.image.load('ConfMenu.jpg')
screen = p.display.set_mode((screen_width, screen_height))
p.display.set_caption('Sonde Simulation')
clock = p.time.Clock()

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
        if click[0] == 1 and action != None: #click [0] = left click
            if action == "play":
                parameter_loop()
            elif action == "quit":
                p.quit()
                quit()
            elif action == "setting":
                setting_screen()
            elif action == "Default":
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
        TextRect.center = ((screen_width/2), (screen_height/2))
        screen.blit(TextSurf, TextRect)

        button('setting', 250, 460, 100, 50, yellow, bright_yellow, 'setting')
        button('start', 100, 460, 100, 50, green, bright_green, 'play')
        button('quit', 400, 460, 100, 50, red, bright_red, 'quit')

        p.display.update()

def setting_screen():

    main()
    setting_exit = False

    while not setting_exit:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                run = True
                p.quit()
                quit()

        p.display.update()

def parameter_loop():

    para_exit = False

    while not para_exit:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                run = True
                p.quit()
                quit()

        screen.fill(grey)
        button('Auto Launch', screen_width/2 - 100, screen_height/2 -100, 200, 50, green, bright_green)
        button('Manual Launch', screen_width/2 - 100 , screen_height/2, 200, 50, green, bright_green)

        p.display.update()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text  #text input
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == p.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
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
        button('Default Setting', screen_width/2 - 100, 500, 200, 50, yellow_launch, bright_yellow_launch, 'Default')

def main():
    clock = p.time.Clock()
    input_box1 = InputBox(300, 100, 140, 32)
    input_box2 = InputBox(300, 160, 140, 32)
    input_box3 = InputBox(300, 220, 140, 32)
    input_box4 = InputBox(300, 280, 140, 32)
    input_box5 = InputBox(300, 340, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]
    done = False

    while not done:
        for event in p.event.get():
            if event.type == p.QUIT or event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
                done = True
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()

        screen.blit(settingimg, (0,0))
        message_screen('Parameters',mediumText, screen_width/2, 30)
        message_screen('Mass of Space Ship',smallText, 200, 115)
        message_screen('Acceleration of Space Ship',smallText, 160, 175)
        message_screen('Mass of Sun',smallText, 227, 235)
        message_screen('Mass of Earth',smallText, 220, 295)
        message_screen('Constant of Gravitation',smallText, 170, 355)
        for box in input_boxes:
            box.draw(screen)

        p.display.flip()
        clock.tick(30)

"""def game_loop():  Waiting game_script

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
