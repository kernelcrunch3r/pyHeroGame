import os
import pygame
from musicPlayer import song_reader

pygame.mixer.init()
pygame.display.init()
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
NOTE_IMGS = [pygame.image.load(os.path.join("imgs", "green note1.png")),
             pygame.image.load(os.path.join("imgs", "red note1.png")),
             pygame.image.load(os.path.join("imgs", "yellow note1.png")),
             pygame.image.load(os.path.join("imgs", "blue note1.png")),
             pygame.image.load(os.path.join("imgs", "orange note1.png"))]


# class used to spawn a note corresponding to the passed color
class Note:
    def __init__(self, color):
        self.VEL = 7.5
        self.y = 0
        self.color = color

        if color == "green":
            self.x = WIDTH / 6
            self.image = NOTE_IMGS[0]
        elif color == "red":
            self.x = WIDTH / 3
            self.image = NOTE_IMGS[1]
        elif color == "yellow":
            self.x = WIDTH / 2
            self.image = NOTE_IMGS[2]
        elif color == "blue":
            self.x = 2 * WIDTH / 3
            self.image = NOTE_IMGS[3]
        elif color == "orange":
            self.x = 5 * WIDTH / 6
            self.image = NOTE_IMGS[4]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_fall_time(self, checkerHeight):
        return (1100 * checkerHeight) / (FPS * self.VEL)

    def move(self):
        self.rect.bottom += self.VEL

    def draw(self):
        screen.blit(self.image, self.rect)
        # screen.blit(self.rect, (self.x, self.y))


CHECKER_IMGS = [pygame.image.load(os.path.join("imgs", "green checker1.png")),
                pygame.image.load(os.path.join("imgs", "red checker1.png")),
                pygame.image.load(os.path.join("imgs", "yellow checker1.png")),
                pygame.image.load(os.path.join("imgs", "blue checker1.png")),
                pygame.image.load(os.path.join("imgs", "orange checker1.png"))]
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
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def collide_check(self, notes):
        if len(notes) >= 4:  # try to check the first four notes
            for i in range(4):
                noteRect = notes[i].rect

                if self.rect.colliderect(noteRect):
                    return True, i  # return a tuple with collision occurring boolean, and position in note list
        else:
            for i in range(len(notes)):
                noteRect = notes[i].rect

                if self.rect.colliderect(noteRect):
                    return True, i
        return False, 5  # no collisions have occurred


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
                    return songSelection  # select song when enter (return) is pressed
                else:
                    songSelection += event.unicode  # add on whatever is typed to the selection

        # create a surface for the text
        textSurface = BASE_FONT.render(songSelection, True, WHITE)
        # draw everything
        draw_window(textSurface)


song = song_menu()
# song = "smoke on the water real"

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
    checkHeight = checkerNotes[0].y

    # local function used to draw the game window
    def draw_window(notes, checkers):
        screen.fill(TEEL)
        # NoteChecker("test").draw()

        for checker in checkers:
            checker.draw()

        for note in notes:
            note.draw()  # draw each

        pygame.display.update()

    # get the game's start time
    startTime = pygame.time.get_ticks()

    # list of the generated notes appearing
    allNotes = []

    hits = 0  # counter for notes hit at the right time
    musicPlaying = False  # music player boolean
    pos = 1  # counter used to run through the .txt's songNotes list
    running = True
    while running:  # main game loop
        clock.tick(FPS)

        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime  # elapsed run-time

        # play the music when the first "log" in the file is passed
        if elapsed >= songNotes[0][1] and not musicPlaying:
            pygame.mixer.music.load("songs/{}.mp3".format(song))
            pygame.mixer.music.play(-1)
            musicPlaying = True

        if pos == len(songNotes):  # pos would be out of index, and all notes would be completed
            if elapsed >= songNotes[-1][1]:  # end at the last "log" in the txt file
                running = False
        # spawn a note in time to hit the checker at the right time
        # music start time plus note occurrence after start time minus the time it takes for note to fall
        elif elapsed >= songNotes[0][1] + songNotes[pos][1] - Note("green").get_fall_time(checkHeight):
            '''if pos == len(songNotes) - 1:  # the last position will signal the end of the song, ending game
                running = False'''

            # spawn a note corresponding to the "fret" pressed
            if songNotes[pos][0] == "a":
                allNotes.append(Note("green"))
            elif songNotes[pos][0] == "s":
                allNotes.append(Note("red"))
            elif songNotes[pos][0] == "d":
                allNotes.append(Note("yellow"))
            elif songNotes[pos][0] == "f":
                allNotes.append(Note("blue"))
            elif songNotes[pos][0] == "space":
                allNotes.append(Note("orange"))
            pos += 1

        pressed = 0  # variable used for which key number is pressed (1-5 from left to right)
        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False
            # get the input that happens and check if it's at the right time to 'hit' a note
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    print("a tapped")
                    if len(allNotes) > 0:  # start running as long as there are notes on screen
                        noteIsHit, hitNotePos = checkerNotes[0].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            hits += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note

                elif event.key == pygame.K_s:
                    print("s tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[1].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            hits += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note

                elif event.key == pygame.K_d:
                    print("d tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[2].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            hits += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note

                elif event.key == pygame.K_f:
                    print("f tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[3].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            hits += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note

                elif event.key == pygame.K_SPACE:
                    print("space tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[4].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            hits += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note

                '''if len(allNotes) > 0:
                    for i in range(3):  # check the first 5 notes for a collision on time with checkers
                        for ii in range(5):
                            if allNotes[i]'''


            print(hits)

        for note in allNotes:
            note.move()

        # remove the first fallen note if it passes the checker's hitbox
        if len(allNotes) > 0 and allNotes[0].rect.top > checkerNotes[0].rect.bottom:
            allNotes.pop(0)

        draw_window(allNotes, checkerNotes)
        pygame.display.set_caption("{}".format(clock.get_fps()))


game()
