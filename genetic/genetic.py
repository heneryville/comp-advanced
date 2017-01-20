import random
from textblob import TextBlob
from functools import reduce


populationCap = 100
alphabet = 'abcdefghijklmnopqrstuvwxyzaeiouaeiou'
generation = 0
wordSize = (1,7)
sentenceSize = (3,7)
generations = 1000000000
mutationRate = .1
boost = 3

def randomIndividual():
    return [ randomWord() for i in range(random.randrange(sentenceSize[0], sentenceSize[1] )) ]

def randomWord():
    return ''.join([ random.choice(alphabet) for i in range(random.randrange(wordSize[0], wordSize[1]))  ])

def fitness(individual):
    positivity = reduce(lambda x,y: x + TextBlob(y).sentiment.polarity, individual,0)
    return positivity+1
    #repetition = reduce(lambda x,y: x + individual.count(y) -1 , individual,0)
    #return max(positivity - repetition/len(individual),0)

def reproduce(surviors, total):
    return crossOverWithMutation(surviors,total)

def asexualMutation(surviors,total):
    momDad = pick(survivors,total)
    return  [ mutateWord(random.choice( momDad ))   for i in range(random.randrange(sentenceSize[0], sentenceSize[1])) ]

def mutateWord(word):
    if random.random() > mutationRate: return word
    return randomWord()

def crossOverWithMutation(surviors, total):
    mom = pick(survivors,total)
    dad = pick(survivors,total)

    return  [ mutateWord(random.choice( [ random.choice(mom), random.choice(dad) ]))   for i in range(random.randrange(sentenceSize[0], sentenceSize[1])) ]

def crossOver(surviors, total):
    mom = pick(survivors,total)
    dad = pick(survivors,total)

    return  [ random.choice( [ random.choice(mom), random.choice(dad) ])   for i in range(random.randrange(sentenceSize[0], sentenceSize[1])) ]

def randomReproduction(surviors,total):
    return randomIndividual()

def pick(surviors, total):
    cursor = random.random() * total
    if len(survivors) == 0: return randomIndividual()
    for survivor in surviors:
        cursor = cursor - survivor[0]
        if(cursor <= 0):
            return survivor[1]
    return survivors[len(survivors) -1][1]

#1) Start with an initial pool of candidates
individuals = [ randomIndividual() for i in range(1,populationCap)  ]

print(individuals)

while generation < generations:
    generation = generation + 1
    #2) Fitness test them
    measures = [ (fitness(i),i) for i in individuals ]
    measures.sort(key=lambda x: x[0],reverse=True)
    maxval = measures[0]
    total = reduce(lambda x,y: x + y[0] , measures, 0)
    #3) Determine survival
    survivors = filter(None,[ i if random.random() < (i[0] + boost ) / (maxval[0] + boost + 1) else None  for i in measures ])
    print('Generation {} = {},{} Best: {}. Survivors: {}'.format(generation, maxval[0], total, ' '.join(maxval[1]), len(survivors)))

    #4) Reproduce
    individuals = [maxval[1]] + [ reproduce(survivors, total) for i in range(populationCap - 1)]
    random.shuffle(individuals)
