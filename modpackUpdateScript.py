import os
from sys import exit
import shutil
import fsspec
import subprocess
from packaging.version import Version

print("Starting modpackUpdateScript...")

cwd = os.getcwd()
if cwd[-4:] == "dist":
	os.chdir("..")
	cwd = os.getcwd()
print(f"Running in directory '{cwd}'")

fs = fsspec.filesystem("github", org="BreadBox64", repo="server-modpack-host")
deltaObject = None
selfUpdate = False
selfUpdatedFiles = []
reinstall = False
onlyLatest = False

try:
	print("Fetching version information...")
	fs.get("modpackVersion.txt", cwd + "\\newModpackVersion.txt")
	newVersionString = open(cwd + "\\newModpackVersion.txt").read().rstrip()
	currentVersionString = open(cwd + "\\modpackVersion.txt").read().rstrip()
	newVersion = Version(newVersionString)
	currentVersion = Version(currentVersionString)
	print(f"Found local modpack version {currentVersion} and upstream version {newVersion}.")
	if newVersion <= currentVersion:
		print(f"Modpack version {currentVersion} is already updated to or past upstream version {newVersion}, cancelling install.\nIf you need to reinstall the pack, delete modpackVersion.txt")
		os.remove(cwd + "\\newModpackVersion.txt")
		input("Press enter to exit...")
		exit()
except OSError:
	reinstallPrompt = True
	while reinstallPrompt:
		reinstallInput = input("No modpack version file found, should the installer reinstall the whole pack, [Y] or only apply the latest update? [N] ").rstrip()
		if reinstallInput == 'Y' or reinstallInput == 'y':
			reinstall = True
			reinstallPrompt = False
		elif reinstallInput == 'N' or reinstallInput == 'n':
			reinstall = False
			reinstallPrompt = False
			currentVersionString = newVersionString
			onlyLatest = True
		else:
			print("Invalid input.")
		
if reinstall:
	deltaList = ["*kubejs", "*mods", "*resourcepacks", "*shaderpacks", "-servers.dat", "+servers.dat"]
else:
	fs.get("modpackDelta.txt", cwd + "\\modpackDelta.txt")
	currentVersionString = f"!{currentVersionString}"
	deltaObject = open(cwd+"\\modpackDelta.txt")
	deltaList = []
	deltaRead = True
	deltaAlign = 0
	while deltaRead:
		line = deltaObject.readline().rstrip()
		if line == "":
			deltaRead = False
		else:
			if deltaAlign == 1:
				deltaList.append(line)
			elif deltaAlign == 0:
				if line == currentVersionString:
					if onlyLatest:
						deltaAlign = 1
						deltaList.append(line)
					else:
						deltaAlign = 2
			else:
				if line[0] == '!':
					deltaAlign = 1
					deltaList.append(line)

	continuePrompt = True
	while continuePrompt:
		continueInput = input(f"Delta lookup returned the following update delta: \n{str(deltaList)}\nContinue with update? [Y/N] ").rstrip()
		if continueInput == 'Y' or continueInput == 'y':
			print("Continuing with install.")
			continuePrompt = False
		elif continueInput == 'N' or continueInput == 'n':
			print("Cancelling install.")
			input("Press enter to exit...")
			exit()
		else:
			print("Invalid input.")

for delta in deltaList:
	print(f" Handling delta '{delta}'")
	deltaType = delta[0]
	fileName = delta[1:]
	fileLoc = cwd + '\\' + fileName.replace('/', '\\')
	match deltaType:
		case '+':
			fs.get(fileName, fileLoc)
		case '-':
			os.remove(fileLoc)
		case '*':
			try:
				shutil.rmtree(fileLoc)
			except FileNotFoundError:
				pass
			fs.get(fileName, fileLoc, recursive=True)
		case '!':
			print(f"Applying updates for version {fileName}.")
		case '&':
			selfUpdate = True
			fs.get(fileName, fileLoc + 'new')
			selfUpdatedFiles.append(fileLoc)

print("Finalizing update...")
try:
	os.remove(cwd + "\\modpackVersion.txt")
	os.rename(cwd + "\\newModpackVersion.txt", cwd + "\\modpackVersion.txt")
except FileNotFoundError:
	pass
except PermissionError:
	pass
try:
	os.remove(cwd + "\\modpackDelta.txt")
except PermissionError:
	pass

print("Update completed.")
input("Press enter to exit...")
if selfUpdate:
	selfUpdateFile = open(cwd + "\\selfUpdateDelta.txt", 'w')
	selfUpdateFile.writelines(selfUpdatedFiles)
	selfUpdateFile.close()
	subprocess.call('start /wait .\\dist\\selfUpdate.exe', shell=True)