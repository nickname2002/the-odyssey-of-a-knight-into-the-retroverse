import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base)]

setup(
    name="The Odyssey of a Knight - Into the Retro-Verse",
    version="1.0",
    description="A game created by a dude who has no clue what he's doing.",
    executables=executables
)
