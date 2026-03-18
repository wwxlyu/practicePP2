import os
#create folders
"""
os.makedirs("test_dir/subdir", exist_ok=True)"""

#show files and folders
files = os.listdir(".")
print(files)

#find files
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)