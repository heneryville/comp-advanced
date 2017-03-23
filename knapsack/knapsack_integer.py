import math
import sys
import queue
from knapsack_continuous import knapsack_continuous
from functools import reduce

discrete_materials = [
    #name, price per unit, unit weight, units available
    ('tv',419,15.76,2) #https://www.amazon.com/TCL-40FS3800-40-Inch-1080p-Smart/dp/B00UB9UJFQ/ref=sr_1_1?s=tv&ie=UTF8&qid=1488476504&sr=1-1&keywords=flat+screen&refinements=p_n_size_browse-bin%3A3578041011
    ,('painting',449.99,5,1) # http://www.art.com/products/p9634418529-sa-i5503232/claude-monet-regatta-at-argenteuil.htm?sOrig=CAT&sOrigID=0&dimVals=5000043-207238&ui=F73B6AD180A8452C9A66D92C6976FAAC&ac=true&PODConfigID=4985770
    ,('kitchen table',699,48,1) # http://www.ikea.com/us/en/catalog/products/20293766/
    ,('tablet',99.99,.01,2) #,https://www.amazon.com/dp/B00YYZEQ1G
    ,('bosch-mixer',389,12.3,1) # https://www.amazon.com/Bosch-MUM6N10UC-Universal-Stand-6-5-Quarts/dp/B0016KU16G
    ,('books',15,1.25,10) # https://www.reference.com/math/average-weight-book-cf771731e743d031
    ,('kindle',119.99,7.1,2) # https://www.amazon.com/Amazon-Kindle-Paperwhite-6-Inch-4GB-eReader/dp/B00OQVZDJM
    ,('silverware',23.95,2.5,2) # https://www.amazon.com/Stainless-Flatware-Luxurious-Silverware-Restaurant/dp/B01M0XDFX5/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1490279724&sr=1-1-spons&keywords=silverware&psc=1
    ,('water-jug',8.35,41.7,5) # varios
    ,('toilet paper',0.57,.2,48) # https://www.amazon.com/Charmin-Ultra-Toilet-Tissue-Double/dp/B00YMVI49W/ref=sr_1_2?s=home-garden&ie=UTF8&qid=1490279905&sr=1-2&keywords=toilet%2Bpaper&th=1
    ,('cash',100,0.1,5) # Cash
    ,('bike',42.63,21.75 ,3) # https://www.amazon.com/Dynacraft-Magna-Gravel-Blaster-12-Inch/dp/B008417IT8/ref=pd_sbs_21_1?_encoding=UTF8&pd_rd_i=B008417IT8&pd_rd_r=TFV4YK17N70TSGE1ADS6&pd_rd_w=tGLGE&pd_rd_wg=9VwuW&psc=1&refRID=TFV4YK17N70TSGE1ADS6
    ,('scooter',27.99, 5.45,2) # https://www.amazon.com/Razor-A-Kick-Scooter-Pink/dp/B000FK7C2E/ref=sr_1_1?s=sporting-goods&ie=UTF8&qid=1490280081&sr=1-1&keywords=razor+scooter
    ,('dirt',1.79,40,1000) # http://www.homedepot.com/p/40-lb-Topsoil-71140180/100355705
    ,('computer',719.99,12.34,2) # https://www.newegg.com/Product/Product.aspx?Item=N82E16883795360
    ,('loose change',1,.05,20) # http://lifehacker.com/5804773/quickly-estimate-how-much-moneys-in-your-change-jar-by-weight
    ,('cup',1.12,.125,16) #https://www.amazon.com/Break-Resistant-Restaurant-Quality-Beverage-Tumblers-Assorted/dp/B010E0N7ZU/ref=sr_1_6?ie=UTF8&qid=1490302203&sr=8-6&keywords=tumbler+cupsk
    ,('shoes',41.25,3,2) #https://www.amazon.com/ASICS-Gel-venture-Running-Titanium-Pistachio/dp/B00NUY4CHK/ref=sr_1_1?s=apparel&ie=UTF8&qid=1490302334&sr=1-1&nodeID=7141123011&psd=1&keywords=sneakers
    ,('light bulb',2.49,.2375,8) #https://www.amazon.com/Philips-433557-100-watt-Twister-4-Pack/dp/B00M6SR1JM/ref=sr_1_8?s=hi&ie=UTF8&qid=1490302418&sr=1-8&keywords=fluorescent+light+bul://www.amazon.com/Philips-433557-100-watt-Twister-4-Pack/dp/B00M6SR1JM/ref=sr_1_8?s=hi&ie=UTF8&qid=1490302418&sr=1-8&keywords=fluorescent+light+bulb
    ,('chair',38.34,15.35,4) #https://www.amazon.com/Winsome-Wood-Windsor-Chair-Natural/dp/B000NPOO6S/ref=sr_1_1?s=furniture&ie=UTF8&qid=1490302506&sr=1-1&keywords=kitchen+chai://www.amazon.com/Winsome-Wood-Windsor-Chair-Natural/dp/B000NPOO6S/ref=sr_1_1?s=furniture&ie=UTF8&qid=1490302506&sr=1-1&keywords=kitchen+chair
    ,('bed sheet',20,3,2) #https://www.amazon.com/AmazonBasics-Microfiber-Sheet-Set-Queen/dp/B00Q7OB4EE/ref=sr_1_5?s=home-garden&ie=UTF8&qid=1490302581&sr=1-5&keywords=bed+shee://www.amazon.com/AmazonBasics-Microfiber-Sheet-Set-Queen/dp/B00Q7OB4EE/ref=sr_1_5?s=home-garden&ie=UTF8&qid=1490302581&sr=1-5&keywords=bed+sheet
    ,('pillow',59.99,3.5,4) #https://www.amazon.com/Snuggle-Pedic-Ultra-Luxury-Combination-Kool-Flow-Micro-Vented/dp/B00PBFP0S6/ref=sr_1_1?s=home-garden&ie=UTF8&qid=1490302627&sr=1-1-spons&keywords=pillow&psc=://www.amazon.com/Snuggle-Pedic-Ultra-Luxury-Combination-Kool-Flow-Micro-Vented/dp/B00PBFP0S6/ref=sr_1_1?s=home-garden&ie=UTF8&qid=1490302627&sr=1-1-spons&keywords=pillow&psc=1
    ,('canned corn',1.5,1.116,10) #https://www.amazon.com/Kirkland-Golden-Sweet-Corn-15-25-12/dp/B004BGO5LY/ref=sr_1_3_s_it?s=grocery&ie=UTF8&qid=1490302739&sr=1-3&keywords=canned+corn
    ,('peanut butter',5.48,2.49,1) # https://www.amazon.com/Jif-Creamy-Peanut-Butter-40/dp/B00I8G7268/ref=sr_1_5_s_it?ie=UTF8&qid=1490302834&sr=1-5&keywords=peanut+butter
    ,('paper towels',1.5,.497,6) #https://www.amazon.com/Bounty-Paper-Towels-Prints-Count/dp/B015TYDZTE/ref=sr_1_1?srs=7301146011&ie=UTF8&qid=1490302915&sr=8-1&keywords=paper+towel://www.amazon.com/Bounty-Paper-Towels-Prints-Count/dp/B015TYDZTE/ref=sr_1_1?srs=7301146011&ie=UTF8&qid=1490302915&sr=8-1&keywords=paper+towels
    ,('plastic trash bags',0.141,.0455,90) # https://www.amazon.com/Glad-Kitchen-Drawstring-Trash-Gallon/dp/B00ASBOP9S
    ,('jeans', 50, 1, 5) #
];


# Returns an array of touples. Each touple has two values. The first is the drawn value, the second is a material array of what would be left
def choices(materials,limit):
    if(len(materials) == 0): return []
    head, *tail = materials
    return choicesForMaterial(head,limit)

def choicesForMaterial(m,limit):
    maxCanTake = min(m[3], math.floor(limit/m[2] ))
    #name, value, weight, taken
    return [ (m[0], m[1] * toTake, m[2] * toTake, toTake)  for toTake in range(0,maxCanTake + 1)]

# A candiate is a tuple of:
# 0) All the items taken (name, total_value, total_weight, cnt taken)
# 1) Index into the materials array, to show how to derive the materials left
# 2) Total value
# 3) Total weight
def children(candidate, masterMaterials, limit):
    priority, taken, index, value, weight, bounds  = candidate
    remainingMaterails = masterMaterials[index:len(masterMaterials)]
    return [ boundify( ( taken + [cs] , index + 1, value + cs[1], weight + cs[2] ), remainingMaterails, limit )  for cs in choices(remainingMaterails,limit-weight) ]

def boundify(candidate,remainingMaterials, limit):
    taken, index, value, weight  = candidate
    if(len(remainingMaterials) == 0): return (-upper,taken,index,value,weight, (value,value,value))
    knapsackContScore , knapsackContSolution = knapsack_continuous(remainingMaterials, limit-weight)
    #lower = value
    lower = sum([ m[1] * math.floor(m[2]) / m[2]   for m in knapsackContSolution if m[2] > 0  ]) + value # knapsack, and then drop the fractions
    #upper = max([ m[1]/m[2] for m in remainingMaterials]) * (limit - weight) + value #Take all of what is left of the most valuable thing
    upper = knapsackContScore + value
    if(upper < lower):
        raise Exception('Upper cannot be less than lower ' + str(lower) + ' ' + str(upper))
    return (-upper, taken, index, value, weight, (lower,value,upper))


def formatTakings(takings):
    return ', '.join(str(t[3]) + 'x ' + str(t[0])  for t in takings if t[3] >0 )

def calcPruneSavings(candidate,masterMaterials,limit):
    priority, taken, index, value, weight, bounds  = candidate
    remainingMaterials = masterMaterials[index:len(masterMaterials)]
    limitLeft = limit - weight
    savings = reduce( (lambda m,x: m*x), [ min(m[3], math.floor(limitLeft/m[2] )) +1 for m in remainingMaterials ] , 1)
    return savings


def knapsack_integer(materials, limit):
    pq = queue.PriorityQueue(0)
    pq.put( (0,[],0,0,0, (0,0,sys.float_info.max)) )
    bestSolution = None
    bestSolutionBounds = (0,0,sys.float_info.max)
    iteration = 0
    prunings = 0
    while(not pq.empty()):
        iteration = iteration +1
        candidate = pq.get()
        if(iteration % 100000 == 0): print('Iteration',iteration,pq.qsize(),prunings )
        bounds = candidate[5]
        if(bounds[2] < bestSolutionBounds[0]):
            # If the candidate's best possible is still lower than the worst possible for our so-far, then don't expore it
            prunings = prunings + calcPruneSavings(candidate,materials,limit)
            #print('Pruned',candidate,bounds)
            continue
        cs = children(candidate, materials, limit)
        #print('Children',cs)
        for child in cs:
            if(child[3] > bestSolutionBounds[1]):
                bestSolution = child
                bestSolutionBounds = child[5]
                #print('New best',bestSolution,'at iteration',iteration,'with prunings',prunings,bestSolutionBounds)
                print('New best',formatTakings(bestSolution[1]),'will get you','$' +str(bestSolution[3]), bestSolutionBounds)
            pq.put( child)
    return (bestSolution,iteration,prunings)

#print('children', children(([('tv', 838, 31.52, 2)], 1, 838, 31.52), discrete_materials,50))
solution, iterations, prunings = knapsack_integer(discrete_materials, 50)
priority, taken,index,value,weight,bounds = solution
print('----------------------------------')
print('Take:', formatTakings(taken))
print('Value:','$'+str(value))
print('Weight:',weight,'lbs')
print('Iterations:',iterations)
print('Prunings:',prunings)
