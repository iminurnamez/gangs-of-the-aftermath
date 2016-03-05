import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.improvements import IMPROVEMENT_REQS


class BuildIcon(pg.sprite.Sprite):
    def __init__(self, midtop, building_name, *groups):
        super(BuildIcon, self).__init__(*groups)
        self.image = prepare.GFX[building_name]
        self.rect = self.image.get_rect(midtop=midtop)
        reqs = IMPROVEMENT_REQS[building_name]
        features, materials, people = reqs
        texts = list(features.items())
        texts.extend(list(materials.items()))
        texts.extend(list(people.items()))
        texts = ("{} x{}".format(name, num) for name, num in texts)
        text = ", ".join(texts)
        self.req_label = Label("Requires: {}".format(text),
                                        {"midtop": (self.rect.centerx, self.rect.bottom + 5)},
                                        font_size=12, text_color="gray20")

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.req_label.draw(surface)

class BuildScreen(tools._State):
    def __init__(self):
        super(BuildScreen, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))

    def make_build_icons(self):
        self.icons = pg.sprite.Group()
        self.buttons = ButtonGroup()
        names = ["Farm"]
        centerx, top = self.window.centerx, self.window.top + 150
        left = centerx - 64
        for name in names:
            icon = BuildIcon((centerx, top), name, self.icons)
            idle = prepare.BUTTONS["{}-idle".format(name)]
            hover = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, icon.req_label.rect.bottom + 10), self.buttons, idle_image=idle,
                    hover_image=hover, call=self.build_improvement,
                    args=name)
            top += 80

    def build_improvement(self, name):
        hood = self.neighborhood
        inv = self.player.gang.inventory
        units = self.neighborhood.units #self.player.gang.unassigned_units
        features = IMPROVEMENT_REQS[name][0]
        materials = IMPROVEMENT_REQS[name][1]
        people = IMPROVEMENT_REQS[name][2]
        has_features = all((hood.features[x] >= features[x] for x in features))
        has_materials = all((inv[x] >= materials[x] for x in materials))
        has_people = all((units[x] >= people[x] for x in people))
        has_all =  all((has_features, has_materials, has_people))
        if has_all:
            prepare.SFX["hammer"].play()
            for f in features:
                hood.features[f] -= features[f]
            for m in materials:
                inv[m] -= materials[m]
            for p in people:
                units[p] -= people[p]
            if name in hood.improvements:
                hood.improvements[name] += 1
            else:
                hood.improvements[name] = 1
        else:
            prepare.SFX["negative"].play()

    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.neighborhood = self.persist["neighborhood"]
        self.labels = pg.sprite.Group()
        title = Label("Build Improvements", {"midtop": (self.window.centerx, self.window.top + 10)},
                          self.labels, font_size=48, text_color="gray15")
        Label(self.neighborhood.name, {"midtop": (self.window.centerx, title.rect.bottom + 5)},
                 self.labels, font_size=28, text_color="gray25")
        self.make_build_icons()

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                prepare.SFX["click"].play()
                self.done = True
                self.next = "PLAYER_HOOD_SCREEN"
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


