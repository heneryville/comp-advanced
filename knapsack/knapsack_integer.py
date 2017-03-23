import math
import sys
import queue
import knapsack_continuous
#from knapsack_continuous import knapsack_continuous

discrete_materials = [
    #name, price per unit, unit weight, units available
    ('tv',419,15.76,2), #https://www.amazon.com/TCL-40FS3800-40-Inch-1080p-Smart/dp/B00UB9UJFQ/ref=sr_1_1?s=tv&ie=UTF8&qid=1488476504&sr=1-1&keywords=flat+screen&refinements=p_n_size_browse-bin%3A3578041011
    ('monet painting',449.99,5,1), # http://www.art.com/products/p9634418529-sa-i5503232/claude-monet-regatta-at-argenteuil.htm?sOrig=CAT&sOrigID=0&dimVals=5000043-207238&ui=F73B6AD180A8452C9A66D92C6976FAAC&ac=true&PODConfigID=4985770
    ('kitchen table',699,48,1), # http://www.ikea.com/us/en/catalog/products/20293766/
    ('tablet',99.99,.01,2), #,https://www.amazon.com/dp/B00YYZEQ1G
    ('bosch mixer',389,12.3,1), # https://www.amazon.com/Bosch-MUM6N10UC-Universal-Stand-6-5-Quarts/dp/B0016KU16G
    ('books',15,1.25,10), # https://www.reference.com/math/average-weight-book-cf771731e743d031
    ('kindle',119.99,7.1,2), # https://www.amazon.com/Amazon-Kindle-Paperwhite-6-Inch-4GB-eReader/dp/B00OQVZDJM
    ('silverware',23.95,2.5,2), # https://www.amazon.com/Stainless-Flatware-Luxurious-Silverware-Restaurant/dp/B01M0XDFX5/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1490279724&sr=1-1-spons&keywords=silverware&psc=1
    ('water jug',8.35,41.7,5), # varios
    ('toilet paper',0.57,.2,48), # https://www.amazon.com/Charmin-Ultra-Toilet-Tissue-Double/dp/B00YMVI49W/ref=sr_1_2?s=home-garden&ie=UTF8&qid=1490279905&sr=1-2&keywords=toilet%2Bpaper&th=1
    ('cash',100,0.1,5), # Cash
    ('kids bike',42.63,21.75 ,3), # https://www.amazon.com/Dynacraft-Magna-Gravel-Blaster-12-Inch/dp/B008417IT8/ref=pd_sbs_21_1?_encoding=UTF8&pd_rd_i=B008417IT8&pd_rd_r=TFV4YK17N70TSGE1ADS6&pd_rd_w=tGLGE&pd_rd_wg=9VwuW&psc=1&refRID=TFV4YK17N70TSGE1ADS6
    ('scooter',27.99, 5.45,2), # https://www.amazon.com/Razor-A-Kick-Scooter-Pink/dp/B000FK7C2E/ref=sr_1_1?s=sporting-goods&ie=UTF8&qid=1490280081&sr=1-1&keywords=razor+scooter
    ('dirt',1.79,40,1000), # http://www.homedepot.com/p/40-lb-Topsoil-71140180/100355705
    ('computer',719.99,12.34,2), # https://www.newegg.com/Product/Product.aspx?Item=N82E16883795360
];

# Returns an array of touples. Each touple has two values. The first is the drawn value, the second is a material array of what would be left
def choices(materials,limit):
    if(len(materials) == 0):
        return []
    head, *tail = materials
    return choicesForMaterial(head,limit)

def choicesForMaterial(m,limit):
    maxCanTake = min(m[3], math.floor(limit/m[2] ))
    #name, value, weight, taken
    return [ (m[0], m[1] * toTake, m[2] * toTake, toTake)  for toTake in range(0,maxCanTake + 1) if toTake >= 0 ]

# A candiate is a tuple of:
# 0) All the items taken (name, total_value, total_weight, cnt taken)
# 1) Index into the materials array, to show how to derive the materials left
# 2) Total value
# 3) Total weight
def children(candidate, masterMaterials, limit):
    taken, index, value, weight  = candidate
    remainingMateraisl = masterMaterials[index:len(masterMaterials)]
    return [ ( taken + [cs] , index + 1, value + cs[1], weight + cs[2], ( lowerBound()  ) )  for cs in choices(remainingMateraisl,limit-weight) ]

def calcBounds(candidate, masterMaterials, limit):
    taken, index, value, weight  = candidate
    remainingMaterials = masterMaterials[index:len(masterMaterials)]
    current = candidate[2]
    lower = current #Worst thing is we take nothing else. We can do better by running a reverse knapsack?
    upper = knapsack_continuous(remainingMateraisl, limit-weight)
    return (lower,candidate[2],upper)

def knapsack_integer(materials, limit):
  pq = queue.Queue(0)
  pq.put( ([],0,0,0) )
  bestSolution = None
  bestSolutionBounds = (0,0,sys.float_info.max)
  iteration = 0
  prunings = 0
  while(not pq.empty()):
      iteration = iteration +1
      candidate = pq.get()
      #print('Iteration',iteration, candidate)
      bounds = calcBounds(candidate,materials,limit)
      if(bounds[2] <= bestSolutionBounds[0]): # If the candidate's best possible is still lower than the worst possible for our so-far, then don't expore it
          prunings = prunings + 1
          continue
      cs = children(candidate, materials, limit)
      for child in children(candidate,materials,limit):
          if(child[2] > bestSolutionBounds[1]):
              print('New best',child,'at iteration',iteration,'with prunings',prunings)
              bestSolution = child
              bestSolutionBounds = calcBounds(child)
          pq.put(child)
  return bestSolution

#print('children', children(([('tv', 838, 31.52, 2)], 1, 838, 31.52), discrete_materials,50))
print('Soluction', knapsack_integer(discrete_materials, 50))
