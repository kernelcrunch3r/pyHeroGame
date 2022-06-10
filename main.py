import os
import pygame
from musicPlayer import song_reader

pygame.mixer.init()
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()

FPS = 30

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (187, 187, 187)
TEEL = (51, 245, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (206, 206, 206)

PIXEL_FONT_LARGE = pygame.font.Font(os.path.join("fonts", "prstartk.ttf"), 24)
PIXEL_FONT_NORMAL = pygame.font.Font(os.path.join("fonts", "prstartk.ttf"), 18)
PIXEL_FONT_SMALL = pygame.font.Font(os.path.join("fonts", "prstartk.ttf"), 12)

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("pyHero")  # window title
# WIDTH, HEIGHT  = pygame.display.get_surface().get_size()

BACKGROUND = pygame.image.load(os.path.join("imgs", "grey background.png"))

# array of the note images (different colors, just select from array)
NOTE_IMGS = [pygame.image.load(os.path.join("imgs", "green note1.png")),
             pygame.image.load(os.path.join("imgs", "red note1.png")),
             pygame.image.load(os.path.join("imgs", "yellow note1.png")),
             pygame.image.load(os.path.join("imgs", "blue note1.png")),
             pygame.image.load(os.path.join("imgs", "orange note1.png"))]

CHECKER_IMGS = [pygame.image.load(os.path.join("imgs", "green checker1.png")),
                pygame.image.load(os.path.join("imgs", "red checker1.png")),
                pygame.image.load(os.path.join("imgs", "yellow checker1.png")),
                pygame.image.load(os.path.join("imgs", "blue checker1.png")),
                pygame.image.load(os.path.join("imgs", "orange checker1.png"))]
CHECKER_Y = HEIGHT - 50 - CHECKER_IMGS[0].get_height()  # get the top position of the checker note


# class for the drawing the background, scrolling, etc.
class Background:
    def __init__(self, pic, nSpeed):
        self.image = pic
        # coords for bottom of the image
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.bottom = HEIGHT
        self.rect2 = self.image.get_rect(center=(self.x, self.y))
        self.rect2.top = self.rect.bottom

        self.vel = nSpeed * 0.3

    def update(self):
        self.rect.top -= self.vel
        self.rect2.top -= self.vel
        # check if the background is going off screen
        if self.rect2.bottom <= HEIGHT:
            self.rect.top = self.rect2.bottom
        if self.rect.bottom <= HEIGHT:
            self.rect2.top = self.rect.bottom

        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect2)


# class used to spawn a note corresponding to the passed color
class Note:
    def __init__(self, color, speed):
        self.VEL = speed
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

    def move(self, paused):
        if not paused:
            self.rect.bottom += self.VEL

    def draw(self):
        screen.blit(self.image, self.rect)
        # screen.blit(self.rect, (self.x, self.y))


# class used to display text on the screen
class TextBox:
    def __init__(self, text, x, y, color, font):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        # create a surface for the text
        self.textSurface = self.font.render(self.text, True, self.color)
        self.rect = self.textSurface.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.textSurface, self.rect)


# a class used to create a button using the passed text
class Button:
    def __init__(self, text, x, y, inactiveColor, activeColor):
        self.inactiveColor = inactiveColor
        self.activeColor = activeColor

        self.color = self.inactiveColor
        self.x = x
        self.y = y
        self.text = text
        # create a surface for the text
        self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)
        self.rect = self.textSurface.get_rect(center=(self.x, self.y))

    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # change color if the mouse hovers over the name
            self.color = self.activeColor
            # render the text again, potentially with new color
            self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)

        elif self.color == self.activeColor:  # if the color is active, but mouse is moved off, change color back
            self.color = self.inactiveColor
            # render the text again, potentially with new color
            self.textSurface = PIXEL_FONT_NORMAL.render(self.text, True, self.color)

        screen.blit(self.textSurface, self.rect)


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

running = True
while running:

    # Menu used to create a 3-letter username.
    def name_select():
        def draw_window(nameText, errorText):  # make a draw function to easily display window, but specific to song-selecting
            screen.fill(BLUE)

            prompt = TextBox("Please enter a 3-letter username:", WIDTH / 2, HEIGHT / 3, GREY, PIXEL_FONT_NORMAL)
            prompt.draw()

            if errorText != "":  # present an error if any occurs
                error = TextBox(errorText, WIDTH / 2, 2 * HEIGHT / 3, LIGHT_GREY, PIXEL_FONT_NORMAL)
                error.draw()

            name = TextBox(nameText, WIDTH / 2, HEIGHT / 2, WHITE, PIXEL_FONT_NORMAL)
            name.draw()

            pygame.display.update()

        nameSelection = ""
        errorMessage = ""

        vulgarities = ["FUC", "FUK", "SHT", "PSS", "PUS", "CNT", "DMN", "DAM", "GOD", "GDM", "NIG", "NGR", "ASS", "CUM",
                       "FAG", "FGT", "TIT", "COC", "COK", "CCK", "DIC", "DIK", "DCK", "SEX", "S3X", "PSY", "@SS", "@$$",
                       "A$S", "AS$", "@S$", "@$S", "C0C", "KKK", "F@G", "ELI", "PNS", "G0D"]

        nameRunning = True
        while nameRunning:  # game loop
            clock.tick(FPS)
            for event in pygame.event.get():  # to exit
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
                # enter text to choose song
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        nameSelection = nameSelection[:-1]  # remove last character from text if backspaced
                    elif event.key == pygame.K_RETURN:
                        if len(nameSelection) != 3:
                            errorMessage = "Make sure your name is 3-letters long."
                        elif nameSelection.upper() in vulgarities:
                            errorMessage = "Inappropriate name."
                        else:
                            return nameSelection.upper()  # select username in capitals
                    else:
                        nameSelection += event.unicode  # add on whatever is typed to the selection

            # draw everything
            draw_window(nameSelection, errorMessage)

    username = name_select()  # call the username menu to get a username

    # main loop after name is selected
    mainRunning = True
    while mainRunning:
        def song_clicking_menu():
            def draw_window(buttons):
                screen.fill(BLUE)

                for button in buttons:
                    button.draw()

                pygame.display.update()

            songButtons = []  # a list containing all the song objects to be displayed on screen
            # create a list containing the song file names
            songNames = os.listdir(os.path.join("song txts"))
            for i in range(len(songNames)):  # go through the list and remove the .txt from end
                songNames[i] = songNames[i][:-4]
                # add the button object to the list of song title buttons
                songButtons.append(Button(songNames[i], WIDTH / 2, HEIGHT * (i + 1) / (len(songNames) + 1), WHITE, GREY))

            running = True
            while running:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return "", True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # when mouse button is pressed, check if it collides with a song, then return that song as selected
                        for button in songButtons:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                return button.text, False  # return the song name as selection, and not back to name select

                draw_window(songButtons)


        song, backToName = song_clicking_menu()
        if backToName:  # quit this loop if they want a new name
            mainRunning = False

        def instructions():
            def draw_window():
                screen.fill(BLUE)

                instructionTexts = [TextBox("Moving from left to right, the", WIDTH / 2, 7 * HEIGHT / 15, GREY, PIXEL_FONT_NORMAL),
                                    TextBox("controls are: [a], [s], [d], [f], [space]", WIDTH / 2, 8 * HEIGHT / 15, GREY, PIXEL_FONT_NORMAL)]
                for instruction in instructionTexts:
                    instruction.draw()

                pygame.display.update()

            instRunning = True
            while instRunning:
                clock.tick(30)
                draw_window()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return True
                        else:
                            return False

        backToSongs = False
        if not backToName:
            backToSongs = instructions()  # display the game instructions

        points = 0.0  # user's points
        highest = []  # highest score ever
        newSong = False  # used to let program know if user wants a new song

        # Function containing the code for the main gameplay
        def game():
            # local function used to draw the game window
            def draw_window(notes, checkers, hits, hs, bg):
                if not paused:
                    bg.update()  # update the background

                for checker in checkers:
                    checker.draw()

                for note in notes:
                    note.draw()  # draw each

                # display user's current score
                score = PIXEL_FONT_NORMAL.render("{}".format(hits), True, WHITE, BLACK)
                screen.blit(score, score.get_rect(center=(15 * WIDTH / 16, HEIGHT / 16)))

                # display the all-time highscore and the corresponding username
                highscore = PIXEL_FONT_NORMAL.render("{} - {}".format(hs[0], hs[1]), True, WHITE, BLACK)
                screen.blit(highscore, highscore.get_rect(center=(WIDTH / 2, 15 * HEIGHT / 16)))

                # display text overtop of screen and pause movement
                if paused:
                    pygame.mixer.music.pause()
                    pausedPrompt = TextBox("GAME PAUSED", WIDTH / 2, 2 * HEIGHT / 5, BLACK, PIXEL_FONT_LARGE)
                    pausedPrompt.draw()
                    newSongButton.draw()  # draw the new song button from outer scope

                pygame.display.update()

            # use the imported function to read the selected song and put the notes and times into a list
            songNotes = song_reader("song txts", song)
            noteSpeed = float(songNotes[0][1])  # get the speed at which the notes fall
            songNotes.pop(0)

            # use the same function to get a list of the high scores for the current song
            highScores = song_reader("highscores", song)
            if len(highScores) > 0:
                highScores.sort(key=lambda x: x[1], reverse=True)
                highScore = highScores[0]
            else:
                highScore = ["CPV", 0.0]

            # set up the music
            pygame.mixer.music.load("songs/{}.mp3".format(song))

            checkerNotes = [NoteChecker("green"),
                            NoteChecker("red"),
                            NoteChecker("yellow"),
                            NoteChecker("blue"),
                            NoteChecker("orange")]
            checkHeight = checkerNotes[0].y

            # create a background object
            background = Background(BACKGROUND, noteSpeed)

            # get the game's start time
            startTime = pygame.time.get_ticks()

            # list of the generated notes appearing
            allNotes = []

            # object for the button to select a different song (in pause menu)
            newSongButton = Button("Click to select different song.", WIDTH / 2, HEIGHT / 2, BLACK, GREY)

            paused = False  # use for pausing the screen
            pausedStarts = []  # use to keep track of the times when paused
            pausedTime = 0  # use for total time paused

            newSong = False  # used in pause menu if they want to select a new song
            points = 0.0  # point counter
            musicPlaying = False  # music player boolean
            pos = 1  # counter used to run through the .txt's songNotes list
            gameRunning = True
            while gameRunning and not newSong:  # main game loop
                clock.tick(FPS)

                currentTime = pygame.time.get_ticks()
                elapsed = currentTime - startTime  # elapsed run-time

                # play the music when the first "log" in the file is passed
                if elapsed >= songNotes[0][1] + 200 + pausedTime and not musicPlaying and not paused:
                    pygame.mixer.music.play()
                    musicPlaying = True

                # check if the position is at the last "log," then end the program after it is passed
                if pos == len(songNotes) - 1:
                    if elapsed >= songNotes[0][1] + songNotes[-1][1] + pausedTime:
                        gameRunning = False
                        pygame.mixer.music.stop()

                # spawn a note in time to hit the checker at the right time
                # music start time plus note occurrence after start time minus the time it takes for note to fall plus total paused times
                elif elapsed >= songNotes[0][1] + songNotes[pos][1] - Note("green", noteSpeed).get_fall_time(checkHeight) + pausedTime and not paused:

                    # spawn a note corresponding to the "fret" pressed
                    if songNotes[pos][0] == "a":
                        allNotes.append(Note("green", noteSpeed))
                    elif songNotes[pos][0] == "s":
                        allNotes.append(Note("red", noteSpeed))
                    elif songNotes[pos][0] == "d":
                        allNotes.append(Note("yellow", noteSpeed))
                    elif songNotes[pos][0] == "f":
                        allNotes.append(Note("blue", noteSpeed))
                    elif songNotes[pos][0] == "space":
                        allNotes.append(Note("orange", noteSpeed))
                    pos += 1

                for event in pygame.event.get():  # to exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    # get the input that happens and check if it's at the right time to 'hit' a note
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if not paused:
                                paused = True
                                pygame.mixer.music.pause()
                                pausedStarts.append(elapsed)
                            else:
                                paused = False
                                pygame.mixer.music.unpause()
                                pausedTime += (elapsed - pausedStarts[-1])

                        if not paused:  # only look for input when the game is not paused
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

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if newSongButton.rect.collidepoint(pygame.mouse.get_pos()):
                            newSong = True

                for note in allNotes:
                    note.move(paused)

                # remove the first fallen note if it passes the checker's hitbox
                if len(allNotes) > 0 and allNotes[0].rect.top > checkerNotes[0].rect.bottom:
                    points -= 0.5  # remove a half-point if missed note
                    allNotes.pop(0)

                draw_window(allNotes, checkerNotes, points, highScore, background)
                pygame.display.set_caption("{} - {}".format(song, elapsed / 1000))  # program title is song name, elapsed time

            # enter the user's highScore into the highscores text files
            highscores = open(os.path.join("highscores", "{}.txt".format(song)), "a")
            highscores.write("{} {}\n".format(username, points))
            highscores.close()
            print("{} {}".format(username, points))

            return points, points * 100 / (len(songNotes) - 2), highScore, newSong  # return the user's points, and the all-time high score, and newSong state

        if not backToName and not backToSongs:  # they want to go back otherwise
            points, percent, highest, backToSongs = game()  # use the game to get the final number of points and the highest score to compare

        # have an end-screen with the user's results, and ask to play the game again.
        def end_screen():
            # draw window function
            def draw_window():
                screen.fill(BLUE)

                score = TextBox("{} points -- {}%".format(points, round(percent)), WIDTH / 2, HEIGHT / 4, WHITE, PIXEL_FONT_LARGE)
                score.draw()

                endPrompt = TextBox("Would you like to play again?", WIDTH / 2, HEIGHT / 2, WHITE, PIXEL_FONT_NORMAL)
                endPrompt.draw()

                for b in buttons:
                    b.draw()

                pygame.display.update()

            buttons = [Button("Yes", 3 * WIDTH / 7, 2 * HEIGHT / 3, WHITE, GREY),
                       Button("No", 4 * WIDTH / 7, 2 * HEIGHT / 3, WHITE, GREY)]

            endRunning = True
            while endRunning:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button in buttons:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                return button.text

                draw_window()  # draw the screen


        if not backToName and not backToSongs:  # new song would mean they exited the game, so no end screen
            end_selection = end_screen()
            if end_selection == "No":
                pygame.quit()  # exit the game if they don't want to replay
                exit()
