import os
import pygame

pygame.display.init()

WIDTH = 800
HEIGHT = 600
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pyHero")  # window title
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # a group of all the sprites on-screen

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

    def draw(self, screen):  # function to draw itself on the screen; easy to call
        self.rect = self.image.get_rect()
        screen.blit(self.image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


def draw_window(screen, notes):
    screen.fill("white")
    for note in notes:  # there are multiple notes to draw on the screen
        note.draw(screen)

    pygame.display.update()


notes = [Note("green"),
         Note("red"),
         Note("yellow"),
         Note("blue"),
         Note("orange")]

running = True
while running:  # game loop
    clock.tick(FPS)

    for event in pygame.event.get():  # to exit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw_window(screen, notes)
