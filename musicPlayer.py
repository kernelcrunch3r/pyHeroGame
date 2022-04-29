import pygame

name = input("What song to open: ")
with open("songs\\{}".format(name)) as file:
    notes = list(file.readlines())
    file.close()

print(notes)
