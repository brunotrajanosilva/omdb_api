from django.shortcuts import render
from .forms import SearchForm
import requests
from django.http import HttpResponse
import os
import math

# Create your views here.


def param_api_key():
    # omdb api key
    api_key = os.environ.get('omdb_api_key')
    return {'apikey': api_key}

def Index(request):
    context_render = {}

    if request.method == 'GET' and 'search' in request.GET:
        form = SearchForm(request.GET)

        search = request.GET['search']
        year = request.GET['year']
        page = request.GET['page']

        params_obj = param_api_key()
        params_obj['s'] = search

        if year:
            params_obj['y'] = year
        
        if page:
            params_obj['page'] = page

        try:
            omdb_request = requests.get('http://www.omdbapi.com/', params=params_obj)

            omdb_request.raise_for_status()

            request_json = omdb_request.json()
            context_render['results'] = request_json

            if 'totalResults' in request_json:
                total_results = int(request_json['totalResults'])
                total_per_items = total_results / 10
                context_render['last'] =  math.ceil(total_per_items)


            context_render['previous'] = int(page) - 1
            context_render['page'] = int(page)
            context_render['next'] = int(page) + 1
        
        except requests.exceptions.RequestException as exception:
            return HttpResponse(exception)

    else:
        form = SearchForm()


    context_render['form'] = form
    return render(request, 'index.html', context_render)


def Title(request, id):

    params_obj = param_api_key()
    params_obj['i'] = id
    params_obj['plot'] = 'full'

    try:
        omdb_request = requests.get('http://www.omdbapi.com/', params=params_obj)
        omdb_request.raise_for_status()

        context_render = {'title' : omdb_request.json()}

    except requests.exceptions.RequestException as exception:
        return HttpResponse(exception)
        
    return render(request, 'title.html', context_render)
