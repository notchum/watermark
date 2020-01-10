from cx_Freeze import setup, Executable

base = None    

executables = [Executable("./src/wmGUI.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "watermarker",
    options = options,
    version = "0.5",
    description = '<any description>',
    executables = executables
)