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
        self.color = color

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
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def get_fall_time(self, checkerHeight):
        return (1000 * checkerHeight) / (FPS * self.VEL)

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

    def collide_check(self, note):
        noteRect = note.rect

        if self.rect.colliderect(noteRect):
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

    pressed1 = False
    pressed2 = False
    pressed3 = False
    pressed4 = False
    pressed5 = False

    hits = 0  # counter for notes hit at the right time
    musicPlaying = False  # music player boolean
    pos = 0  # counter used to run through the .txt's songNotes list
    running = True
    while running:  # main game loop
        clock.tick(FPS)

        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime  # elapsed run-time

        # play the music when the first "log" in the file is passed
        if elapsed >= songNotes[0][1] and not musicPlaying:
            # the first timestamp decides when to start the song
            '''pygame.mixer.music.load("songs/{}.mp3".format(song))
            pygame.mixer.music.play(-1)'''
            musicPlaying = True

        if pos == len(songNotes):  # pos would be out of index, and all notes would be completed
            if elapsed >= songNotes[-1][1]:  # end at the last "log" in the txt file
                running = False
        # spawn a note in time to hit the checker at the right time
        elif elapsed >= songNotes[pos][1] - Note("green").get_fall_time(checkHeight):
            '''if pos == len(songNotes) - 1:  # the last position will signal the end of the song, ending game
                running = False'''

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

        '''# get the state of pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not pressed1:
            print("a tapped")
            pressed1 = True  # set the key as pressed so that it can't be held
            # check if first note matching corresponding key
            if len(allNotes) > 0 and allNotes[0].color == "green":
                # check if the first note is colliding with the corresponding checker
                if checkerNotes[0].collide_check(allNotes[0]):
                    hits += 1
                    allNotes.pop(0)  # remove the first note if pressed at right time
        elif not keys[pygame.K_a] and pressed1:
            pressed1 = False

        if keys[pygame.K_s] and not pressed2:
            print("s tapped")
            pressed2 = True
            # check if first note matching corresponding key
            if len(allNotes) > 0 and allNotes[0].color == "red":
                # check if the first note is colliding with the corresponding checker
                if checkerNotes[0].collide_check(allNotes[0]):
                    hits += 1
                    allNotes.pop(0)  # remove the first note if pressed at right time
        elif not keys[pygame.K_s] and pressed2:
            pressed2 = False

        if keys[pygame.K_d] and not pressed3:
            print("d tapped")
            pressed3 = True
            # check if first note matching corresponding key
            if len(allNotes) > 0 and allNotes[0].color == "yellow":
                # check if the first note is colliding with the corresponding checker
                if checkerNotes[0].collide_check(allNotes[0]):
                    hits += 1
                    allNotes.pop(0)  # remove the first note if pressed at right time
        elif not keys[pygame.K_d] and pressed3:
            pressed3 = False

        if keys[pygame.K_f] and not pressed4:
            print("f tapped")
            pressed4 = True
            # check if first note matching corresponding key
            if len(allNotes) > 0 and allNotes[0].color == "blue":
                # check if the first note is colliding with the corresponding checker
                if checkerNotes[0].collide_check(allNotes[0]):
                    hits += 1
                    allNotes.pop(0)  # remove the first note if pressed at right time
        elif not keys[pygame.K_f] and pressed4:
            pressed4 = False

        if keys[pygame.K_SPACE] and not pressed5:
            print("space tapped")
            pressed5 = True
            # check if first note matching corresponding key
            if len(allNotes) > 0 and allNotes[0].color == "orange":
                # check if the first note is colliding with the corresponding checker
                if checkerNotes[0].collide_check(allNotes[0]):
                    hits += 1
                    allNotes.pop(0)  # remove the first note if pressed at right time
        elif not keys[pygame.K_SPACE] and pressed5:
            pressed5 = False'''

        for event in pygame.event.get():  # to exits
            if event.type == pygame.QUIT:
                running = False

            # get the input that happens and check if it's at the right time to 'hit' a note
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and not pressed1:
                    print("a tapped")
                    pressed1 = True
                    # check if a note is colliding with the corresponding key pressed
                    for i in range(4):  # run for the first 5 notes because of chords
                        if len(allNotes) > 0 and allNotes[i].color == "green":  # only run if notes are onscreen
                            # check if the first note is colliding with the corresponding checker
                            if checkerNotes[0].collide_check(allNotes[i]):
                                hits += 1
                                allNotes.pop(i)  # remove the first note if pressed at right time

                if event.key == pygame.K_s and not pressed2:
                    print("s tapped")
                    pressed2 = True
                    # check if a note is colliding with the corresponding key pressed
                    for i in range(4):  # run for the first 5 notes because of chords
                        if len(allNotes) > 0 and allNotes[i].color == "red":  # only run if notes are onscreen
                            # check if the first note is colliding with the corresponding checker
                            if checkerNotes[1].collide_check(allNotes[i]):
                                hits += 1
                                allNotes.pop(i)  # remove the first note if pressed at right time

                if event.key == pygame.K_d and not pressed3:
                    print("d tapped")
                    pressed3 = True
                    # check if a note is colliding with the corresponding key pressed
                    for i in range(4):  # run for the first 5 notes because of chords
                        if len(allNotes) > 4 and allNotes[i].color == "yellow":  # only run if notes are onscreen
                            # check if the first note is colliding with the corresponding checker
                            if checkerNotes[2].collide_check(allNotes[i]):
                                hits += 1
                                allNotes.pop(i)  # remove the first note if pressed at right time

                if event.key == pygame.K_a and not pressed4:
                    print("f tapped")
                    pressed4 = True
                    # check if a note is colliding with the corresponding key pressed
                    for i in range(4):  # run for the first 5 notes because of chords
                        if len(allNotes) > 0 and allNotes[i].color == "blue":  # only run if notes are onscreen
                            # check if the first note is colliding with the corresponding checker
                            if checkerNotes[3].collide_check(allNotes[i]):
                                hits += 1
                                allNotes.pop(i)  # remove the first note if pressed at right time

                if event.key == pygame.K_SPACE and not pressed5:
                    print("space tapped")
                    pressed5 = True
                    # check if a note is colliding with the corresponding key pressed
                    for i in range(4):  # run for the first 5 notes because of chords
                        if len(allNotes) > 0 and allNotes[i].color == "orange":  # only run if notes are onscreen
                            # check if the first note is colliding with the corresponding checker
                            if checkerNotes[4].collide_check(allNotes[i]):
                                hits += 1
                                allNotes.pop(i)  # remove the first note if pressed at right time
                print(hits)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pressed1 = False
                elif event.key == pygame.K_s:
                    pressed2 = False
                if event.key == pygame.K_d:
                    pressed3 = False
                elif event.key == pygame.K_f:
                    pressed4 = False
                if event.key == pygame.K_SPACE:
                    pressed5 = False

        for note in allNotes:
            note.move()

        # remove the first fallen note if it passes the checker's hitbox
        if len(allNotes) > 0 and allNotes[0].rect.top > checkerNotes[0].rect.bottom:
            allNotes.pop(0)

        draw_window(allNotes, checkerNotes)
        pygame.display.set_caption("{}".format(clock.get_fps()))


game()
