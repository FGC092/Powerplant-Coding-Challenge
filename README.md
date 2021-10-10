# Powerplant Coding Challenge

This is a Django project to solve the Powerplant Coding Challenge.

### *Run project*

To expose api in port :8888 please follow the setps:
  
   - Clone this repository
   - Create a virtual and activate environment (venv, virtualenv, conda...)
   - Install Django package
   - Run the following command: python3 manage.py runserver 8888
   - To call the api endpoint please use a post http call to http://127.0.0.1:8888/api/productionplan
   
If you are using Linux or Mac, there is a serve.sh script that can be executer with the following commnad: bash serve.sh
* Use this script only for installation, then activate the generated environment and run the following command: python3 manage.py runserver 8888

### *Project explanation*

This repository includes a Django project called 'PowerPlant' with an app called 'api'

/api/productionplan logic is included in views.py and utils.py inside api folder

### *Algorithm explanation*

The endpoint expects load, fuels and powerplants payload within the post request.

Free charge load sources should be included in freeChargeSouce source variable (eg. windturbine).

Algorithm will loop through provided powerplants to estimate power unitary merit order for no renewable sources.

It will also estimate the amount of power available by renewable sources taking into account weather conditions.

Next step is to sort the no renewable sources taking into account the obtained unitary merit order.

The algorithm will distribute the requested load starting with the renewable sources and following by sorted no renewable sources. 

This distribution will take into account the min and max available power by eache source using mapLoadWithSources() function.

To finish processing the request, the apgorithm will check if there is uncovered remining load using the most efficient configuration. 

If this is the case, a redistribution will take place to allow the use of sources discarded by pmin restriction. this is performed by the loadRedistribution() function.

### *Demo project*

Since this is a demo project, there are several disclamers:

   - This django project has its secret key exposed and should never be used in production.
   - Error handling is not the main objective of this demo and could not work properly if provided data is not structured as demo files.
   - The api should be exposed using a server other than the one included in Django by default such as Nginx or Apache.
