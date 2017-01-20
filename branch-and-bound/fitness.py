people = [ 'andres','francisco','mario','dax','daniel','ruddy','octavio','rommel','christian','jose','juan','joaz','bruce','mitchell','pia','gema','allison','walter' ]

"""
Seat labels
---------------------
|       1   2   3   |
|
|       4   5   6   |
|----+  7   8   9
|    |              |
|----+
|    |  10  11  12  |
|--- +  13  14  15
|
|     16  17   18   |
---------------------
"""

seats = range(1,19)

def adjacentSeats(seat):
    if seat % 3 == 0: return [ seat -1  ]
    if seat % 3 == 1: return [ seat + 1  ]
    return [ seat - 1, seat + 1 ]

# 0 means it's cold, 2 means it's hot
seatHeat = { 1: 0, 2: 1, 3: 2,
        4: 0, 5: 1, 6: 2,
        7: 0, 8: 1, 9: 2,
        10: 0, 11: 1, 12: 2,
        13: 0, 14: 1, 15: 2,
        16: 0, 17: 1, 18: 2,
        }

# 0 means you like it cold, 2 means you like it hot, absence means you don't care
peopleHeat = {
    'andres': 2,
    'francisco': 0,
    'mario': 0,
    'dax': 1,
    'octavio': 1,
    'mitchell': 2,
    'pia': 2,
    'gema': 2,
}

# Each team has various tiers,
teams = [
    {'name': 'wp', 'tiers': [ (3, ['mario','dax','daniel']) ] },
    {'name': 'mobile', 'tiers': [ (3, ['jose','christian']), (1,'octavio') ] },
    {'name': 'harmons-app', 'tiers': [ (3, ['jose','christian','juan']), (1,'bruce') ] },
    {'name': 'harmons-site', 'tiers': [ (2, ['bruce','juan']), (1,'andres') ] },
    {'name': 'alexa', 'tiers': [ (3, ['octavio','andres','rommel']), (2,'mitchell') ] },
    {'name': 'admin', 'tiers': [ (3, ['pia','gema','allison']), (1,'walter') ] },
    {'name': 'qa', 'tiers': [ (2, ['franciso','ruddy'])] },
]
# { seat: person }
def fitness(assignments):
    return sum( seatFitness(assignments, assignments[seat], seat) for seat in assignments )

def seatFitness(assignments,person, seat):
    heat = heatFitness(person,seat)
    team = teamFitness(assignments,person,seat)
    return heat + team

def heatFitness(person,seat):
    if person not in peopleHeat: return 0
    desired = peopleHeat[person]
    heat = seatHeat[seat]
    diff = abs(desired - heat)
    happyness = 2 - diff
    return happyness * happyness

def isOnTeam(person,team):
    return any( person in tier[1] for tier in team['tiers']   )

# Assignments are { seat: person }
def teamFitness(assignments, person, seat):
    def teamFitnessForSeat(neighborSeat):
        if not neighborSeat in assignments: return 0 #Unoccupied seats are meaningless
        neighbor = assignments[neighborSeat]
        return sum( [teamFitnessForTeam(team,neighbor) for team in teams] )

    def teamFitnessForTeam(team,neighbor):
        if not isOnTeam(person,team) or not isOnTeam(neighbor,team): return 0
        return sum( [teamFitnessForTier(tier,person) for tier in team['tiers']] )


    def teamFitnessForTier(tier,neighbor):
        if neighbor in tier[1]: return tier[0]
        return 0

    return sum([teamFitnessForSeat(x) for x in adjacentSeats(seat)])
