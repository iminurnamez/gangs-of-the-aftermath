from random import randint, shuffle

from ..components.units import UNIT_STATS


class BattleHandler(object):
    def __init__(self, attacker, hood, city):
        self.attacker = attacker
        self.hood = hood
        self.city = city
        self.defenders = self.hood.units
        self.attackers = self.attacker.unassign_all()
        self.attacker_gone = False
        self.defender_gone = False

    def resolve_battle(self):
        for _ in range(100):
            def_dead = self.conduct_attack()
            att_dead = self.conduct_defense()
            self.reconcile_deaths(att_dead, def_dead)
            if self.attacker_gone:
                self.attacker.unassigned_units = self.attackers
                break
            elif self.defender_gone:
                self.attacker.unassigned_units = self.attackers
                self.hood.owner.hoods.remove(self.hood)
                self.hood.owner = self.attacker
                self.attacker.hoods.append(self.hood)
                self.city.make_gang_colors_image()
                break

    def reconcile_deaths(self, att_dead, def_dead):
        for a in range(att_dead):
            names = ["Soldier", "Raider"]
            shuffle(names)
            if self.attackers[names[0]] > 0:
                self.attackers[names[0]] -= 1
            elif self.attackers[names[1]] > 0:
                self.attackers[names[1]] -= 1
            else:
                self.attacker_gone = True
                break
        for d in range(def_dead):
            names = ["Soldier", "Raider", "Worker", "Scavenger"]
            shuffle(names)
            if self.defenders[names[0]] > 0:
                self.defenders[names[0]] -= 1
            elif self.defenders[names[1]] > 0:
                self.defenders[names[1]] -= 1
            elif self.defenders[names[2]] > 0:
                self.defenders[names[2]] -= 1
            elif self.defenders[names[3]] > 0:
                self.defenders[names[3]] -= 1
            else:
                self.defender_gone = True
                break

    def conduct_attack(self):
        hits = 0
        for name in ("Soldier", "Raider"):
            for _ in range(self.attackers[name]):
                if randint(1, 6) <= UNIT_STATS[name]["attack"]:
                    hits += 1
        return hits

    def conduct_defense(self):
        hits = 0
        for d in self.defenders:
            for _ in range(self.defenders[d]):
                if randint(1, 6) <= UNIT_STATS[d]["defense"]:
                    hits += 1
        return hits