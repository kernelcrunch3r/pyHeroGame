import keyboard
import os
import pygame

'''
This file is to be used to create song txts in 
'''

name = input("Song: ")  # get the song choice

speed = input("What speed is the song being made at from the original? (1 = original): ")

addTime = input("What time in the song is being started at?: ")  # usually 0, but maybe further if I want to redo a part

clock = pygame.time.Clock()
startTime = pygame.time.get_ticks()  # get the starting time

print(startTime)

level = open(os.path.join("song txts", "{}.txt".format(name)), "w")  # create a new file for the song and open it
highScores = open(os.path.join("highscores", "{}.txt".format(name)), "a")

pressed1 = False  # use to individually make sure a key isnt held
pressed2 = False
pressed3 = False
pressed4 = False
pressed5 = False
tPressed = False
while True:
    clock.tick(30)
    currentTime = pygame.time.get_ticks()
    elapsed = round((currentTime - startTime) * float(speed) + float(addTime))

    if keyboard.is_pressed("t"):
        if not tPressed:
            if addTime == "0":
                # I'll press t to represent time to start the music, just for simplicity looking at files
                level.writelines("t {}\n".format(3000))  # start music after 3 seconds
            else:
                level.writelines("t {}\n".format(addTime))
            startTime = pygame.time.get_ticks()  # set start time to the t press time, so each log is time after music starts
            tPressed = True  # stop looking for t presses

    if keyboard.is_pressed("e"):
        # t will represent ending time, so end program after pressing and recording time
        level.writelines("e {}\n".format(elapsed))
        break

    if keyboard.is_pressed("a"):
        if not pressed1:  # only change file if the
            # write the pressed symbol and the elapsed program time
            level.writelines("a {}\n".format(elapsed))
            pressed1 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed1 = False  # reset once the held key is released

    if keyboard.is_pressed("s"):
        if not pressed2:
            level.writelines("s {}\n".format(elapsed))
            pressed2 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed2 = False  # reset once the held key is released

    if keyboard.is_pressed("d"):
        if not pressed3:
            level.writelines("d {}\n".format(elapsed))
            pressed3 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed3 = False  # reset once the held key is released

    if keyboard.is_pressed("f"):
        if not pressed4:
            level.writelines("f {}\n".format(elapsed))
            pressed4 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed4 = False  # reset once the held key is released

    if keyboard.is_pressed("space"):
        if not pressed5:
            level.writelines("space {}\n".format(elapsed))
            pressed5 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed5 = False  # reset once the held key is released

    if keyboard.is_pressed("q"):  # exit the program
        break

level.close()
