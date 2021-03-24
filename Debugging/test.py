import os
current_dir = os.getcwd()

for filename in os.listdir(current_dir):
    if filename.endswith(".jpg"):
      with open('log.txt', 'a') as file:
        file.write("file found!\n")
    else:
        print("Ooops, something went wrong")
