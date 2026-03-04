#Write a Python program to convert a given camel case string to snake case.
import re
text = "helloWorldTest"

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)