import json
from django.conf.global_settings import SESSION_COOKIE_SECURE
from django.http import HttpResponse
from django.template import loader

from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from api.utils import sortByPrice, mapLoadWithSources, loadRedistribution

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@method_decorator(csrf_exempt, name='dispatch')
class productionplan(View):

    def post(self, request, *args, **kwargs):
        # Fuel source for each power generator
        sourceFuel = {
            'windturbine':{'fuel': 'wind(%)', 'co2':0},
            'gasfired':{'fuel': 'gas(euro/MWh)', 'co2':0.3},
            'turbojet':{'fuel': 'kerosine(euro/MWh)', 'co2':0},
        }
        # Input data
        input = json.loads(request.body)
        load = input['load']
        fuels = input['fuels']
        powerplants = input['powerplants']
        # Define renewable power generators
        freeChargeSouce = ['windturbine']
        # Variable initialization
        renewableLoad = 0
        sourceTypes = []
        noRenewableCurrentMeritOrder = []
        renewableSourceList = []
        # Review provided data and estimate merit order for no renewables.
        for index,source in enumerate(powerplants):
            if (not source['type'] in sourceTypes):
                sourceTypes.append(source['type'])
            if (source['type'] in freeChargeSouce):
                renewableSource = sourceFuel[source['type']]['fuel']
                renewableLoad = source['pmax']*fuels[renewableSource]/100
                renewableSourceList.append({
                    'source':source['name'], 
                    'index':index, 
                    'availableLoad':renewableLoad
                })
            else:
                noRenewableSource = sourceFuel[source['type']]['fuel']
                unitaryPrice = fuels[noRenewableSource]
                meritOrder = unitaryPrice / source['efficiency'] + sourceFuel[source['type']]['co2'] * fuels['co2(euro/ton)']
                noRenewableCurrentMeritOrder.append({
                    'source':source['name'],
                    'meritOrder':meritOrder, 
                    'index':index, 
                    'availableLoad':source['pmax']
                })
        # Sort no renewables by merit order.
        noRenewableCurrentMeritOrder.sort(key=sortByPrice)
        # Provide requested load in the maximizing cost efficiency.
        # ··· Only renewable load
        distributionResult = mapLoadWithSources(load, renewableSourceList, powerplants)
        loadDistribution_rw = distributionResult["distribution"]
        # ··· No renewable load after applying renewable load
        remainingLoad_rw = distributionResult["uncoveredLoad"]
        distributionResult = mapLoadWithSources(remainingLoad_rw, noRenewableCurrentMeritOrder, powerplants)
        loadDistribution = loadDistribution_rw + distributionResult["distribution"]
        remainingLoad = distributionResult["uncoveredLoad"]
        print('Uncovered load:', remainingLoad)
        if remainingLoad > 0:
            # Most cost efficient distribution cannot match the required load
            # Redistribute load sources to match required load
            noRenewableCurrentMeritOrder = loadRedistribution(distributionResult["unusedSources"], distributionResult["usedSources"], noRenewableCurrentMeritOrder, remainingLoad)
            # Generate new load distribution
            distributionResult = mapLoadWithSources(remainingLoad_rw, noRenewableCurrentMeritOrder, powerplants)
            loadDistribution = loadDistribution_rw + distributionResult["distribution"]
            remainingLoad = distributionResult["uncoveredLoad"]
            print('Uncovered load:', remainingLoad)
        return JsonResponse(loadDistribution, safe=False)

