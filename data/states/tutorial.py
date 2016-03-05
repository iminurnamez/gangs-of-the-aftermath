import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup


class Tutorial(tools._State):
    def __init__(self):
        super(Tutorial, self).__init__()


    lines = {
        "Happiness": ["You must keep your gang members happy or they may replace you as their leader.",
                              "Happiness - Food",
                              "Health - Meds",
                              "Comfort - Clothing, Toiletries"


    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        self.buttons.get_event(event)

    def update(self, dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(dt)

    def draw(self, surface):
        surface.fill(pg.Color("gray80"))
        self.labels.draw(surface)
        self.buttons.draw(surface)





Units
    Soldier
    Raider
    Worker - one worker is needed for each improvement - new units can be created by training and equipping workers
    Scavenger - Scavengers comd the ruins looking for resources

Farms

Farms periodically generate food.


Attacking a Territory

All unassigned Soldiers and Raiders will launch an assault on the territory
    Continue Attack
    Retreat


Raiding a Territory

Steal from a rival neighborhood (do a multiple scavenge for each raider)