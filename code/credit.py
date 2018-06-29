import pygame
from pygame.locals import *
from tkinter import *
from random import *
import settings as s

pygame.init()
pygame.display.set_caption('credits')
screen = pygame.display.set_mode((800, 600))
screen_r = screen.get_rect()
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

def game():
    def do_event(event):
        print("{},{}".format(event.x,event.y))

    def jump(event):
        app.hello_b.place(relx=random(),rely=random())

    class App:
        def __init__(self,master):
            frame = Frame(master)
            master.geometry("800x800")
            master.title("Quit the programm please !")
            master.bind("<Button-1>",do_event)
            master.bind("<Button-1>",do_event)
            frame.pack()

            self.hello_b = Button(master,text="Quit",command=sys.exit)
            self.hello_b.bind("<Enter>",jump)
            self.hello_b.pack()

    root = Tk()

    app = App(root)

    root.mainloop()

def credit():

    credit_list = ["The Simulation"," ","Directed by:","Herr Kambor and Herr Keller","", "Created by:","","Amin","Joel","Simon","","","","","","","","You wait until the end nice","Wait a bit..","","","","","","ps: It's possible to quit the programme"]
    texts = []
    # Render the text
    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (10, 10, 10))
        # Create a Rect for each Surface.
        r = s.get_rect(centerx = screen_r.centerx, y = screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.fill((180,180,180))

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            screen.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            game()
            return

        pygame.display.flip()

        #framerate at 60 FPS
        clock.tick(170)


    credit()
