people = [ 'andres','francisco','mario','octavio','rommel','christian','jose','juan','bruce','mitchell','kathya', 'luis p', 'wuelber', 'lawrence', 'luis f', '']

"""
Seat labels
---------------------
|    0   1   2   3   |
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


seats = list(range(0,16))

def sameRowAdjacentSeats(seat):
    if seat == 0: return [(1,1)]
    if seat == 1: return [(0,1),(2,1)]
    if seat % 3 == 0: return [ (seat -1,1)  ]
    if seat % 3 == 1: return [ (seat + 1,1)  ]
    return [ (seat - 1,1), (seat + 1,1) ]

def opposingRowAdjacents(seat):
    if seat in [0,1,2,3]: return [4,5,6]
    if seat in [4,5,6]: return [0,1,2,3]
    if seat in [7,8,9]: return [10,11,12]
    if seat in [10,11,12]: return [7,8,9]
    return []

def adjacentSeats(seat):
    return sameRowAdjacentSeats(seat) + [ (x,.5) for x in  opposingRowAdjacents(seat) ]

# 0 means it's cold, 2 means it's hot
seatHeat = {
        0: .5, 1:  .5,   2:  0,   3:  1,
            4:  0,   5:  .5,   6:  2,
            7:  0,   8:  1,   9:  2,
            10: 1,   11: 1,   12: 2,
            13: 2,   14: 2,   15: 3,
            }

# 0 means you like it cold, 2 means you like it hot, absence means you don't care
"""
Mario: Ice cold
Octavio: 21
Christian: 21
Jose: Cold
Kathya: Cold
"""
peopleHeat = {
    'mario': -1,
    'francisco': 0,
    'octavio': 1,
    'christian': 1,
    'jose': 0,
    'kathya': 0,
    'mitchell': 3,

    'bruce': 2,
    'andres': 2,
}

# Each team has various tiers,
teams = [
    {'name': 'mobile', 'tiers': [ (4, ['jose','christian']) ] },
    {'name': 'harmons-site', 'tiers': [ (1, ['bruce','juan']), (.1,['andres']) ] },
    {'name': 'alexa', 'tiers': [ (3, ['octavio','andres','rommel','wuelber']), (2,['mitchell','lawrence']),(1,['luis f'])  ] },
    {'name': 'sitecore', 'tiers': [ (3, ['jose','christian','luis p','lawrence', 'luis f'])] },
    {'name': 'qa', 'tiers': [ (2, ['kathya','francisco'])] },
]
# { seat: person }
def fitness(assignments):
    return sum( seatFitness(assignments, assignments[seat], seat) for seat in assignments ) + ( 2 if 'mitchell' in [ assignments[s] for s in [3,6,9,12,15] ] else 0)

def seatFitness(assignments,person, seat):
    heat = heatFitness(person,seat)
    team = teamFitness(assignments,person,seat)
    #print('For',person,'in',seat,team)
    return heat + team

# The fitness for the given person being in the given seat
def heatFitness(person,seat):
    if person not in peopleHeat: return 0
    desired = peopleHeat[person]
    heat = seatHeat[seat]
    diff = abs(desired - heat)
    return -diff**2

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

    return sum([ v * teamFitnessForSeat(s) for s,v in adjacentSeats(seat)])
