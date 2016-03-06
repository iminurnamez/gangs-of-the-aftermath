from ..components.gang import Gang

PLAYER_DEFAULT = ("Pythons", (127, 127, 127), ("Westdale"), {"Worker": 1, "Scavenger": 1, "Soldier": 1, "Raider": 1}, None)

class Player(object):
    def __init__(self, city, info):
        self.gang = Gang(info, city)
