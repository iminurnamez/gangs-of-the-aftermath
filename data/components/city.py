import pygame as pg

from .. import tools, prepare
from ..components.units import UNIT_NAMES
from ..components.labels import Label
from ..components.gang import Gang, EnemyGang, GANGS
from ..components.battle_handler import BattleHandler

HOOD_INFO = [
        #("Name", (r,g,b), center_pos, RCI, scavenge_chance, wanderer_chance, features, improvements
        ("Westdale", (255, 106, 0), (122, 68), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Auburndale", (127, 51, 0), (160, 233), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Sugar Ridge", (91, 127, 0), (144, 377), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Oak Hill", (255, 216, 0), (104, 504), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Maplehurst", (38, 127, 0), (248, 630), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Weston", (127, 106, 0), (339, 73), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Fulton", (64, 64, 64), (371, 210), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("College Station", (128, 128, 128), (375, 306), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Edgemont", (33, 0, 127), (336, 496), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Henley Heights", (127, 0, 110), (480, 93), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Manton", (255, 233, 127), (504, 246), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Mercer Park", (255, 0, 220), (482, 327), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Glendale", (0, 127, 127), (492, 474), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Holton", (161, 127, 255), (512, 599), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Tallwood", (127, 255, 142), (559, 683), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Emerald Park", (0, 19, 127), (565, 60), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Northbend", (182, 255, 0), (609, 243), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Pike Gardens", (127, 0, 55), (572, 304), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Prospect Circle", (127, 0, 0), (594, 394), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Granton", (127, 255, 255), (609, 492), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Fernwood", (255, 127, 127), (694, 669), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Rosedale", (0, 74, 127), (674, 100), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Colton", (178, 0, 255), (722, 268), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Southbend", (255, 0, 0), (704, 381), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Bayside", (0, 255, 33), (794, 608), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Spring Hill", (82, 127, 63), (857, 57), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Springvale", (255, 178, 127), (818, 168), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Ackerton", (0, 127, 70), (882, 243), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Cogtown", (72, 0, 255), (808, 345), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("East Bay", (0, 38, 255), (840, 431), (7, 3, 0), 25, 5, {"Park": 3}, {}),
        ("Eastdale", (0, 255, 255), (881, 535), (7, 3, 0), 25, 5, {"Park": 3}, {})
        ]


class City(object):
    def __init__(self, hood_info, gang_info):
        self.base = prepare.GFX["citymap-base"]
        self.base_rect = self.base.get_rect()
        self.screen_rect = pg.display.get_surface().get_rect()
        self.colormap = prepare.GFX["neighborhood-colormap"]
        self.mapleft = 162
        panel = prepare.GFX["ui-panel"]
        panel_width = panel.get_width()
        self.bg_rect = self.base_rect.inflate(panel_width * 2, 0)
        self.bg = pg.Surface(self.bg_rect.size)
        self.bg.blit(self.base, (panel_width, 0))
        self.bg.blit(panel, (0, 0))
        self.bg.blit(panel, (self.screen_rect.right - panel_width, 0))

        self.highlighted = None
        self.make_neighborhoods(hood_info)
        self.make_gangs(gang_info)
        self.make_gang_colors_image()

        for n in self.neighborhoods:
            n.neighbors = n.get_neighbors(self.neighborhoods)
        self.day = 0
        self.enemy_attacks = []

    def make_neighborhoods(self, hood_info):
        self.neighborhoods = pg.sprite.Group()
        for name, color, center_pos, rci, scavenge_chance, wanderer_chance, features, improvements in hood_info:
            neighborhood = Neighborhood(name, color, center_pos, rci, scavenge_chance,
                                                           wanderer_chance, features, improvements, self.colormap, hood_info,
                                                           self.mapleft, self.neighborhoods)

    def make_gangs(self, gang_info):
        self.gangs = pg.sprite.Group()
        for gang in gang_info:
            EnemyGang(gang, self, self.gangs)

    def make_gang_colors_image(self):
        self.gang_colors = pg.Surface(self.base_rect.size)
        for hood in self.neighborhoods:
            surf = hood.territory_image.copy()
            surf.set_alpha(255)
            if hood.owner:
                surf.set_colorkey(pg.Color("white"))
                img = surf.copy()
                img.fill(hood.owner.color)
                img.blit(surf, (0, 0))
                img.set_colorkey(pg.Color("black"))
                surf = img
            self.gang_colors.blit(surf, (0, 0))
            self.gang_colors.set_alpha(hood.alpha)

    def daily_update(self, player):
        self.day += 1
        player.gang.daily_update()
        battles = []
        player_involved = []
        for gang in self.gangs:
            gang.daily_update()
            if gang.opponent:
                battles.append((gang, gang.opponent))
        attackers = []
        defenders = []
        cleaned_battles = []
        for battle in battles:
            if battle[0] not in defenders:
                attackers.append(battle[0])
                defenders.append(battle[1].owner)
                cleaned_battles.append((battle[0], battle[1]))
        for attacker, hood in cleaned_battles:
            if hood in player.gang.hoods:
                self.enemy_attacks.append((attacker, hood))
            else:
                handler = BattleHandler(attacker, hood, self)
                handler.resolve_battle()
        
        




    def update(self, dt, map_pos):
        for hood in self.neighborhoods:
            try:
                if hood.mask.get_at(map_pos):
                    self.highlighted = hood
                    break
            except IndexError:
                pass
        else:
            self.highlighted = None




class Neighborhood(pg.sprite.Sprite):
    def __init__(self, name, color, center_pos, rci, scavenge_chance,
                         wanderer_chance, features, improvements,colormap,
                         hood_info, mapleft, *groups):
        super(Neighborhood, self).__init__(*groups)
        self.name = name
        self.color = color
        self.center_pos = center_pos
        self.rci = rci
        self.scavenge_chance = scavenge_chance
        self.wanderer_chance = wanderer_chance
        self.features = features
        self.improvements = improvements
        swap_dict = {tuple(info[1]): "black" for info in hood_info if info[1] != color}
        swap_dict[tuple(color)] = "white"
        self.territory_image = tools.color_swap(colormap, swap_dict)
        self.territory_image.set_colorkey(pg.Color("black"))
        self.alpha = 150
        self.territory_image.set_alpha(self.alpha)
        self.mask = pg.mask.from_surface(self.territory_image)
        self.area = self.mask.count()

        self.owner = None
        self.units = {x: 0 for x in UNIT_NAMES}
        x, y = self.center_pos
        self.name_label = Label(self.name, {"center": (x + mapleft, y)}, text_color="gray20", font_size=14)



    def get_neighbors(self, hoods):
        neighbors = set()
        for hood in (x for x in hoods if x is not self):
            offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for offset in offsets:
                if self.mask.overlap(hood.mask, offset):
                    neighbors.add(hood)
        return neighbors