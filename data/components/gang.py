from random import randint, choice, shuffle
from itertools import cycle
import pygame as pg

from ..components.units import UNIT_NAMES, UNIT_REQS
from ..components.items import ITEMS
from ..components.scavenge_dicts import RESIDENTIAL, COMMERCIAL, INDUSTRIAL
from ..components.improvements import IMPROVEMENT_REQS

GANGS = [
        #("Gang Name", (r, g, b), (neighborhoods)
        ("Rattlers", (255, 127, 127), ("Colton", "Southbend", "Cogtown", "East Bay"),
         {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Jaguars", (255, 178, 127), ("Spring Hill", "Rosedale", "Emerald Park", "Springvale", "Ackerton"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Panthers", (255, 233, 127), ("Bayside", "Eastdale", "Fernwood", "Granton"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Wolverines", (218, 255, 127), ("Weston", "Henley Heights", "Fulton", "Manton"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Wolves", (165, 255, 127), ("Maplehurst", "Holton", "Tallwood"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Tigers", (127, 255, 142), ("Glendale", "Edgemont", "College Station"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Cobras", (127, 255, 255), ("Mercer Park", "Northbend", "Pike Gardens", "Prospect Circle"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Badgers", (127, 201, 255), ("Oak Hill", "Sugar Ridge"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None),
        ("Llamas", (127, 146, 255), ("Auburndale"),
        {"Soldier": 2, "Raider": 0, "Scavenger": 0, "Worker": 4}, None)
        ]




class Gang(pg.sprite.Sprite):
    def __init__(self, info, city, *groups):
        super(Gang, self).__init__(*groups)
        self.name, self.color, hoods, unit_dict, inventory = info
        self.hoods = [x for x in city.neighborhoods if x.name in hoods]
        self.make_units(unit_dict)
        if inventory is None:
            self.inventory = {item[0]: 0 for item in ITEMS}
        else:
            self.inventory = inventory
        #TESTING
        self.inventory["Food"] += 50.

        for hood in self.hoods:
            hood.owner = self
        self.food_level = "Adequate"
        self.food_levels = {
                #"name": (daily_ration, max_happy)
                "Minimal": (.4, 35),
                "Poor": (.7, 45),
                "Adequate": (1., 55),
                "Decent": (1.3, 65),
                "Good": (1.6, 80),
                "Decadent": (1.9, 95)
                }
        self.food_happiness = 100.
        self.comfort_happiness = 100.
        self.health_happiness = 100.
        self.fun_happiness = 100.
        
    def make_units(self, unit_dict):
        self.unassigned_units = {x: 0 for x in UNIT_NAMES}
        self.unassigned_units.update(unit_dict)

    def get_total_units(self):
        total_units = {x: 0 for x in UNIT_NAMES}
        for hood in self.hoods:
            for unit in hood.units:
                total_units[unit] += hood.units[unit]
        for un_unit in self.unassigned_units:
            total_units[un_unit] += self.unassigned_units[un_unit]
        return total_units

    def get_neighbors(self):
        neighbors = set()
        for hood in self.hoods:
            for n in hood.neighbors:
                neighbors.add(n)

    def daily_update(self):
        total_units = self.get_total_units()
        self.update_farms()
        self.scavenge()
        self.calc_happiness(total_units)
        num_wanderers = self.check_wanderers()

    def calc_food_ration(self, total_units):
        food_level = self.food_levels[self.food_level]
        num_total_units = sum(total_units.values())
        food_need = num_total_units * food_level[0]
        if food_need > self.inventory["Food"]:
            ration = self.inventory["Food"] / float(num_total_units)
        else:
            ration = food_level[0]
        withdrawal = ration * num_total_units
        return ration, withdrawal

    def calc_happiness(self, total_units):
        self.consume_food(total_units)
        food = self.food_happiness
        comfort = self.calc_comfort_happy(total_units)
        self.calc_health(total_units)
        health = self.health_happiness
        fun = self.calc_fun(total_units)
        
        self.happiness = ((food * 6) + (comfort * 1.5) + (health * 1.5) + fun) / 10.
        
    def check_mutiny(self):
        chance = self.happiness
    
    def calc_fun(self, total_units):
        num_units = sum(total_units.values())
        fun_need = .2
        fun = 0
        booze = self.inventory["Booze"]
        games = self.inventory["Games"]
        total = booze + games
        total_need = fun_need * num_units
        total_per = total / float(num_units)
        names = ["Booze", "Games"]
        shuffle(names)
        if total < total_need:
            self.inventory["Booze"] = 0
            self.inventory["Games"] = 0
            fun = total_per / float(total_need)
        else:
            for name in names:
                amt = self.inventory[name]
                deducted = min(amt, total_need)
                self.inventory[name] -= deducted
                total_need -= deducted
            fun = 1
        return fun


    def calc_health(self, total_units):
        num_units = sum(total_units.values())
        need = .2
        per_unit = self.inventory["Meds"] / num_units
        if per_unit >= need:
            health = 1
            self.inventory["Meds"] -= num_units * need
            self.health_happiness += .5
        else:
            percent = per_unit / need
            self.inventory["Meds"] = 0
            self.health_happiness -= percent
        self.health_happiness = max(0, min(self.health_happiness, 100.))

    def calc_comfort_happy(self, total_units):
        num_units = sum(total_units.values())
        total_comfort = 0
        needs = {"Clothing": (.2, .6),
                       "Toiletries": (.2, .4)}

        for item_name in needs:
            need, mod = needs[item_name]
            per_unit = self.inventory[item_name] / num_units
            if per_unit >= need:
                total_comfort += mod
                self.inventory[item_name] -= need * num_units
            else:
                percent = per_unit / need
                total_comfort += percent * mod
                self.inventory[item_name] = 0
        return total_comfort

    def calc_ammo_ration(self, total_units):
        total = 0
        total_num = 0
        for unit_name in ("Soldier", "Raider"):
            consumption = UNIT_CONSUMPTION[unit_name]
            num = total_units[unit_name]
            total_num += num
            per = consumption["Ammo"]
            total += num * per
        if self.inventory["Ammo"] < total:
            ration = self.inventory["Ammo"] / float(total_num)
            withdrawal = ration * total_num
        else:
            ration = "Full"
            withdrawal = total
        return ration, withdrawal

    def consume_food(self, total_units):
        ration, withdrawal = self.calc_food_ration(total_units)

        food_level = self.food_levels[self.food_level]
        if ration < food_level[0]:
            loss = 1 - (ration / 1.)
            self.food_happiness -= loss
        else:
            self.food_happiness += .5
        self.food_happiness = max(0, min(self.food_happiness, 100.))
        self.inventory["Food"] -= withdrawal

    def scavenge(self):
        all_loot = []
        for hood in self.hoods:
            chance = hood.scavenge_chance
            res_tries, comm_tries, ind_tries = hood.rci
            for _ in range(hood.units["Scavenger"]):
                for r in range(res_tries):
                    if randint(0, 100) < chance:
                        all_loot.append(choice(RESIDENTIAL))
                for c in range(comm_tries):
                    if randint(0, 100) < chance:
                        all_loot.append(choice(COMMERCIAL))
                for i in range(ind_tries):
                    if randint(0, 100) < chance:
                        all_loot.append(choice(INDUSTRIAL))
        for item in all_loot:
            self.inventory[item] += 1

    def check_wanderers(self):
        wanderers = 0
        for hood in self.hoods:
            if randint(0, 100) < hood.wanderer_chance:
                self.unassigned_units["Worker"] += 1
        return wanderers

    def update_farms(self):
        num_food = 0
        for hood in self.hoods:
            try:
                num_farms = hood.improvements["Farm"]
            except KeyError:
                num_farms = 0
            for _ in range(num_farms):
                num_food += randint(1, 8)
        self.inventory["Food"] += num_food







class EnemyGang(Gang):
    def __init__(self, info, unit_dict, city, *groups):
        super(EnemyGang, self).__init__(info, unit_dict, city, *groups)
        self.opponent = None
        total_units = self.unassign_all()
        ranked = self.rank_hoods()
        self.divvy_units(total_units, ranked)


    def unassign_all(self):
        total_units = {x: 0 for x in UNIT_NAMES}
        for hood in self.hoods:
            for unit in hood.units:
                total_units[unit] += hood.units[unit]
            hood.units = {x: 0 for x in UNIT_NAMES}
        for un_unit in self.unassigned_units:
            total_units[un_unit] += self.unassigned_units[un_unit]
        self.unassigned_units = {x: 0 for x in UNIT_NAMES}
        return total_units

    def daily_update(self):
        self.check_wanderers()
        total_units = self.unassign_all()
        self.opponent = None
        
        self.update_farms()
        self.consume_food(total_units)
        self.check_train_troops(total_units)
        self.check_build(total_units)
        self.opponent = self.attack_update(total_units)
        ranked = self.rank_hoods()
        self.divvy_units(total_units, ranked)
        self.scavenge()
        
    def rank_hoods(self):
        ranked = []
        for hood in self.hoods:
            num_features = sum(hood.features.values())
            num_improved = sum(hood.improvements.values())
            score = (num_features * .3) + (num_improved * .7)
            ranked.append((hood, score))
        ranked.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in ranked]

    def divvy_units(self, total_units, ranked_hoods):
        for name in ("Raider", "Soldier", "Scavenger", "Worker"):
            hoods = cycle(ranked_hoods)
            for _ in range(total_units[name]):
                hood = next(hoods)
                hood.units[name] += 1

    def check_build(self, total_units):
        num_farms = 0
        for h in self.hoods:
            try:
                num_farms += h.improvements["Farm"]
            except KeyError:
                pass

        population = sum(total_units.values())
        if num_farms < population // 5:
            for hood in self.hoods:
                if hood.features["Park"] > 0:
                    self.build("Farm", total_units, hood)
                    break

    def build(self, name, units, hood):
        inv = self.inventory
        features = IMPROVEMENT_REQS[name][0]
        materials = IMPROVEMENT_REQS[name][1]
        people = IMPROVEMENT_REQS[name][2]
        has_features = all((hood.features[x] >= features[x] for x in features))
        has_materials = all((inv[x] >= materials[x] for x in materials))
        has_people = all((units[x] >= people[x] for x in people))
        has_all =  all((has_features, has_materials, has_people))
        if has_all:
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

            
    def check_train_troops(self, total_units):
        if total_units["Scavenger"] <= len(self.hoods) * 2:
             self.train_unit("Scavenger", total_units)
        elif total_units["Soldier"] <= len(self.hoods):
            self.train_unit("Soldier", total_units)
        else:
            self.train_unit("Raider", total_units)

    def train_unit(self, unit_name, total_units):
        reqs = UNIT_REQS[unit_name]
        inventory = self.inventory
        units = total_units
        materials = {x: reqs[x] for x in reqs if x in inventory}
        people = {x: reqs[x] for x in reqs if x in UNIT_NAMES}
        has_materials = all((inventory[m] >= materials[m] for m in materials))
        has_people = all((units[p] >= people[p] for p in people))
        if has_materials and has_people:
            for m in materials:
                self.inventory[m] -= materials[m]
            for p in people:
                debt = people[p]
                total_units[p] -= debt
            total_units[unit_name] += 1
        return total_units

    def attack_update(self, total_units):
        att = self.attack_check(total_units)
        if att:
            opponent = self.choose_opponent()
            return opponent


    def attack_check(self, total_units):
        att_chance = total_units["Raider"] + (total_units["Soldier"] // 3)
        if randint(0, 100) < att_chance * 5:
            return True
        return False

    def choose_opponent(self):
        neighbors = []
        for hood in self.hoods:
            neighbors.extend([n for n in hood.neighbors if n not in self.hoods])
        if neighbors:
            return choice(neighbors)
        return

    def update(self, dt):
        pass

