from collections import OrderedDict

import pygame as pg


UNIT_NAMES = ["Soldier", "Raider", "Worker", "Scavenger"]

UNIT_STATS = {
        "Soldier": {"attack": 2, "defense": 3},
        "Raider": {"attack": 2, "defense": 3},
        "Worker": {"attack": 0, "defense": 1},
        "Scavenger": {"attack": 0, "defense": 1}
        }

UNIT_REQS = {
        "Soldier": OrderedDict([("Worker", 1), ("Rifle", 1), ("Ammo", 3)]),
        "Raider": OrderedDict([("Worker", 1), ("Automatic", 1), ("Ammo", 3)]),
        "Scavenger": OrderedDict([("Worker", 1)])
        }
