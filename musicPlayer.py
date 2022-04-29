import pygame

name = input("What song to open: ")
with open("songs\\{}".format(name)) as file:
    notes = list(file.read().split("\n"))  # get each note and its time in an element of an array
    file.close()

print(notes)

