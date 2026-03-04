#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re

text = ["a", "ab", "abb", "ac"]

for t in text:
    if re.fullmatch(r"ab*", t):
        print(t)