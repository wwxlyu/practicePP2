#Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re
text = ["ab", "axxb", "ac", "bax"]

for t in text:
    if re.fullmatch(r"a.*b", t):
        print(t)