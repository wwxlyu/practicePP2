#Write a Python program to replace all occurrences of space, comma, or dot with a colon.
import re
text = "Hello, world. Python is fun"
result = re.sub(r"[ ,.]", ":", text)

print(result)