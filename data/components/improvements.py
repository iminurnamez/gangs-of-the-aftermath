
"""player buildable (also occur naturally):
                farm - produces food, requires laborers
                still - produces booze
                defensive walls - bonus to defense when attacked
                housing - increase population limit
                    bare minimum, poor - req. build. materials
                    average - consumes fuel, requires build. material
                    good housing - consumes fuel, toiletries, requires build. materials
                garage - less auto part usage for troops
                water tank - holds so many gallons
                    excess water is lost
"""
"""
Features
    Hospital
    Clinic
    Pharmacy
    Park - can become a farm
    Police Station - weapons, ammo
    Armory - weapons, ammo
    dealership - vehicles
    Radio Tower - more new recruits
"""

IMPROVEMENT_REQS = {
        #"Name": ({feature_reqs}, {materials}, {people}
        "Farm": ({"Park": 1}, {"Building Materials": 5}, {"Worker": 1}),
        "Walls": ({}, {"Building Materials": 10}, {"Worker": 1})
        }

