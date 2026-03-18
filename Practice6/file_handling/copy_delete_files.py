#append
with open("example.txt", "a") as f:
    f.write("Check it out\n")
    f.write("Check it out22\n")


#shutil(copy file)
import shutil

shutil.copy("example.txt", "copy_example.txt")


#delete file
import os

if os.path.exists("copy_example.txt"):
    os.remove("copy_example.txt")