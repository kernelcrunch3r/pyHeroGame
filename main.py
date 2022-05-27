import os
import pygame
from musicPlayer import song_reader

pygame.mixer.init()
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 600
FPS = 30

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (187, 187, 187)
TEEL = (51, 245, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (206, 206, 206)

inactiveColor = WHITE
activeColor = GREY

PIXEL_FONT_NORMAL = pygame.font.Font(os.path.join("fonts", "prstartk.ttf"), 18)
PIXEL_FONT_SMALL = pygame.font.Font(os.path.join("fonts", "prstartk.ttf"), 12)

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
        # using the velocity of the notes and the distance from top of screen to the checker, I determined this formula
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
CHECKER_Y = HEIGHT - 50 - CHECKER_IMGS[0].get_height()  #


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
        if len(notes) >= 4:  # try to check the first four notes for collisions
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


# Menu used to create a 3-letter username.
def name_select():
    def draw_window(text, errorText):  # make a drawing function to easily display window, but specific to song-selecting
        screen.fill(BLUE)

        prompt = PIXEL_FONT_NORMAL.render("Please enter a 3-letter username:", True, GREY)
        promptRect = prompt.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(prompt, promptRect)  # "draw" the prompt text with the rect's position

        if errorText != "":
            error = PIXEL_FONT_NORMAL.render(errorText, True, LIGHT_GREY)
            errorRect = error.get_rect(center=(WIDTH / 2, 2 * HEIGHT / 3))
            screen.blit(error, errorRect)

        textRect = text.get_rect(center=(WIDTH/2, HEIGHT / 2))
        screen.blit(text, textRect)
        pygame.display.update()

    songSelection = ""
    errorMessage = ""

    vulgarities = ["FUC", "FUK", "SHT", "PSS", "PUS", "CNT", "DMN", "DAM", "GOD", "GDM", "NIG", "NGR", "ASS", "CUM",
                   "FAG", "FGT", "TIT", "COC", "COK", "CCK", "DIC", "DIK", "DCK", "SEX", "S3X", "PSY", "@SS", "@$$",
                   "A$S", "AS$", "@S$", "@$S", "C0C", "KKK", "F@G", "ELI", "PNS", ""]

    running = True
    while running:  # game loop
        clock.tick(FPS)
        for event in pygame.event.get():  # to exit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            # enter text to choose song
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    songSelection = songSelection[:-1]  # remove last character from text if backspaced
                elif event.key == pygame.K_RETURN:
                    if len(songSelection) != 3:
                        errorMessage = "Make sure your name is 3-letters long."
                    elif songSelection.upper() in vulgarities:
                        errorMessage = "Inappropriate name."
                    else:
                        return songSelection.upper()  # select username in capitals
                else:
                    songSelection += event.unicode  # add on whatever is typed to the selection

        # create a surface for the text
        textSurface = PIXEL_FONT_NORMAL.render(songSelection, True, WHITE)
        # draw everything
        draw_window(textSurface, errorMessage)


username = name_select()  # call the username menu to get a username


# a class used to create a button using the passed text
class SongButton:
    def __init__(self, text, x, y):
        self.color = inactiveColor
        self.x = x
        self.y = y
        self.text = text
        # create a surface for the text
        self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)
        self.rect = self.textSurface.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.textSurface, self.rect)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # change color if the mouse hovers over the name
            self.color = activeColor
            # render the text again, potentially with new color
            self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)

        elif self.color == activeColor:  # if the color is active, but mouse is moved off, change color back
            self.color = inactiveColor
            # render the text again, potentially with new color
            self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)


def song_clicking_menu():
    def draw_window(buttons):
        screen.fill(BLUE)

        for button in buttons:
            button.update()
            button.draw()

        pygame.display.update()

    songButtons = []  # a list containing all the song objects to be displayed on screen
    # create a list containing the song file names
    songNames = os.listdir(os.path.join("song txts"))
    for i in range(len(songNames)):  # go through the list and remove the .txt from end
        songNames[i] = songNames[i][:-4]
        # add the button object to the list of song title buttons
        songButtons.append(SongButton(songNames[i], WIDTH / 2, HEIGHT * (i + 1) / (len(songNames) + 1)))

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # when mouse button is pressed, check if it collides with a song, then return that song as selected
                for button in songButtons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        return button.text  # return the song name as selection

        draw_window(songButtons)


song = song_clicking_menu()


def instructions():
    def draw_window():
        screen.fill(BLUE)

        instructionTexts = []
        instructionRects = []
        instructionTexts.append(PIXEL_FONT_NORMAL.render("Moving from left to right, the", True, GREY))
        instructionRects.append(instructionTexts[0].get_rect(center=(WIDTH / 2, 7 * HEIGHT / 15)))
        instructionTexts.append(PIXEL_FONT_NORMAL.render("controls are: [a], [s], [d], [f], [space]", True, GREY))
        instructionRects.append(instructionTexts[1].get_rect(center=(WIDTH / 2, 8 * HEIGHT / 15)))

        for i in range(len(instructionTexts)):
            screen.blit(instructionTexts[i], instructionRects[i])  # "draw" the prompt text with the rect's position

        pygame.display.update()

    running = True
    while running:
        clock.tick(30)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                running = False


instructions()  # display the game instructions


# Function containing the code for the main gameplay
def game():
    # local function used to draw the game window
    def draw_window(notes, checkers, hits, hs):
        screen.fill(TEEL)

        for checker in checkers:
            checker.draw()

        for note in notes:
            note.draw()  # draw each

        score = PIXEL_FONT_NORMAL.render("{}".format(hits), True, WHITE, BLACK)
        screen.blit(score, score.get_rect(center=(15*WIDTH/16, HEIGHT/16)))

        highscore = PIXEL_FONT_NORMAL.render("{} - {}".format(hs[0], hs[1]), True, WHITE, BLACK)
        screen.blit(highscore, highscore.get_rect(center=(WIDTH/2, 15 * HEIGHT/16)))

        pygame.display.update()

    # use the imported function to read the selected song and put the notes and times into a list
    songNotes = song_reader("song txts", song)
    # use the same function to get a list of the high scores for the current song
    highScores = song_reader("highscores", song)
    highScores.sort(key=lambda x: x[1], reverse=True)
    highscore = highScores[0]

    # set up the music
    pygame.mixer.music.load("songs/{}.mp3".format(song))

    checkerNotes = [NoteChecker("green"),
                    NoteChecker("red"),
                    NoteChecker("yellow"),
                    NoteChecker("blue"),
                    NoteChecker("orange")]
    checkHeight = checkerNotes[0].y

    # get the game's start time
    startTime = pygame.time.get_ticks()

    # list of the generated notes appearing
    allNotes = []

    points = 0.0  # counter for notes hit at the right time
    musicPlaying = False  # music player boolean
    pos = 1  # counter used to run through the .txt's songNotes list
    running = True
    while running:  # main game loop
        clock.tick(FPS)

        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime  # elapsed run-time

        # play the music when the first "log" in the file is passed
        if elapsed >= songNotes[0][1] + 300 and not musicPlaying:
            pygame.mixer.music.play(-1)
            musicPlaying = True

        # check if the position is at the last "log," then end the program after it is passed
        if pos == len(songNotes) - 1:
            if elapsed >= songNotes[0][1] + songNotes[-1][1]:
                running = False
        # spawn a note in time to hit the checker at the right time
        # music start time plus note occurrence after start time minus the time it takes for note to fall
        elif elapsed >= songNotes[0][1] + songNotes[pos][1] - Note("green").get_fall_time(checkHeight):
            if pos == len(songNotes) - 1:  # the last position will signal the end of the song, ending game
                running = False

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
                            points += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note
                        else:
                            points -= 0.5

                elif event.key == pygame.K_s:
                    print("s tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[1].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            points += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note
                        else:
                            points -= 0.5

                elif event.key == pygame.K_d:
                    print("d tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[2].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            points += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note
                        else:
                            points -= 0.5

                elif event.key == pygame.K_f:
                    print("f tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[3].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            points += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note
                        else:
                            points -= 0.5

                elif event.key == pygame.K_SPACE:
                    print("space tapped")
                    if len(allNotes) > 0:
                        noteIsHit, hitNotePos = checkerNotes[4].collide_check(allNotes)
                        # check if a note hits the box at when right button is pressed
                        if noteIsHit:
                            points += 1
                            allNotes.pop(hitNotePos)  # remove the detected hit note
                        else:
                            points -= 0.5

        for note in allNotes:
            note.move()

        # remove the first fallen note if it passes the checker's hitbox
        if len(allNotes) > 0 and allNotes[0].rect.top > checkerNotes[0].rect.bottom:
            allNotes.pop(0)

        draw_window(allNotes, checkerNotes, points, highscore)
        pygame.display.set_caption("{} - {}".format(song, elapsed/1000))

    # enter the user's highscore into the highscores text files
    highscores = open(os.path.join("highscores", "{}.txt".format(song)), "a")
    highscores.write("{} {}\n".format(username, points))
    highscores.close()
    print("{} {}".format(username, points))


game()

