import os
import pygame
import time
from musicPlayer import song_reader


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
TEEL = (51, 245, 255)

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
            self.y = 0
            self.image = NOTE_IMGS[0]
        elif color == "red":
            self.x = WIDTH / 3
            self.y = 0
            self.image = NOTE_IMGS[1]
        elif color == "yellow":
            self.x = WIDTH / 2
            self.y = 0
            self.image = NOTE_IMGS[2]
        elif color == "blue":
            self.x = 2 * WIDTH / 3
            self.y = 0
            self.image = NOTE_IMGS[3]
        elif color == "orange":
            self.x = 5 * WIDTH / 6
            self.y = 0
            self.image = NOTE_IMGS[4]

    def move(self):
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


# Menu used to select a song.
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


# Function containing the code for the main gameplay
def game():
    # use the imported function to read the selected song and put the notes and times into a list
    songNotes = song_reader(song)

    # local function used to draw the game window
    def draw_window(notes):
        screen.fill(TEEL)

        for note in notes:
            note.draw()  # draw each

        pygame.display.update()

    # get the game's start time
    startTime = round(time.time() * 1000)

    # list of the generated notes appearing
    notes = []

    pos = 0  # counter used to run through the .txt's songNotes list
    running = True
    while running:  # main game loop
        clock.tick(FPS)

        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False

        elapsed = round(time.time() * 1000) - startTime  # elapsed run-time
        # if the elasped time is the same (within milliseconds) as the .txt note elapsed time, generate a new note
        if -20 <= songNotes[pos][1] - elapsed <= 20:
            if pos == 0:
                # set up the chosen song to play
                pygame.mixer.music.load("songs/{}.wav".format(song))
                pygame.mixer.music.play(-1)

            if songNotes[pos][0] == "a":
                notes.append(Note("green"))
            elif songNotes[pos][0] == "f":
                notes.append(Note("red"))
            elif songNotes[pos][0] == "space":
                notes.append(Note("yellow"))
            elif songNotes[pos][0] == "j":
                notes.append(Note("blue"))
            elif songNotes[pos][0] == ";":
                notes.append(Note("orange"))
            pos += 1
            if pos == len(songNotes):
                running = False

        for note in notes:
            note.move()

        draw_window(notes)


game()
