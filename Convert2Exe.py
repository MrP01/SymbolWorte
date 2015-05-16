import sys
sys.argv.append("build")
from cx_Freeze import setup, Executable

# dependencies
build_exe_options = {
	"packages": ["sys", "atexit", "PySide.QtCore", "PySide.QtGui"],
	"include_files": ["Elements.csv","StopProcess.png"], # this isn't necessary after all
	"excludes": ["Tkinter", "Tkconstants", "tcl"],
	"build_exe": "build",
	#~ "icon": "./example/Resources/Icons/monitor.ico"
}

executable = [
	Executable("SymbolWorte.py",
			   base="Win32GUI",
			   targetName="SymbolWorte.exe",
			   targetDir="build",
			   copyDependentFiles=True)
]

setup(
	name="SymbolWorte",
	version="0.3",
	description="Konvertiert Worte in SymbolWorte!", # Using the word "test" makes the exe to invoke the UAC in win7. WTH?
	author="Peter Waldert",
	options={"build_exe": build_exe_options},
	executables=executable,
	requires=['PySide', 'cx_Freeze']
)
