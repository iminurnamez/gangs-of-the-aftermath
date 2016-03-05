import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.helpers import UnitIcon
from ..components.units import UNIT_NAMES


class PlayerHoodScreen(tools._State):
    def __init__(self):
        super(PlayerHoodScreen, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))

    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.neighborhood = self.persist["neighborhood"]
        self.make_labels()
        self.make_buttons()
        self.make_unit_icons()

    def make_labels(self):
        self.labels = pg.sprite.Group()
        cx = self.window.centerx
        top = self.window.top
        Label(self.neighborhood.name, {"midtop": (cx, top)},
                 self.labels, font_size=48, text_color="gray15")
        Label(self.neighborhood.owner.name, {"midtop": (cx, top + 55)},
                 self.labels, font_size=28, text_color="gray25")
        Label("Features", {"midtop": (cx, top + 310)}, self.labels,
                 font_size=28, text_color="gray20")
        feat_top = top + 360
        for i, f in enumerate(self.neighborhood.features, start=1):
            if i % 2:
                centerx = cx - 60
            else:
                centerx = cx + 60
            Label("{} x {}".format(f, self.neighborhood.features[f]),
                    {"midtop": (centerx, feat_top)}, self.labels, font_size=24,
                    text_color="gray25")
            if not i % 2:
                feat_top += 50
        Label("Improvements", {"midtop": (cx, top + 400)}, self.labels,
                 font_size=28, text_color="gray20")
        imp_top = top + 450
        for j, impr_ in enumerate(self.neighborhood.improvements):
            if j % 2:
                centerx = cx - 60
            else:
                centerx = cx + 60
            Label("{} x {}".format(impr_, self.neighborhood.improvements[impr_]),
                     {"midtop": (centerx, imp_top)}, self.labels, font_size=24,
                     text_color="gray25")

    def make_buttons(self):
        self.buttons = ButtonGroup()
        b_info = [("build", self.build),
                       ]
        top = self.window.centery + 250
        left = self.window.centerx - 64
        for name, callback in b_info:
            img = prepare.BUTTONS["{}-idle".format(name)]
            hover_img = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, top), self.buttons, idle_image=img,
                       hover_image=hover_img, call=callback,
                       click_sound=prepare.SFX["click"])
            top += 100

    def make_unit_icons(self):
        self.icons = pg.sprite.Group()
        unit_names = UNIT_NAMES
        centerx = self.window.centerx - 15
        top = 140
        for unit_name in unit_names:
            num = self.neighborhood.units[unit_name]
            icon = UnitIcon((centerx, top), unit_name, num, self.icons)
            up_idle = prepare.SMALL_BUTTONS["plus-idle"]
            up_hover = prepare.SMALL_BUTTONS["plus-hover"]
            down_idle = prepare.SMALL_BUTTONS["minus-idle"]
            down_hover = prepare.SMALL_BUTTONS["minus-hover"]
            up_button = Button((centerx - 70, top + 15), self.buttons, idle_image=up_idle, hover_image=up_hover, call=self.add_unit, args=icon)
            down_button = Button((centerx + 65, top + 15), self.buttons, idle_image=down_idle, hover_image=down_hover, call=self.remove_unit, args=icon)
            top += 50

    def add_unit(self, icon):
        unit_name = icon.unit_name
        available = self.player.gang.unassigned_units[unit_name]
        if available:
            prepare.SFX["click"].play()
            self.player.gang.unassigned_units[unit_name] -= 1
            self.neighborhood.units[unit_name] += 1
            icon.label.set_text( "x {}".format(self.neighborhood.units[unit_name]))
        else:
            prepare.SFX["negative"].play()
            pass

    def remove_unit(self, icon):
        unit_name = icon.unit_name
        num = self.neighborhood.units[unit_name]
        if num:
            self.player.gang.unassigned_units[unit_name] += 1
            self.neighborhood.units[unit_name] -= 1
            icon.label.set_text( "x {}".format(self.neighborhood.units[unit_name]))
        else:
            #play negative sound
            pass

    #def make_unit_icons(self):
    #    self.icons = pg.sprite.Group()
    #    unit_names = UNIT_NAMES
    #    centerx = self.window.centerx
    #    top = self.window.top + 80
    #    for unit_name in unit_names:
    #        num = self.neighborhood.units[unit_name]
    #        icon = UnitIcon((centerx, top), unit_name, num, self.icons)
    #        top += 50

    def build(self, *args):
        self.done = True
        self.next = "BUILD_SCREEN"

    def assign_units(self, *args):
        self.done = True
        self.next = "ASSIGN_UNITS"

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
        self.labels.draw(surface)
        for icon in self.icons:
            icon.draw(surface)
        self.buttons.draw(surface)


