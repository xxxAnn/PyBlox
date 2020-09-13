import importlib
import os
from pathlib import Path

tests = {}
directory = Path(str(Path(__file__).parent) + "\\src")

for filename in os.listdir(directory):
	if not filename.startswith("__"):
		f = filename.replace(".py", "")
		success = True
		try:
			print("Running test", f)
			tests[f] = importlib.import_module("src." + f)
		except:
			success = False
		if success:
			print("Successfully passed test")
		else:
			print("Test failed")


