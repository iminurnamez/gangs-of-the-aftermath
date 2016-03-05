import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.helpers import UnitIcon


class EnemyHoodScreen(tools._State):
    def __init__(self):
        super(EnemyHoodScreen, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))

    def make_labels(self):
        self.labels = pg.sprite.Group()
        cx = self.window.centerx
        top = self.window.top
        Label(self.neighborhood.name, {"midtop": (cx, top)},
                 self.labels, font_size=48, text_color="gray15")
        Label(self.neighborhood.owner.name, {"midtop": (cx, top + 55)},
                 self.labels, font_size=28, text_color="gray25")
        Label("Features", {"midtop": (cx, top + 300)}, self.labels,
                 font_size=28, text_color="gray20")
        feat_top = top + 330
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
        Label("Improvements", {"midtop": (centerx, top + 450)}, self.labels,
                 font_size=28, text_color="gray20")
        imp_top = top + 500
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
        b_info = []
        for h in self.player.gang.hoods:
            if self.neighborhood in h.neighbors:
                b_info.append(("attack", self.attack_warning))
                break
        top = self.window.centery + 100
        left = self.window.centerx - 64
        for name, callback in b_info:
            img = prepare.BUTTONS["{}-idle".format(name)]
            hover_img = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, top), self.buttons, idle_image=img, hover_image=hover_img, call=callback)
            top += 100

    def close_warning(self, *args):
        self.make_labels()
        self.make_buttons()

    def attack_warning(self, *args):
        self.labels = pg.sprite.Group()
        text = "{}?".format(self.neighborhood.name)
        Label("Attack", {"midtop": (self.window.centerx, self.window.top + 100)}, self.labels,
                 font_size=48, text_color="gray20")
        Label(text, {"midtop": (self.window.centerx, self.window.top + 150)}, self.labels,
                 font_size=48, text_color="gray20")
        self.buttons = ButtonGroup()
        b_info = [("attack", self.attack),
                       ("nevermind", self.close_warning)]
        top = self.window.centery + 100
        left = self.window.centerx - 64
        for name, callback in b_info:
            img = prepare.BUTTONS["{}-idle".format(name)]
            hover_img = prepare.BUTTONS["{}-hover".format(name)]
            Button((left, top), self.buttons, idle_image=img, hover_image=hover_img, call=callback)
            top += 40

    def attack(self, *args):
        self.persist["attacker"] = self.player.gang
        self.persist["neighborhood"] = self.neighborhood
        self.persist["defender"] = self.neighborhood.owner
        self.done = True
        self.next = "PLAYER_ATTACK"
        pg.mixer.music.stop()
        pg.mixer.music.load(prepare.MUSIC["undead-cyborg"])
        pg.mixer.music.play(-1)

    def startup(self, persistent):
        self.persist = persistent
        self.player = self.persist["player"]
        self.neighborhood = self.persist["neighborhood"]
        self.make_labels()
        self.make_buttons()

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
        self.buttons.draw(surface)

