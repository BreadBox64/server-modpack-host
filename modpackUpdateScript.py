import os
from sys import exit
import shutil
import fsspec
from packaging.version import Version

cwd = os.getcwd()
fs = fsspec.filesystem("github", org="BreadBox64", repo="server-modpack-host")
deltaObject = None
reinstall = False
try:
	print(cwd + "\\modpackVersion.txt")
	fs.get("modpackVersion.txt", cwd + "\\newModpackVersion.txt")
	currentVersion = Version(open(cwd + "\\modpackVersion.txt").read().strip('\n'))
	newVersion = Version(open(cwd + "\\newModpackVersion.txt").read().strip('\n'))
	print(f"Found local modpack version {currentVersion} and upstream version {newVersion}.")
	if newVersion <= currentVersion:
		print(f"Modpack version {currentVersion} is already updated to or past upstream version {newVersion}, cancelling install.\nIf you need to reinstall the pack, delete modpackVersion.txt")
		input("Press any key to exit...")
		exit()
except OSError:
	reinstallPrompt = True
	while reinstallPrompt:
		reinstallInput = input("No modpack version file found, should the installer reinstall the whole pack, [Y] or only apply the latest update? [N] ").strip()
		if reinstallInput == 'Y' or reinstallInput == 'y':
			reinstall = True
			reinstallPrompt = False
		elif reinstallInput == 'N' or reinstallInput == 'n':
			reinstall = False
			reinstallPrompt = False
		else:
			print("Invalid input.")
		
if reinstall:
	deltaList = ["*kubejs", "*mods", "*resourcepacks", "*shaderpacks", "*texturepacks", "-servers.dat", "+servers.dat"]
else:
	fs.get("modpackDelta.txt", cwd + "\\modpackDelta.txt")
	deltaObject = open(cwd+"\\modpackDelta.txt")
	deltaList = []
	deltaRead = True
	deltaAlign = 0
	while deltaRead:
		line = deltaObject.readline()
		if deltaAlign == 1:
			deltaList.append(line)
		elif deltaAlign == 0:
			if line == f"!{str(currentVersion)}":
				deltaAlign = 2
		else:
			if line[0] == '!':
				deltaAlign = 1

	deltaString = f"\n{deltaObject.read()}\n"
	deltaObject.seek(0, os.SEEK_SET)

	continuePrompt = True
	while continuePrompt:
		continueInput = input(f"Delta lookup returned the following update delta: {deltaString}Continue with update? [Y/N] ").strip()
		if continueInput == 'Y' or continueInput == 'y':
			print("Continuing with install.")
			continuePrompt = False
		elif continueInput == 'N' or continueInput == 'n':
			print("Cancelling install.")
			input("Press any key to exit...")
			exit()
		else:
			print("Invalid input.")

for delta in deltaList:
	print(f"Handling delta '{delta}'")
	deltaType = delta[0]
	fileName = delta[1:]
	fileLoc = cwd + '//' + fileName.replace('/', '\\')
	if deltaType == '+':
		fs.get(fileName, fileLoc)
	elif deltaType == '-':
		os.remove(fileLoc)
	elif deltaType == '*':
		shutil.rmtree(fileLoc)
		fs.get(fileName, fileLoc, recursive=True)

print("Update completed.")
input("Press any key to exit...")