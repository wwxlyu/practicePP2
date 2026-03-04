#Write a Python program to split a string at uppercase letters.
import re
text = "HelloWorldTest"

result = re.split(r"(?=[A-Z])", text)

print(result)