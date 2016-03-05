from random import randint, shuffle, sample

import pygame as pg

from .. import tools, prepare
from ..components.labels import Label, Button, ButtonGroup
from ..components.units import UNIT_STATS
from ..components.animation import Animation, Task


class BattleSprite(pg.sprite.Sprite):
    shoot_sounds = {
        "Worker": prepare.SFX["pistol"],
        "Scavenger": prepare.SFX["pistol"],
        "Raider": prepare.SFX["machinegun"],
        "Soldier": prepare.SFX["rifle"]
        }

    def __init__(self, unit_name, midbottom, facing, *groups):
        super(BattleSprite, self).__init__(*groups)
        self.name = unit_name
        self.image = prepare.GFX["{}-battle".format(unit_name)]
        self.facing = facing
        if self.facing == "left":
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.attack = UNIT_STATS[self.name]["attack"]
        self.defense = UNIT_STATS[self.name]["defense"]
        self.dead = False
        self.animations = pg.sprite.Group()
        self.shoot_sound = self.shoot_sounds[self.name]

    def fire(self, delay):
        dur = 250
        task = Task(self.shoot, delay)
        x_pos = self.rect.x
        ani = Animation(x=x_pos-5, delay=delay, duration=dur, round_values=True)
        ani2 = Animation(x=x_pos, delay=dur + delay, duration=dur, round_values=True)
        ani.start(self.rect)
        ani2.start(self.rect)
        self.animations.add(ani, ani2, task)

    def shoot(self):
        #add muzzle flash
        self.shoot_sound.play()
        #play shoot sound


    def die(self):
        self.dead = True
        if self.facing == "left":
            angle = -90
            self.image = pg.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(bottomleft=self.rect.midbottom)
        else:
            angle = 90
            self.image = pg.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(bottomright=self.rect.midbottom)

    def update(self, dt):
        self.animations.update(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class EnemyAttackScreen(tools._State):
    def __init__(self):
        super(EnemyAttackScreen, self).__init__()
        self.window_img = prepare.GFX["ui-window"]
        self.window = self.window_img.get_rect(topleft=(400, 40))

    def startup(self, persistent):
        self.animations = pg.sprite.Group()
        self.persist = persistent
        self.player = self.persist["player"]
        self.neighborhood = self.persist["neighborhood"]
        self.attacker = self.persist["attacker"]
        self.defender = self.persist["defender"]
        self.attacker.unassigned_units = self.attacker.unassign_all()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.make_labels()
        self.make_attack_sprites()
        self.make_defense_sprites()
        for s in self.all_sprites:
            self.all_sprites.change_layer(s, s.rect.bottom)

        self.conduct_battle()

    def make_attack_sprites(self):
        ys = range(self.window.top + 100, self.window.bottom - 150)
        shuffle(ys)
        self.attackers = pg.sprite.Group()
        for name in ("Soldier", "Raider"):
            for _ in range(self.attacker.unassigned_units[name]):
                y = ys.pop()
                x = randint(self.window.left + 40, self.window.left + 200)
                BattleSprite(name, (x, y), "right", self.attackers, self.all_sprites)

    def make_defense_sprites(self):
        ys = range(self.window.top + 100, self.window.bottom - 150)
        shuffle(ys)
        self.defenders = pg.sprite.Group()
        for name in self.neighborhood.units:
            for _ in range(self.neighborhood.units[name]):
                y = ys.pop()
                x = randint(self.window.right -200, self.window.right - 40)
                BattleSprite(name, (x, y), "left", self.defenders, self.all_sprites)

    def conduct_battle(self, *args):
        delay = 350
        for a in self.attackers:
            a.fire(delay)
            delay += 300
        delay += 1500
        for d in self.defenders:
            d.fire(delay)
            delay += 300
        def_dead = self.conduct_attack()
        att_dead = self.conduct_defense()
        task = Task(self.reconcile_deaths, delay + 750, args=(att_dead, def_dead))
        self.animations.add(task)

    def new_round(self):
        pass

    def conduct_attack(self):
        hits = 0
        for a in self.attackers:
            if randint(1, 6) <= a.attack:
                hits += 1
        return hits

    def conduct_defense(self):
        hits = 0
        for d in self.defenders:
            if randint(1, 6) <= d.defense:
                hits += 1
        return hits

    def reconcile_deaths(self, att_dead, def_dead):
        if att_dead < len(self.attackers):
            a_dead = sample(self.attackers, att_dead)
        else:
            a_dead = [x for x in self.attackers]
        if def_dead < len(self.defenders):
            d_dead = sample(self.defenders, def_dead)
        else:
            d_dead = [x for x in self.defenders]
        for a in a_dead:
            a.die()
            self.attacker.unassigned_units[a.name] -= 1
            self.attackers.remove(a)
        for d in d_dead:
            d.die()
            self.neighborhood.units[d.name] -= 1
            self.defenders.remove(d)
        for s in self.all_sprites:
            self.all_sprites.change_layer(s, s.rect.bottom)
        if len(self.attackers) < 1:
            task2 = Task(self.defender_win, 2000)
        elif len(self.defenders) < 1:
            task2 = Task(self.attacker_win, 2000)
        else:
            task2 = Task(self.conduct_battle, 1500)
        self.animations.add(task2)

    def make_labels(self):
        cx = self.window.centerx
        top = self.window.top
        self.labels = pg.sprite.Group()
        Label(self.neighborhood.name, {"midtop": (cx, top - 5)}, self.labels, font_size=48, text_color="gray15")
        Label(self.attacker.name, {"midtop": (cx -80, top + 50)}, self.labels, font_size=28, text_color="gray20")
        Label("vs", {"midtop": (cx, top + 55)}, self.labels, font_size=28, text_color="gray25")
        Label(self.defender.name, {"midtop": (cx + 80, top + 50)}, self.labels, font_size=28, text_color="gray20")


    def retreat(self, *args):
        self.done = True
        self.next = "CITYMAP"
        self.fadeout()

    def fadeout(self):
        pg.mixer.music.fadeout(5000)

    def attacker_win(self):
        self.fadeout()
        self.defender.hoods.remove(self.neighborhood)
        self.attacker.hoods.append(self.neighborhood)
        self.neighborhood.owner = self.attacker
        self.done = True
        self.next = "MESSAGE_SCREEN"
        texts = ["You lost", "control of", "{}!".format(self.neighborhood.name)]
        labels = []
        for text in texts:
            labels.append(Label(text, {"midtop": (0, 0)}, text_color="gray20", font_size=48))
        self.persist["messages"] = labels
        self.persist["city"].make_gang_colors_image()

    def defender_win(self):
        self.fadeout()
        self.done= True
        self.next = "MESSAGE_SCREEN"
        texts = ["The {}'".format(self.attacker.name),  "attack was", "unsuccessful"]
        labels = []
        for text in texts:
            labels.append(Label(text, {"midtop": (0, 0)}, text_color="gray20", font_size=48))
        self.persist["messages"] = labels

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
       
    def update(self, dt):
        self.animations.update(dt)
        mouse_pos = pg.mouse.get_pos()
        self.attackers.update(dt)
        self.defenders.update(dt)

    def draw(self, surface):
        surface.blit(self.window_img, self.window)
        self.labels.draw(surface)
        self.all_sprites.draw(surface)






