import os
songNames = os.listdir(os.path.join("song txts"))
for i in range(len(songNames)):
    songNames[i] = songNames[i][:-4]
print(songNames)

for i in range(0):
    print("hi")