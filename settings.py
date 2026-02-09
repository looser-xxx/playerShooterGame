from os import walk
from os.path import join

import pygame

Big = True


if Big:
    window = (1920, 1080)
else:
    window = (1280, 720)
windowCenter = (window[0] / 2, window[1] / 2)
tileSize = 64
