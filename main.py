import os
import pygame
import time

pygame.display.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("pyHero")  # window title

RED_IMG = pygame.image.load(os.path.join("imgs", "red note.png"))


class Note:
    image = RED_IMG

    def __init__(self, color):
        if color == "red":
            self.x = 150
            self.y = 100




while True:
    for event in pygame.event.get():  # to exit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    redNote = Note("red")