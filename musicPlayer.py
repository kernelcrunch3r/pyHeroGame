import pygame
import time
import keyboard

start_time = round(time.time() * 1000)
pygame.mixer.init()
boom = pygame.mixer.Sound("songs\\vine boom.mp3")

name = input("What song to open: ")
with open("song txts\\{}.txt".format(name)) as file:
    n = list(file.read().split("\n"))  # get each note and its time in an element of an array
    print(n)
    file.close()

notes = []
for note in n:
    note = note.split()  # split each note into its own list of its symbol and the time pressed
    notes.append(note)  # add the 'mini' list to full notes list

notes.pop(len(notes) - 1)

for i in range(len(notes)):
    notes[i][1] = int(notes[i][1])

print(notes)

total = 0
pos = 0
while True:
    current_time = round(time.time() * 1000)
    elapsed = current_time - start_time
    print(elapsed)
    if elapsed == notes[pos][1]:
        boom.play()
        pos += 1
        total += 1
        if pos == len(notes):
            break

    elif keyboard.is_pressed("q"):  # exit program
        break
print(total)
