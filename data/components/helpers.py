import pygame as pg
from .. import tools, prepare
from ..components.labels import Label
from ..components.units import UNIT_REQS, UNIT_STATS


class StatusBar(pg.sprite.Sprite):
    def __init__(self, name, topleft, val, *groups):
        super(StatusBar, self).__init__(*groups)
        self.color = tools.lerp((127, 0, 0), (38, 127, 0), val)
        bar_width = int(80 * val)
        left, top = topleft
        left += 60
        self.rect = pg.Rect((left, top), (80, 14)) 
        self.bar_rect = pg.Rect((left, top), (bar_width, 14))
        self.label = Label(name, {"midleft": (topleft[0], self.rect.centery)},
                                  text_color="gray20", font_size=12)
                
    def draw(self, surface):
        pg.draw.rect(surface, (48, 48, 48), self.rect)
        pg.draw.rect(surface, self.color, self.bar_rect)
        pg.draw.rect(surface, (137, 137, 137), self.rect, 2)
        self.label.draw(surface)
        

class UnitIcon(pg.sprite.Sprite):
    def __init__(self, midtop, unit_name, num, *groups):
        super(UnitIcon, self).__init__(*groups)
        self.unit_name = unit_name
        self.num = num
        self.image = prepare.GFX[unit_name.lower()]
        self.rect = self.image.get_rect(midtop=midtop)
        style = {"font_size": 18, "text_color": "gray5"}
        self.label = Label("x {}".format(self.num), {"midleft": (self.rect.right, self.rect.centery + 10)}, **style)

    def update(self, units):
        self.num = len((x for x in units if unit.name == self.unit_name))
        self.label.update_text("x {}".format(self.num))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.label.draw(surface)


class InventoryIcon(pg.sprite.Sprite):
    def __init__(self, midtop, item_name, img_name, inventory_dict, *groups):
        super(InventoryIcon, self).__init__(*groups)
        self.item_name = item_name
        self.image = prepare.GFX[img_name]
        self.rect = self.image.get_rect(midtop=midtop)
        self.make_qty_label(inventory_dict)

    def make_qty_label(self, inventory_dict):
        qty = "{}".format(int(inventory_dict[self.item_name]))
        self.label = Label(qty, {"topleft": (self.rect.centerx + 35, self.rect.top)})


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.label.draw(surface)


class TrainingIcon(pg.sprite.Sprite):
    def __init__(self, midtop, unit_name, player, *groups):
        super(TrainingIcon, self).__init__(*groups)
        self.labels = pg.sprite.Group()

        self.rect = pg.Rect((0, 0), (320, 480))
        self.rect.midtop = midtop
        self.icon_img = prepare.GFX[unit_name.lower()]
        self.icon_rect = self.icon_img.get_rect(midtop=(self.rect.centerx, self.rect.top))
        reqs = UNIT_REQS[unit_name]
        stats = UNIT_STATS[unit_name]

        att_label = Label("Attack: {}  Defense: {}".format(stats["attack"], stats["defense"]), {"midtop": (self.rect.centerx, self.icon_rect.bottom + 5)}, self.labels, text_color="gray20")
        requires_text = ", ".join(("{} x {}".format(r, reqs[r]) for r in reqs))
        req_label = Label("Requires: {}".format(requires_text), {"midtop": (self.rect.centerx, att_label.rect.bottom)}, self.labels, text_color="gray20")

    def draw(self, surface):
        surface.blit(self.icon_img, self.icon_rect)
        self.labels.draw(surface)

