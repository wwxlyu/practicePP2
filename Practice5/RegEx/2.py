#Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re
text = ["ab", "abb", "abbb", "abbbb"]

for t in text:
    if re.fullmatch(r"ab{2,3}", t):
        print(t)