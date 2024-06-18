from distutils.core import setup
import py2exe

setup(
	console = [{"script": 'modpackUpdateScript.py', "icon_resources": [(1, "updaterIcon.ico")]}, 'selfUpdate.py'],
	py_modules = ["modpackUpdateScript"],
	options = {
		"py2exe": {
			"includes": ["os", "shutil", "packaging.version", "fsspec", "requests", "fsspec.implementations.github", "ssl", "subprocess"], # The extra includes and packages were initially there to prevent requiring an installer and have everything bundle into a single exe, that hasnt worked, but I might try again later.
			"packages": ["fsspec", "requests", "ssl"],
			"bundle_files": 1,
			"compressed": True,
		}
	},
	zipfile = None
)