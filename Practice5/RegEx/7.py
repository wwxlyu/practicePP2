#Write a python program to convert snake case string to camel case string.
import re
text = "hello_world_test"

result = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(result)