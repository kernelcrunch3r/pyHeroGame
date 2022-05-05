import os
import pygame
import time


# function used to open a created song txt file and transition all the lines into a list of lists
# copied from musicPlayer.py
def song_read(name):
    with open("song txts/{}.txt".format(name)) as file:  # open the input's file and put the lines into a list
        n = list(file.read().split("\n"))  # get each note and its time in an element of an array
        print(n)
        file.close()

    notes = []
    for note in n:
        note = note.split()  # split each note into its own list of its symbol and the time pressed
        notes.append(note)  # add the 'mini' list to full notes list

    notes.pop(len(notes) - 1)  # there is always a blank space at the end

    for i in range(len(notes)):
        notes[i][1] = int(notes[i][1])  # the level creator has already rounded the time into an integer but in a string

    print(notes)
    return notes


pygame.display.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
FPS = 60

VEL = 5

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (187, 187, 187)

BASE_FONT = pygame.font.Font(None, 32)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pyHero")  # window title


# array of the note images (different colors, just select from array)
NOTE_IMGS = [pygame.image.load(os.path.join("imgs", "green note.png")),
             pygame.image.load(os.path.join("imgs", "red note.png")),
             pygame.image.load(os.path.join("imgs", "yellow note.png")),
             pygame.image.load(os.path.join("imgs", "blue note.png")),
             pygame.image.load(os.path.join("imgs", "orange note.png"))]


class Note:
    def __init__(self, color):
        self.VEL = 2
        if color == "green":
            self.x = WIDTH / 6
            self.y = HEIGHT / 2
            self.image = NOTE_IMGS[0]
        elif color == "red":
            self.x = WIDTH / 3
            self.y = HEIGHT / 2
            self.image = NOTE_IMGS[1]
        elif color == "yellow":
            self.x = WIDTH / 2
            self.y = HEIGHT / 2
            self.image = NOTE_IMGS[2]
        elif color == "blue":
            self.x = 2 * WIDTH / 3
            self.y = HEIGHT / 2
            self.image = NOTE_IMGS[3]
        elif color == "orange":
            self.x = 5 * WIDTH / 6
            self.y = HEIGHT / 2
            self.image = NOTE_IMGS[4]

    def update(self):
        self.y += self.VEL

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


'''
class InputBox:

    def __init__(self, x1, y1, x2, y2):
        self.color = WHITE
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.rect = pygame.Rect(x1, y1, x2, y2)

    # function used to get the user's input
    def user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    songSelection = songSelection[:-1]  # if backspace, remove last character
                else:
                    songSelection += event.unicode  # add the input onto the text string

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.rect)
        text_surface = BASE_FONT.render(songSelection, True, WHITE)
        screen.blit(text_surface, (self.x1 + 10, (self.x2 - self.x1)/2))'''


def song_menu():
    def draw_window(text):  # make a drawing function to easily display window, but specific to song-selecting
        screen.fill(BLUE)

        prompt = BASE_FONT.render("Please enter the name of your song:", True, GREY)
        screen.blit(prompt, (WIDTH / 4, HEIGHT / 3))
        screen.blit(text, (WIDTH / 4, HEIGHT / 2))
        pygame.display.update()

    songSelection = ""

    running = True
    while running:  # game loop
        clock.tick(FPS)
        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False
            # enter text to choose song
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    songSelection = songSelection[:-1]  # remove last character from text if backspaced
                elif event.key == pygame.K_RETURN:
                    return songSelection
                else:
                    songSelection += event.unicode

        # create a surface for the text
        textSurface = BASE_FONT.render(songSelection, True, WHITE)
        # draw everything
        draw_window(textSurface)


song = song_menu()

print(song)


def game():
    # use the created function
    songNotes = song_read(song)

    def draw_window(notes):
        screen.fill("black")

        for note in notes:
            note.draw()

        pygame.display.update()

    # set up the chosen song to play
    pygame.mixer.music.load("songs/{}.wav".format(song))
    pygame.mixer.music.play(-1)
    # get the game's start time
    startTime = round(time.time() * 1000)

    notes = [Note("green")]

    running = True
    while running:  # main game loop
        clock.tick(FPS)

        elapsed = round(time.time() * 1000) - startTime  # elapsed run-time
        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False

        for note in notes:
            note.update()

        draw_window(notes)


game()
