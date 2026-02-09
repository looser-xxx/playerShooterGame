from os import walk
from os.path import join

import sys
import pygame
from os import walk
from os.path import join, abspath, dirname

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

Big = True


if Big:
    window = (1920, 1080)
else:
    window = (1280, 720)
windowCenter = (window[0] / 2, window[1] / 2)
tileSize = 64
