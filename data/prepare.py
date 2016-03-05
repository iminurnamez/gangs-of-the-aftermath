"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

from . import tools


def load_button_images(names, sheet, size):
    names_ = []
    for n in names:
        names_.append("{}-idle".format(n))
        names_.append("{}-hover".format(n))
    imgs = tools.strip_from_sheet(sheet, (0, 0), size, 2, len(names))
    return {name: img for name, img in zip(names_, imgs)}



SCREEN_SIZE = (1280, 720)
ORIGINAL_CAPTION = "Gangs of the Aftermath"

#Initialization

pg.mixer.pre_init(44100, -16, 1, 512)

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


#Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"), accept=(".ttf", ".otf"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
names = ["newgame", "next-turn", "gang-filter", "continue", "options", "tutorial", "Farm", "OK",
                "retreat", "Units", "Walls", "train", "nevermind", "build", "attack",
                "Soldier", "Raider", "Scavenger"]
BUTTONS = load_button_images(names, GFX["button-sheet"], (128, 32))
small_names = ["plus", "minus"]
SMALL_BUTTONS = load_button_images(small_names, GFX["small-button-sheet"], (32, 32))

