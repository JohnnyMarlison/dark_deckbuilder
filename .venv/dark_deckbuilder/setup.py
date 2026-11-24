import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["arcade", "pyglet", "xml", "core", "views", "visuals", "audio"],
    "include_files": ["data"],
    "excludes": ["tkinter", "unittest", "email", "http", "pydoc"],
}



# Убираем чёрное консольное окно в Windows
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="DarkDeckbuilder",
    version="3.5",
    description="Тёмный Колодострой",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="DarkDeckbuilder.exe",
        )
    ],
)
