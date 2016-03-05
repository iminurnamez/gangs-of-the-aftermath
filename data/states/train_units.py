import pygame as pg

from .. import tools, prepare

from ..components.labels import Label, Button, ButtonGroup
from ..components.helpers import TrainingIcon
from ..components.units import UNIT_NAMES, UNIT_REQS


class TrainUnits(tools._State):
    equip_sounds = {x: prepare.SFX["{}-equip".format(x)]
                              for x in ("Raider", "Soldier", "Scavenger")}
    def __init__(self):
        super(TrainUnits, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))
        self.title = Label("Train Units", {"midtop": (self.window.centerx, self.window.top)},
                                font_path=prepare.FONTS["weblysleekuisb"], font_size=48, text_color="gray15")

    def make_training_icons(self, player):
        self.training_icons = pg.sprite.Group()
        self.buttons = ButtonGroup()
        centerx = self.window.centerx
        top = self.window.top + 100
        for name in ["Soldier", "Raider", "Scavenger"]:
            TrainingIcon((centerx, top), name, player, self.training_icons)
            idle_img = prepare.BUTTONS["{}-idle".format(name)]
            hover_img = prepare.BUTTONS["{}-hover".format(name)]
            Button((centerx - 64, top + 88), self.buttons, idle_image=idle_img,
                        hover_image=hover_img, call=self.train_unit, args=name)
            top += 160

    def train_unit(self, unit_name):
        reqs = UNIT_REQS[unit_name]
        inventory = self.player.gang.inventory
        units = self.player.gang.unassigned_units
        materials = {x: reqs[x] for x in reqs if x in inventory}
        people = {x: reqs[x] for x in reqs if x in units}
        has_materials = all((inventory[m] >= materials[m] for m in materials))
        has_people = all((units[p] >= people[p] for p in people))
        if has_materials and has_people:
            prepare.SFX["click"].play()
            self.equip_sounds[unit_name].play()
            for m in materials:
                self.player.gang.inventory[m] -= materials[m]
            for p in people:
                self.player.gang.unassigned_units[p] -= people[p]

            self.player.gang.unassigned_units[unit_name] += 1
        else:
            prepare.SFX["negative"].play()
            pass


    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.make_training_icons(self.player)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                prepare.SFX["click"].play()
                self.done = True
                self.next = "CITYMAP"
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)

    def draw(self, surface):
        surface.blit(self.window_img, self.window)
        self.title.draw(surface)
        for icon in self.training_icons:
            icon.draw(surface)
        self.buttons.draw(surface)