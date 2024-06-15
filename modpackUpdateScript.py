import os
import shutil
import urllib
import fsspec
from packaging.version import Version
from time import sleep

cwd = os.getcwd()
dataURL = "https://raw.githubusercontent.com/BreadBox64/server-modpack-host/main"
deltaObject = None
reinstall = False
try:
	currentVersion = Version(open(f"{cwd}\\modpackVersion.txt")[0])
	newVersion = Version(urllib.urlopen(f"{dataURL}/modpackVersion.txt")[0])
	if newVersion <= currentVersion:
		print(f"Modpack version {currentVersion} is already updated to or past upstream version {newVersion}")
		exit()
except OSError:
	reinstallPrompt = True
	while reinstallPrompt:
		reinstallInput = input("No modpack version file found, should the installer reinstall the whole pack [Y] or only apply the latest update [N]").strip()
		if reinstallInput == 'Y' or reinstallInput == 'y':
			reinstall = True
			reinstallPrompt = False
		elif reinstallInput == 'N' or reinstallInput == 'n':
			reinstall = False
			reinstallPrompt = False
		else:
			print("Invalid input.")
		
if reinstall:
	deltaObject = ["*kubejs", "*mods", "*resourcepacks", "*shaderpacks", "*texturepacks", "-servers.dat", "+servers.dat"]
else:
	deltaObject = urllib.urlopen(f"{dataURL}/modpackDelta.txt")
fs = fsspec.filesystem("github", org="BreadBox64", repo="server-modpack-host")
for delta in deltaObject:
	deltaType = delta[0]
	fileName = delta[1:]
	if deltaType == '+':
		fs.get(fs.ls(f"src/{fileName}"), f"{cwd}\\{fileName.replace('/', '\\')}")
	elif deltaType == '-':
		os.remove(f"{cwd}\\{fileName.replace('/', '\\')}")
	elif deltaType == '*':
		shutil.rmtree(f"{cwd}\\{fileName.replace('/', '\\')}")
		fs.get(fs.ls(f"src/{fileName}"), f"{cwd}\\{fileName.replace('/', '\\')}", recursive=True)