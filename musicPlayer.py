import pygame
import time
import keyboard


# function used to open a created song txt file and transition all the lines into a list of lists
def song_reader(name):
    with open("song txts/{}.txt".format(name)) as file:  # open the input's file and put the lines into a list
        n = list(file.read().split("\n"))  # get each note and its time in an element of an array
        print(n)
        file.close()

    notes = []
    for note in n:
        note = note.split()  # split each note into its own list of its symbol and the time pressed
        notes.append(note)  # add the 'mini' list to full notes list

    notes.pop(len(notes) - 1)  # there is always a blank space at the end

    for i in range(len(notes)):
        notes[i][1] = int(notes[i][1])  # the level creator has already rounded the time into an integer but in a string

    print(notes)
    return notes


# only run the following code if this file is run (not if the file is imported)
if __name__ == "__main__":
    pygame.mixer.init()
    boom = pygame.mixer.Sound("songs/vine boom.mp3")

    name = input("What song to open: ")
    notes = song_reader(name)

    startTime = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    total = 0
    pos = 0
    while True:
        clock.tick(30)
        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime  # get elapsed run time, in order to
        if elapsed >= notes[pos][1]:
            boom.play()
            print(elapsed)
            pos += 1  # even if time is still within the range to trigger a sound, the position will have changed
            total += 1

        elif keyboard.is_pressed("q"):  # exit program
            break
        if pos == len(notes):
            time.sleep(3)  # wait for last note to finish
            break
    print(total)
