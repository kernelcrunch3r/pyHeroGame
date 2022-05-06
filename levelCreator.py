import time
import keyboard
import os

'''
This file is to be used to create song txts in 
'''

name = input("Song: ")  # get the song choice

startTime = time.time()  # get the starting time

print(startTime)

level = open(os.path.join("song txts", "{}.txt".format(name)), "w")  # create a new file for the song and open it

wasPressed = False  # use to make sure no keys are held
while True:
    elapsed = round((time.time() - startTime) * 1000)
    if keyboard.is_pressed("a"):
        if not wasPressed:  # only change file if the
            # write the pressed symbol and the elapsed program time
            level.writelines("{} {}\n".format("a", elapsed))
            wasPressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("f"):
        if not wasPressed:
            level.writelines("{} {}\n".format("f", elapsed))
            wasPressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("j"):
        if not wasPressed:
            level.writelines("{} {}\n".format("j", elapsed))
            wasPressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed(";"):
        if not wasPressed:
            level.writelines("{} {}\n".format(";", elapsed))
            wasPressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("space"):
        if not wasPressed:
            level.writelines("{} {}\n".format("space", elapsed))
            wasPressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        wasPressed = False  # reset once the held key is released

    if keyboard.is_pressed("q"):
        break

level.close()
