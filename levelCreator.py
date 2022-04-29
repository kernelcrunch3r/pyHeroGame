import time
import keyboard
import os

'''
This file is to be used to create songs in 
'''

start_time = time.time()
print(start_time)

name = input("Song: ")  # get the song choice

level = open(os.path.join("songs", "{}.txt".format(name)), "w")  # create a new file for the song and open it

was_pressed = False  # use to make sure no keys are held
while True:
    if keyboard.is_pressed("a"):
        if not was_pressed:  # only change file if the
            level.writelines("{} {}\n".format("a", time.time() - start_time))
            was_pressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("f"):
        if not was_pressed:
            level.writelines("{} {}\n".format("f", time.time() - start_time))
            was_pressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("j"):
        if not was_pressed:
            level.writelines("{} {}\n".format("j", time.time() - start_time))
            was_pressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed(";"):
        if not was_pressed:
            level.writelines("{} {}\n".format(";", time.time() - start_time))
            was_pressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    elif keyboard.is_pressed("space"):
        if not was_pressed:
            level.writelines("{} {}\n".format("space", time.time() - start_time))
            was_pressed = True  # set to true so that even if key is pressed, nothing will happen; no holding
    else:
        was_pressed = False  # reset once the held key is released

    if keyboard.is_pressed("q"):
        break

level.close()
