import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.city import City, HOOD_INFO
from ..components.player import Player, PLAYER_DEFAULT
from ..components.helpers import UnitIcon, InventoryIcon, StatusBar
from ..components.items import ITEMS
from ..components.units import UNIT_NAMES
from ..components.gang import GANGS


class CityMapScreen(tools._State):
    def __init__(self):
        super(CityMapScreen, self).__init__()
        self.gang_filter = True

    def make_titles(self):
        self.titles = pg.sprite.Group()
        Label("Unassigned Units", {"topleft": (5, 5)}, self.titles)
        Label("Inventory", {"topleft": (1200, 5)}, self.titles)

    def make_unit_icons(self):
        self.icons = pg.sprite.Group()
        unit_names = UNIT_NAMES
        left = 50
        top = 50
        for unit_name in unit_names:
            num = self.player.gang.unassigned_units[unit_name]
            icon = UnitIcon((left, top), unit_name, num, self.icons)
            top += 60

    def make_inventory_icons(self):
        inventory = self.player.gang.inventory
        self.inventory_icons = pg.sprite.Group()
        left = 1140
        top = 50
        for i, item in enumerate(ITEMS, start=1):
            shift = 80 if not i % 2 else 0
            name = item[0]
            img_name = item[1]
            InventoryIcon((left + shift, top), name, img_name, inventory, self.inventory_icons)
            if not i % 2:
                top += 60

    def make_status_bars(self):
        self.status_bars = pg.sprite.Group()
        info = [
                ("Food", self.player.gang.food_happiness / 100.),
                ("Health", self.player.gang.health_happiness / 100.), 
                ("Comfort", self.player.gang.comfort_happiness / 100.),
                ("Fun", self.player.gang.fun_happiness / 100.)]
        left  = 8
        top = 300
        for name, val in info:
            StatusBar(name, (left, top), val, self.status_bars)
            top += 20
            
    def make_buttons(self):
        self.buttons = ButtonGroup()
        info = [("train", self.train_units),
                   ("gang-filter", self.toggle_gang_filter)]

        left = 16
        top = 620
        for name, callback in info:
            idle_img = prepare.BUTTONS["{}-idle".format(name)]
            hover_img = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, top), self.buttons, idle_image=idle_img,
                        hover_image=hover_img, call=callback,
                        click_sound=prepare.SFX["click"])
            top += 50
        idle = prepare.BUTTONS["next-turn-idle"]
        hover = prepare.BUTTONS["next-turn-hover"]
        Button((1140, 680), self.buttons, idle_image=idle, hover_image=hover, call=self.advance_day)

    def advance_day(self, *args):
        self.city.daily_update(self.player)
        self.make_unit_icons()
        self.make_inventory_icons()
        self.make_status_bars()

    def toggle_gang_filter(self, *args):
        self.gang_filter = not self.gang_filter

    def train_units(self, *args):
        self.done  = True
        self.next = "TRAIN_UNITS"
        self.persist["player"] = self.player

    def startup(self, persistent):
        self.persist = persistent
        self.city = self.persist["city"]
        self.player = self.persist["player"]
        self.make_titles()
        self.make_unit_icons()
        self.make_inventory_icons()
        self.make_buttons()
        self.make_status_bars()

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.done = True
            self.next = "SAVE_GAME"

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.city.highlighted:
                    if self.city.highlighted in self.player.gang.hoods:
                        self.done = True
                        self.next = "PLAYER_HOOD_SCREEN"
                        self.persist["neighborhood"] = self.city.highlighted
                        self.persist["player"] = self.player
                    else:
                        self.done = True
                        self.next = "ENEMY_HOOD_SCREEN"
                        self.persist["city"] = self.city
                        self.persist["neighborhood"] = self.city.highlighted
                        self.persist["player"] = self.player
        self.buttons.get_event(event)

    def update(self, dt):
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(prepare.MUSIC["grey-land"])
            pg.mixer.music.set_volume(.5)
            pg.mixer.music.play(-1)
        mousex, mousey = pg.mouse.get_pos()
        map_pos = mousex - self.city.mapleft, mousey
        self.city.update(dt, map_pos)
        self.buttons.update((mousex, mousey))
        if self.city.enemy_attacks:
            attacker, hood = self.city.enemy_attacks.pop()
            self.persist["attacker"] = attacker
            self.persist["neighborhood"] = hood
            self.persist["defender"] = hood.owner
            self.done = True
            self.next = "ENEMY_ATTACK"
            
    def draw(self, surface):
        surface.blit(self.city.bg, (0, 0))
        if self.city.highlighted:
            surface.blit(self.city.highlighted.territory_image, (self.city.mapleft, 0))
            self.city.highlighted.name_label.draw(surface)
        self.titles.draw(surface)
        for icon in self.icons:
            icon.draw(surface)
        for inv_icon in self.inventory_icons:
            inv_icon.draw(surface)
        for bar in self.status_bars:
            bar.draw(surface)
        self.buttons.draw(surface)
        if self.gang_filter:
            surface.blit(self.city.gang_colors, (self.city.mapleft, 0))
        for hood in self.city.neighborhoods:
            hood.name_label.draw(surface)
