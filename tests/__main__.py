import importlib
import os
from pathlib import Path

tests = {}
directory = Path(str(Path(__file__).parent) + "\\src")

for filename in os.listdir(directory):
	f = filename.replace(".py", "")
	tests[f] = importlib.import_module("src." + f)


