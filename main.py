import os
import pygame
from musicPlayer import song_reader


pygame.display.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
FPS = 30

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


# class used to spawn a note corresponding to the passed color
class Note:
    def __init__(self, color):
        self.VEL = 5
        if color == "green":
            self.x = WIDTH / 6
            self.y = 0
            self.image = NOTE_IMGS[0]
        elif color == "red":
            self.x = WIDTH /3
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
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.rect.bottom += self.VEL

    def draw(self):
        screen.blit(self.image, self.rect)
        # screen.blit(self.rect, (self.x, self.y))

    def get_mask(self):  # call to get the note's mask used for collisions
        return pygame.mask.from_surface(self.image)


CHECKER_IMGS = [pygame.image.load(os.path.join("imgs", "green checker.png")),
                pygame.image.load(os.path.join("imgs", "red checker.png")),
                pygame.image.load(os.path.join("imgs", "yellow checker.png")),
                pygame.image.load(os.path.join("imgs", "blue checker.png")),
                pygame.image.load(os.path.join("imgs", "orange checker.png"))]
CHECKER_Y = HEIGHT - 50 - CHECKER_IMGS[0].get_height()


# class for the image at the bottom of the screen used to "play" the note
class NoteChecker:
    def __init__(self, color):
        if color == "green":
            self.x = round(WIDTH / 6)
            self.y = CHECKER_Y
            self.image = CHECKER_IMGS[0]
        elif color == "red":
            self.x = round(WIDTH / 3)
            self.y = CHECKER_Y
            self.image = CHECKER_IMGS[1]
        elif color == "yellow":
            self.x = round(WIDTH / 2)
            self.y = CHECKER_Y
            self.image = CHECKER_IMGS[2]
        elif color == "blue":
            self.x = round(2 * WIDTH / 3)
            self.y = CHECKER_Y
            self.image = CHECKER_IMGS[3]
        elif color == "orange":
            self.x = round(5 * WIDTH / 6)
            self.y = CHECKER_Y
            self.image = CHECKER_IMGS[4]
        elif color == "test":
            self.x = 0
            self.y = 0
            self.image = CHECKER_IMGS[0]
        self.rect = self.image.get_rect(center=(self.x,self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def collide_check(self, note):
        # use masks for pixel-perfect collision checking
        noteMask = note.get_mask()
        noteRect = note.rect
        checkerMask = pygame.mask.from_surface(self.image)
        offset = (self.x - note.x, self.y - note.y)

        if noteRect.colliderect(self.rect):
            if noteMask.overlap(checkerMask, offset):
                return True


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

    checkerNotes = [NoteChecker("green"),
                    NoteChecker("red"),
                    NoteChecker("yellow"),
                    NoteChecker("blue"),
                    NoteChecker("orange")]

    # local function used to draw the game window
    def draw_window(notes, checkers):
        screen.fill(TEEL)
        NoteChecker("test").draw()

        for checker in checkers:
            checker.draw()
            if len(notes) > 0 and checker.collide_check(notes[0]):
                notes.pop(0)
        for note in notes:
            note.draw()  # draw each

        pygame.display.update()

    # get the game's start time
    startTime = pygame.time.get_ticks()

    # list of the generated notes appearing
    allNotes = []

    pos = 0  # counter used to run through the .txt's songNotes list
    pressed1 = False
    pressed2 = False
    pressed3 = False
    pressed4 = False
    pressed5 = False
    running = True
    while running:  # main game loop
        clock.tick(FPS)

        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if not pressed1:
                        print("a tapped")
                        '''pressed1 = True'''
                elif event.key == pygame.K_f:
                    if not pressed2:
                        print("f tapped")
                        '''pressed2 = True'''
                elif event.key == pygame.K_j:
                    if not pressed3:
                        print("j tapped")
                        '''pressed3 = True'''
                elif event.key == pygame.K_SEMICOLON:
                    if not pressed4:
                        print("; tapped")
                        '''pressed4 = True'''
                elif event.key == pygame.K_SPACE:
                    if not pressed5:
                        print("space tapped")
                        '''pressed5 = True'''

        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime  # elapsed run-time
        # if the elasped time is the same (within milliseconds) as the .txt note elapsed time, generate a new note
        if pos != len(songNotes):  # pos would be out of index range if its the length, so make sure that doesn't happen
            if elapsed >= songNotes[pos][1]:
                if pos == 0:
                    # the first timestamp decides when to start the song
                    pygame.mixer.music.load("songs/{}.mp3".format(song))
                    pygame.mixer.music.play(-1)

                if pos == len(songNotes) - 1:  # the last position will signal the end of the song, ending game
                    running = False

                # spawn a note corresponding to the "fret" pressed
                if songNotes[pos][0] == "a":
                    allNotes.append(Note("green"))
                elif songNotes[pos][0] == "f":
                    allNotes.append(Note("red"))
                elif songNotes[pos][0] == "space":
                    allNotes.append(Note("yellow"))
                elif songNotes[pos][0] == "j":
                    allNotes.append(Note("blue"))
                elif songNotes[pos][0] == ";":
                    allNotes.append(Note("orange"))
                pos += 1

        for note in allNotes:
            note.move()

        draw_window(allNotes, checkerNotes)


game()
