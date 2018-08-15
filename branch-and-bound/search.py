import fitness
import random
import itertools

people = set(fitness.people)

#partial
# assignments: {seat: person}

initial = {}


def greedy_search():
    bestConfig = random_config()
    bestFitness = fitness.fitness(bestConfig)
    searches = 1

    while True:
        searches += 1
        swapped = random_swap(bestConfig)
        fit = fitness.fitness(swapped)
        if(fit > bestFitness):
            bestFitness = fit
            bestConfig = swapped
            print('New best ',fit,searches)
            printConfiguration(swapped)

def random_swap(config):
    config = config.copy()
    seat1 = random.choice(fitness.seats)
    seat2 = random.choice(fitness.seats)
    temp = config[seat1]
    config[seat1] = config[seat2]
    config[seat2] = temp
    return config

def all_swaps(config):
    pairs = itertools.combinations(fitness.seats,2)
    for i, j in pairs:
        si = config[i]
        sj = config[j]
        if si == sj: continue
        copy = config.copy()
        copy[i] = sj
        copy[j] = si
        yield copy

def hill_climb(best_config, best_fit):
    while True:
        swaps = list(all_swaps(best_config));
        fit, i_config = max( (fitness.fitness(swaps[i]), i) for i in range(len(swaps )))
        config = swaps[i_config]
        if fit > best_fit:
            best_fit = fit
            best_config = config
        else:  return [ best_config, best_fit ]

def monte_carlo_search():
    bestConfig = {}
    bestFitness = -1
    searches = 0

    while True:
        searches += 1
        sam = random_config()
        fit = fitness.fitness(sam)
        sam, fit = hill_climb(sam, fit)
        if(fit > bestFitness):
            bestFitness = fit
            bestConfig = sam
            print('New best ',fit,searches)
            printConfiguration(sam)


def random_config():
    asgns = {}
    peps = list(fitness.people)
    seats = list(fitness.seats)
    random.shuffle(seats)
    return { seats[i]: (peps[i] if i < len(peps) else None)   for i in range(len(seats))  }

def depth_search():
    bestConfig = {}
    bestFitness =  -1
    searches = 0
    def deep_search_next(partial):
        nonlocal bestConfig
        nonlocal bestFitness
        nonlocal searches

        #{seat: person}
        if len(partial) == len(fitness.seats):
            searches += 1
            fit = fitness.fitness(partial)
            if(fit > bestFitness):
                bestFitness = fit
                bestConfig = partial
                print('New best ',fit,searches)
                printConfiguration(partial)
        kids = [x for x in children(partial)]
        kids.sort(key = fitness.fitness)
        kids.reverse()
        for kid in kids:
            deep_search_next(kid)

    deep_search_next(initial)
    print('Done! ',bestFitness,bestConfig)

def children(configuration):
    # Trade off. I've chosen  to not store unused seats and people and recalc these on each iteration.
    # I'm thinking that we're more memory constrained that CPU constrained. We'll see
    nextSeat = findNextSeat(configuration)
    if nextSeat == None: return []
    unseatedEmployees = findUnseatedEmployees(configuration)
    for emp in unseatedEmployees:
        asgn = configuration.copy();
        asgn[nextSeat] = emp
        yield asgn

def findNextSeat(configuration):
    if len(configuration) == len(fitness.seats): return None
    return next( seat for seat in fitness.seats if seat not in configuration)

def findUnseatedEmployees(configuration):
    seated = set(configuration.values())
    return people - seated

def printConfiguration(assignments):
    txt = ''
    for x in range(5):
        base = x * 3
        bottom = base if x > 0 else -1
        for s in range(bottom+1,base+4):
            if s in assignments: asgn = '[' + pad_center(assignments[s],10) + ']'
            else: asgn = ' [ ' + pad_center(str(s),10) + ' ]'
            txt += asgn
        txt += '\n'
    print(txt)

def pad_center(txt, desiredLength):
    actualLength = len(txt)
    needed = desiredLength - actualLength
    each = needed//2
    isOdd = needed % 1 == 1
    leach = each + 1 if isOdd else each
    return (' ' * leach) + txt + (' '*each)

#greedy_search()
#depth_search()

monte_carlo_search()

"""

[  mario  ][          ][          ]
[francisco][ wuelber ][          ]
[  rommel  ][ octavio ][  bruce  ]
[   juan   ][  andres  ][ mitchell ]
[christian][   jose   ][   luis   ]


"""
example = {
    1: 'mario',
    2: '',
    3: '',
    4: 'francisco',
    5: 'wuelber',
    6: '',
    7: 'rommel',
    8: 'octavio',
    9: 'bruce',
    10: 'juan',
    11: 'andres',
    12: 'mitchell',
    13: 'christian',
    14: 'jose',
    15: 'luis',
}

print(fitness.fitness(example))
example[4] = 'wuelber'
example[10] = ''
printConfiguration(example)
print(fitness.fitness(example))
#better, _ =  hill_climb(example, fitness.fitness(example))
