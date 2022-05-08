import time
import keyboard
import os
import pygame

'''
This file is to be used to create song txts in 
'''

name = input("Song: ")  # get the song choice

clock = pygame.time.Clock()
startTime = pygame.time.get_ticks()  # get the starting time

print(startTime)

level = open(os.path.join("song txts", "{}.txt".format(name)), "w")  # create a new file for the song and open it

pressed1 = False  # use to individually make sure a key isnt held
pressed2 = False
pressed3 = False
pressed4 = False
pressed5 = False
tPressed = False
while True:
    clock.tick(30)
    currentTime = pygame.time.get_ticks()
    elapsed = currentTime - startTime

    if keyboard.is_pressed("t"):
        if not tPressed:
            # I'll press t to represent time to start the music, just for simplicity looking at files
            level.writelines("{} {}\n".format("t", elapsed))
            tPressed = True  # stop looking for t presses

    if keyboard.is_pressed("e"):
        # t will represent ending time, so end program after pressing and recording time
        level.writelines("{} {}\n".format("e", elapsed))
        break

    if keyboard.is_pressed("a"):
        if not pressed1:  # only change file if the
            # write the pressed symbol and the elapsed program time
            level.writelines("{} {}\n".format("a", elapsed))
            pressed1 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed1 = False  # reset once the held key is released

    if keyboard.is_pressed("f"):
        if not pressed2:
            level.writelines("{} {}\n".format("f", elapsed))
            pressed2 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed2 = False  # reset once the held key is released

    if keyboard.is_pressed("j"):
        if not pressed3:
            level.writelines("{} {}\n".format("j", elapsed))
            pressed3 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed3 = False  # reset once the held key is released

    if keyboard.is_pressed(";"):
        if not pressed4:
            level.writelines("{} {}\n".format(";", elapsed))
            pressed4 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed4 = False  # reset once the held key is released

    if keyboard.is_pressed("space"):
        if not pressed5:
            level.writelines("{} {}\n".format("space", elapsed))
            pressed5 = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        pressed5 = False  # reset once the held key is released

    if keyboard.is_pressed("q"):  # exit the program
        break

level.close()
