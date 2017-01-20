import random

n = 4
lookback = n -1
ngrams = {}
START = '<START>'
END = '<END>'

def chunk(line):
  pieces = [ *[START for i in range(lookback)], *line.split(), END ]
  for i in range(len(pieces) - lookback):
      yield ( tuple( [pieces[i+j]  for j in range(lookback)]  ), pieces[i+lookback] )

def learn(chunk,strength):
    key, target = chunk
    targets = {}
    if key in ngrams:
        targets = ngrams[key]
    else:
        ngrams[key] = targets

    if target in targets:
        targets[target] = targets[target] + strength
    else:
        targets[target] = strength

def generate():
  seq = []
  prior = tuple([START for i in range(lookback)])

  while prior[-1] != END:
      nextNode = gennext(prior)
      seq.append(nextNode)
      prior = tuple([ *list(prior)[1:], nextNode  ])
  return ' '.join(seq[0:-1])

def gennext(prior):
    options = ngrams[prior]
    totalProbs = sum([ options[option] for option in options ])
    numPicked = random.uniform(0,totalProbs)
    for option in options:
        numPicked = numPicked - options[option]
        if numPicked < 0: return option

def prescriptiveness():
    keys = len(ngrams)
    return sum( [ len(ngrams[key]) for key in ngrams ] ) / float(keys)

def train(corpus,strength):
    #Train ngrams
    with open(corpus,'r') as file:
        for line in file:
            if(len(line.strip())<=0): continue
            for c in chunk(line):
                learn(c,strength)
    print('Learned the corpus',corpus)

#train('bible-corpus.txt',1)
train('slack-corpus.txt',1)
#train('shakespeare-corpus.txt',1)

#print('Corpus prescriptiveness',prescriptiveness())
for i in range(1,200):
  print(generate())

