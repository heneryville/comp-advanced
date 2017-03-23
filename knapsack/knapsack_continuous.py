materials = [
    #name, price per unit, unit weight, units available
    ('copper',2.79,1,3), # http://www.infomine.com/investment/metal-prices/copper/
    ('silver',236.76,1,7), # https://trendshare.org/how-to-invest/the-current-price-of-silver-today
    ('dirt',1.79,40,1000), # http://www.homedepot.com/p/40-lb-Topsoil-71140180/100355705
    ('gold',18087.56,1,10), # http://onlygold.com/Info/Value-Your-Weight-In-Gold.asp
    ('paper',11.87,20,10), # https://www.amazon.com/Hammermill-letter-Bright-Sheets-105007R/dp/B005NL739M/ref=lp_1069722_1_1?s=office-products&ie=UTF8&qid=1488475423&sr=1-1
];
"""
max
2.79 236.76 1.79 18087.56 11.87

1 1 40 1 20 -1 50
1 0 0 0 0 -1 3
0 1 0 0 0 -1 7
0 0 1 0 0 -1 1000
0 0 0 1 0 -1 10
0 0 0 0 1 -1 10
"""

def knapsack_continuous(materials, limit):
  strengthLeft = limit;
  take = []
  valueTaken = 0;
  valuePerPound = [ (materials[ind][1]/materials[ind][2],ind) for ind in range(len(materials)) ]
  valuePerPound.sort(key= lambda x: x[0] )
  valuePerPound.reverse()
  for vpp in valuePerPound:
    material = materials[vpp[1]]
    lbsToTake = min(strengthLeft,material[3] * material[2])
    value = lbsToTake * vpp[0]
    valueTaken = valueTaken + value
    strengthLeft = strengthLeft - lbsToTake;
    unitsToTake = lbsToTake/material[2]
    take.append( (material[0],lbsToTake, unitsToTake, value)  )
  return (valueTaken, take)

#print('Continuous Knapsack',knapsack_continuous(materials,50))

