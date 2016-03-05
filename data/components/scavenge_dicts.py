DEFAULT = {
        "percentages": [
            ("Food", 65),
            ("Building Materials", 6),
            ("Booze", 4),
            ("Games", 4),
            ("Meds", 5),
            ("Toiletries", 4),
            ("Clothing", 4),
            ("Rifle", 2),
            ("Automatic", 1),
            ("Ammo", 4),
            ]
    }


DEFAULT_COMMERCIAL = {
        "percentages": [
            ("Food", 46),
            ("Building Materials", 8),
            ("Booze", 7),
            ("Games", 7),
            ("Meds", 7),
            ("Toiletries", 7),
            ("Clothing", 7),
            ("Rifle", 4),
            ("Automatic", 2),
            ("Ammo", 5)
            ]
    }

DEFAULT_INDUSTRIAL = {
        "percentages": [
            ("Food", 30),
            ("Building Materials", 20),
            ("Booze", 3),
            ("Games", 3),
            ("Meds", 3),
            ("Toiletries", 3),
            ("Clothing", 3),
            ("Rifle", 10),
            ("Automatic", 10),
            ("Ammo", 15)
            ]
    }

def make_scavenge_list(percentages):
    loot = []
    for name, num in percentages:
        loot.extend([name] * num)
    return loot

RESIDENTIAL = make_scavenge_list(DEFAULT["percentages"])


INDUSTRIAL = make_scavenge_list(DEFAULT_INDUSTRIAL["percentages"])


COMMERCIAL = make_scavenge_list(DEFAULT_COMMERCIAL["percentages"])


