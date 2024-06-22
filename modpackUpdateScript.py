import os
from sys import exit
import shutil
import fsspec
import subprocess
from packaging.version import Version

try:
	os.system('color')

	class PrintFormats:
		DEFAULT = "\033[39m"
		RESET = "\033[0m"
		ERROR = "\033[91m"
		RED = "\033[31m"
		GREEN = "\033[32m"
		YELLOW = "\033[33m"
		BLUE = "\033[34m"

	def progressBar(current, total, currentDelta): # Progress bar blatantly stolen from https://stackoverflow.com/a/37630397
		bar_length = 20
		fraction = current / total

		arrow = int(fraction * bar_length - 1) * '-' + '>'
		padding = int(bar_length - len(arrow)) * ' '

		ending = '\n' if current == total else '\r'

		print(f'Update Progress: [{arrow}{padding}] {int(fraction*100)}% - {currentDelta}                                                                  ', end=ending)

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
		print(f"Fetching version information...")
		fs.get("modpackVersion.txt", cwd + "\\newModpackVersion.txt")
		newVersionString = open(cwd + "\\newModpackVersion.txt").read().rstrip()
		currentVersionString = open(cwd + "\\modpackVersion.txt").read().rstrip()
		newVersion = Version(newVersionString)
		currentVersion = Version(currentVersionString)
		print(f"Found local modpack version {PrintFormats.BLUE}{currentVersion}{PrintFormats.DEFAULT} and upstream version {PrintFormats.BLUE}{newVersion}{PrintFormats.DEFAULT}.")
		if newVersion <= currentVersion:
			print(f"Modpack version {PrintFormats.GREEN}{currentVersion}{PrintFormats.DEFAULT} is already updated to or past upstream version {PrintFormats.RED}{newVersion}{PrintFormats.DEFAULT}, cancelling install.\nIf you need to reinstall the pack, delete modpackVersion.txt")
			os.remove(cwd + "\\newModpackVersion.txt")
			input("Press enter to exit...")
			exit()
		else:
			print(f"Modpack version {PrintFormats.RED}{currentVersion}{PrintFormats.DEFAULT} is behind upstream version {PrintFormats.GREEN}{newVersion}{PrintFormats.DEFAULT}, fetching delta list.")
	except OSError:
		reinstallPrompt = True
		while reinstallPrompt:
			reinstallInput = input(f"No modpack version file found, should the installer reinstall the whole pack, {PrintFormats.YELLOW}[{PrintFormats.GREEN}Y{PrintFormats.YELLOW}]{PrintFormats.DEFAULT} or only apply the latest update? {PrintFormats.YELLOW}[{PrintFormats.RED}N{PrintFormats.YELLOW}] ").rstrip()
			if reinstallInput == 'Y' or reinstallInput == 'y':
				reinstall = True
				reinstallPrompt = False
			elif reinstallInput == 'N' or reinstallInput == 'n':
				reinstall = False
				reinstallPrompt = False
				currentVersionString = newVersionString
				onlyLatest = True
			else:
				print(f"{PrintFormats.DEFAULT}Invalid input.")
			
	if reinstall:
		deltaList = ["&dist/modpackUpdateScript.exe", "*kubejs", "*mods", "*resourcepacks", "*shaderpacks", "-servers.dat", "+servers.dat"]
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
			continueInput = input(f"{PrintFormats.DEFAULT}Delta lookup returned the following update delta: \n{PrintFormats.YELLOW}{str(deltaList)}{PrintFormats.DEFAULT}\nContinue with update? {PrintFormats.YELLOW}[{PrintFormats.GREEN}Y{PrintFormats.YELLOW}/{PrintFormats.RED}N{PrintFormats.YELLOW}] ").rstrip()
			if continueInput == 'Y' or continueInput == 'y':
				print(f"{PrintFormats.DEFAULT}Continuing with install.")
				continuePrompt = False
			elif continueInput == 'N' or continueInput == 'n':
				print(f"{PrintFormats.DEFAULT}Cancelling install.")
				os.remove(cwd + "\\newModpackVersion.txt")
				input("Press enter to exit...")
				exit()
			else:
				print(f"{PrintFormats.DEFAULT}Invalid input.")

	print(PrintFormats.YELLOW)

	i = 0
	total = len(deltaList)
	for delta in deltaList:
		#print(f" Handling delta '{delta}'")
		progressBar(i, total, delta)
		i += 1
		deltaType = delta[0]
		fileName = delta[1:]
		fileLoc = cwd + '\\' + fileName.replace('/', '\\')
		match deltaType:
			case '+':
				fs.get(fileName, fileLoc)
			case '-':
				try:
					os.remove(fileLoc)
				except FileNotFoundError:
					pass
			case '*':
				try:
					shutil.rmtree(fileLoc)
				except FileNotFoundError:
					pass
				fs.get(fileName, fileLoc, recursive=True)
			case '!':
				#print(f"Applying updates for version {fileName}.")
				pass
			case '&':
				selfUpdate = True
				fs.get(fileName, fileLoc + 'new')
				selfUpdatedFiles.append(fileLoc)
	progressBar(total, total, "Done!")

	print(PrintFormats.DEFAULT + "\nFinalizing update...")
	try:
		os.remove(cwd + "\\modpackVersion.txt")
	except FileNotFoundError:
		print(f"{PrintFormats.YELLOW}Unable to delete modpack version file due to file already being deleted!{PrintFormats.DEFAULT}")

	try:
		os.rename(cwd + "\\newModpackVersion.txt", cwd + "\\modpackVersion.txt")
	except PermissionError:
		print(f"{PrintFormats.ERROR}Unable to update version file due to another process having the file open!{PrintFormats.DEFAULT}")

	try:
		os.remove(cwd + "\\modpackDelta.txt")
	except FileNotFoundError:
		print(f"{PrintFormats.YELLOW}Unable to delete delta file due to file already being deleted!{PrintFormats.DEFAULT}")
	except PermissionError:
		print(f"{PrintFormats.YELLOW}Unable to delete delta file due to another process having the file open!{PrintFormats.DEFAULT}")

	print("Update completed.")
	input("Press enter to exit...")
	if selfUpdate:
		selfUpdateFile = open(cwd + "\\selfUpdateDelta.txt", 'w')
		selfUpdateFile.writelines(selfUpdatedFiles)
		selfUpdateFile.close()
		subprocess.call('start /wait .\\dist\\selfUpdate.exe', shell=True)
	print(PrintFormats.DEFAULT)
	exit()
except Exception as e:
	print(f"{PrintFormats.ERROR}Updater crashed with '{type(e)}' exception!\nMake sure to report this error with a screenshot of this message and the following details!{PrintFormats.RED}")
	print(e)
	input(PrintFormats.DEFAULT + "Press enter to exit...")