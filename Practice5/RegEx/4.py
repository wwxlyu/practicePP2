#Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re
text = "London paris Berlin"

print(re.findall(r"[A-Z][a-z]+", text))