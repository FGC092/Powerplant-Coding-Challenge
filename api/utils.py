def sortByPrice(e):
  return e['meritOrder']

def findIndex(list, key, value):
  return next((index for (index, d) in enumerate(list) if d[key] == value), None)

def mapLoadWithSources(load, sourceList, powerplants):
  try:
    loadDistribution = []
    unusedSources = []
    usedSources = []
    for source in sourceList:
      if load > powerplants[source['index']]['pmin']:
        if load <= source['availableLoad']:
          providedLoad = round(load,1)
          load = 0
        else:
          providedLoad = source['availableLoad']
          load = round(load - providedLoad,1)
        usedSources.append({"name": powerplants[source['index']]['name'],"p": providedLoad})
      else:
          unusedSources.append({"name": powerplants[source['index']]['name'],"p": powerplants[source['index']]['pmin']},)
          providedLoad = 0
      loadDistribution.append({"name": powerplants[source['index']]['name'],"p": providedLoad})
    return {"distribution":loadDistribution, "uncoveredLoad": load, "unusedSources":unusedSources, "usedSources":usedSources}
  except:
    print('mapLoadWithSources error')

def loadRedistribution(unusedSources, usedSources, noRenewableCurrentMeritOrder, remainingLoad):
  try:
    accumulatedExtraLoad = 0
    for source in unusedSources:
        extraLoadAvailable = source['p']
        accumulatedExtraLoad += extraLoadAvailable
        for listedSource in reversed(usedSources):
            if (listedSource['p'] < extraLoadAvailable):
                adjustment = listedSource['p']
            else:
                adjustment = extraLoadAvailable                        
            sourceIndex = findIndex(noRenewableCurrentMeritOrder, "source", listedSource['name'])
            noRenewableCurrentMeritOrder[sourceIndex]['availableLoad'] += -adjustment
            extraLoadAvailable += -adjustment
            if(extraLoadAvailable == 0):
                break
        if(accumulatedExtraLoad > remainingLoad):
            break   
    return noRenewableCurrentMeritOrder
  except:
    print('loadRedistribution error')