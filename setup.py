import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["arcade", "pyglet", "xml", "core", "views", "visuals", "audio"],
    "include_files": ["data", "cards.json", "records.json"],
    "excludes": ["tkinter", "unittest", "email", "http", "pydoc"],
}

base = "gui" if sys.platform == "win32" else None

setup(
    name="DarkDeckbuilder",
    version="5.0",
    description="Dark Fantasy Roguelike Deckbuilder",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="DarkDeckbuilder.exe")],
)
