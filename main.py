import os
import pygame
import time

pygame.display.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pyHero")  # window title


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


notes = [Note("green"),
         Note("red"),
         Note("yellow"),
         Note("blue"),
         Note("orange")]


def draw_window():  # make a drawing function to easily display window
    screen.fill(WHITE)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    start_time = round(time.time() * 1000)

    running = True
    while running:  # game loop
        clock.tick(FPS)

        elapsed = round(time.time() * 1000) - start_time  # elapsed run-time
        print(elapsed)

        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False

        draw_window()

    pygame.quit()


main()
