#Write a Python program to find sequences of lowercase letters joined with a underscore.
import re
text = "hello_world test_string Hello_World"

print(re.findall(r"[a-z]+_[a-z]+", text))