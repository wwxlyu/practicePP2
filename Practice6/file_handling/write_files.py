with open("example.txt", "w") as f:
    f.write("Good afternoon\n")
    f.write("If you read this - everything is working\n")

with open("new.txt", "x") as f:
    f.write("New file")