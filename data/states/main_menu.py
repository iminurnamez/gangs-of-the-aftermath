import pygame as pg
import os
import json

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.gang import Gang, GANGS
from ..components.city import HOOD_INFO, City
from ..components.player import PLAYER_DEFAULT, Player


class MainMenu(tools._State):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.make_labels()
        self.make_buttons()

    def make_labels(self):
        self.labels = pg.sprite.Group()
        cx = prepare.SCREEN_RECT.centerx
        style = {"font_size": 84, "text_color": "gray15"}
        Label("Gangs", {"midtop": (cx, 20)}, self.labels, **style)
        Label("of the", {"midtop": (cx, 120)}, self.labels, **style)
        Label("Aftermath", {"midtop": (cx, 220)}, self.labels, **style)

    def make_buttons(self):
        self.buttons = ButtonGroup()
        names = ["newgame", "continue", "options", "tutorial"]
        calls = [self.new_game, self.load_game, self.options, self.tutorial]
        left = prepare.SCREEN_RECT.centerx - 64
        top = 400
        for name, call in zip(names, calls):
            idle = prepare.BUTTONS["{}-idle".format(name)]
            hover = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, top), self.buttons, idle_image=idle, hover_image=hover, call=call)
            top += 50

    def show_msg(self):
        label = Label("Loading City", {"center": prepare.SCREEN_RECT.center}, font_size=64, text_color="gray20")
        surf = pg.display.get_surface()
        surf.fill(pg.Color("gray60"))
        label.draw(surf)
        pg.display.update()
        
    def new_game(self, *args):
        self.show_msg()
        self.persist["city"] = City(HOOD_INFO, GANGS)
        self.persist["player"] = Player(self.persist["city"], PLAYER_DEFAULT)
        self.done  = True
        self.next = "CITYMAP"

    def load_game(self, *args):
        self.show_msg()
        hood_info = self.load_hoods()
        gang_info = self.load_gangs()
        self.persist["city"] = City(hood_info, gang_info)
        self.persist["player"] = Player(self.persist["city"], self.load_player())
        self.persist["city"].make_gang_colors_image()
        self.done  = True
        self.next = "CITYMAP"

    def load_player(self):
        load_path = os.path.join("resources", "saves", "player_save.json")
        try:
            with open(load_path, "r") as f:
                 loaded = json.load(f)
        except IOError:
            loaded = PLAYER_DEFAULT
        return loaded

    def load_gangs(self):
        load_path = os.path.join("resources", "saves", "gangs_save.json")
        try:
            with open(load_path, "r") as f:
                loaded = json.load(f)
        except IOError:
            loaded = GANGS
        return loaded

    def load_hoods(self):
        load_path = os.path.join("resources", "saves", "hoods_save.json")
        try:
            with open(load_path, "r") as f:
                loaded = json.load(f)
        except IOError:
            loaded = HOOD_INFO
        return loaded

    def options(self, *args):
        pass

    def tutorial(self):
        pass

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.fill(pg.Color("gray60"))
        self.labels.draw(surface)
        self.buttons.draw(surface)
