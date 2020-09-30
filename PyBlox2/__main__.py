import sys
import re
import os

local_dir = os.path.dirname(__file__)
file_path = os.path.join(local_dir, './__init__.py')

ex = re.compile("..version.. = \'(.*?)\'")

with open(file_path, "r") as f:
    text = f.read()

print("Version", ex.findall(text)[0])


