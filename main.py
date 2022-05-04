import os
import pygame
import time

pygame.display.init()
pygame.mixer.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
FPS = 60

VEL = 5

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (187, 187, 187)
INACTIVE_TEXT_COLOR = GREY
COMIC_SANS = pygame.font.Font("comicsansms", 14)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pyHero")  # window title
pygame.mixer.music.load("songs/Guns N' Roses Sweet Child O' Mine l MP3.mp3")
pygame.mixer.music.play(-1)

# array of the note images (different colors, just select from array)
note_imgs = [pygame.image.load(os.path.join("imgs", "green note.png")),
             pygame.image.load(os.path.join("imgs", "red note.png")),
             pygame.image.load(os.path.join("imgs", "yellow note.png")),
             pygame.image.load(os.path.join("imgs", "blue note.png")),
             pygame.image.load(os.path.join("imgs", "orange note.png"))]


class Note:
    def __init__(self, color):
        if color == "green":
            self.x = WIDTH / 6
            self.y = HEIGHT / 2
            self.image = note_imgs[0]
        elif color == "red":
            self.x = WIDTH / 3
            self.y = HEIGHT / 2
            self.image = note_imgs[1]
        elif color == "yellow":
            self.x = WIDTH / 2
            self.y = HEIGHT / 2
            self.image = note_imgs[2]
        elif color == "blue":
            self.x = 2 * WIDTH / 3
            self.y = HEIGHT / 2
            self.image = note_imgs[3]
        elif color == "orange":
            self.x = 5 * WIDTH / 6
            self.y = HEIGHT / 2
            self.image = note_imgs[4]


class InputBox:

    def init(self, x1, y1, x2, y2):
        self.rect = pygame.Rect(x1, y1, x2, y2)
        self.text = ""
        self.color = INACTIVE_TEXT_COLOR


def draw_window():  # make a drawing function to easily display window
    screen.fill(BLUE)
    pygame.display.update()


def song_menu():

    start_time = round(time.time() * 1000)

    running = True
    while running:  # game loop
        clock.tick(FPS)
        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False

        elapsed = round(time.time() * 1000) - start_time  # elapsed run-time
        print(elapsed)

        draw_window()

    pygame.quit()


song_menu()
