import os

cwd = os.getcwd()
if cwd[-4:] == "dist":
	os.chdir("..")
	cwd = os.getcwd()
print(f"Running in directory '{cwd}'")

selfUpdateFile = open(cwd + "\\selfUpdateDelta.txt")
for line in selfUpdateFile.readlines():
	os.remove(line)
	os.rename(line + "new", line)
selfUpdateFile.close()
os.remove(cwd + "\\selfUpdateDelta.txt")
print("Done!")