import os
import sys
from cx_Freeze import setup, Executable

class ExeCreator:
    def __init__(self, script_name, base):
        self.script_name = script_name
        self.base = base if sys.platform == "win32" else None

    def create_exe(self):
        setup(
            name=self.script_name,
            version="0.1",
            description=f"{self.script_name} Application",
            executables=[Executable(self.script_name, base=self.base)]
        )

if __name__ == "__main__":
    script_name = "game.py"
    exe_creator = ExeCreator(script_name, "Win32GUI")
    exe_creator.create_exe()