import os
import json

import pygame as pg

from .. import tools, prepare
from ..components.units import UNIT_NAMES


class SaveGame(tools._State):
    def __init__(self):
        super(SaveGame, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        city = self.persist["city"]
        gangs = city.gangs
        hoods = city.neighborhoods
        player = self.persist["player"]
        self.save(gangs, hoods, player)

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def save(self, gangs, hoods, player):
        self.save_gangs(gangs)
        self.save_hoods(hoods)
        self.save_player(player)

    def save_gangs(self, gangs):
        gangs_save = []
        for gang in gangs:
            unit_dict = gang.get_total_units()
            info = (gang.name, gang.color, [hood.name for hood in gang.hoods],
                       unit_dict, gang.inventory)
            gangs_save.append(info)
        save_path = os.path.join("resources", "saves", "gangs_save.json")
        with open(save_path, "w") as f:
            json.dump(gangs_save, f)


    def save_hoods(self, hoods):
        all_info = []
        for hood in hoods:
            info = [hood.name, hood.color, hood.center_pos, hood.rci, hood.scavenge_chance,
                       hood.wanderer_chance, hood.features, hood.improvements]
            all_info.append(info)
        save_path = os.path.join("resources", "saves", "hoods_save.json")
        with open(save_path, "w") as f:
            json.dump(all_info, f)

    def save_player(self, player):
        p = player
        units = {x: 0 for x in UNIT_NAMES}
        for hood in p.gang.hoods:
            for unit in hood.units:
                units[unit] += hood.units[unit]
        for p_unit in p.gang.unassigned_units:
            units[p_unit] += p.gang.unassigned_units[p_unit]
        hood_names = [h.name for h in p.gang.hoods]
        p_info = [p.gang.name, p.gang.color, hood_names, units, None]
        save_path = os.path.join("resources", "saves", "player_save.json")
        with open(save_path, "w") as f:
            json.dump(p_info, f)

