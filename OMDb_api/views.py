from django.shortcuts import render
from .forms import SearchForm
import requests
from django.http import HttpResponse

# Create your views here.


def param_api_key():
    api_key = ''
    return {'apikey': api_key}

def Index(request):

    context_render = {}

    if request.method == 'GET' and 'search' in request.GET:
        form = SearchForm(request.GET)
        
        search = request.GET['search']
        year = request.GET['year']

        params_obj = param_api_key()
        params_obj['s'] = search

        if year:
            params_obj['y'] = year
        
        try:
            omdb_request = requests.get('http://www.omdbapi.com/', params=params_obj)
            omdb_request.raise_for_status()
            context_render['search_results'] = omdb_request.json()
        
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
        
    print(context_render)
    return render(request, 'title.html', context_render)
