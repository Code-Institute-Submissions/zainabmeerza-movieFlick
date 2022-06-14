from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import requests

# Create your views here.
def index(request):
    query = request.GET.get('q')

    if query:
        url = 'https://www.omdbapi.com/?apikey=9c393141&s=' + query
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
        }

        template = loader.get_template('search_results.html')

        return HttpResponse(template.render(context, request))
    
    return render(request, 'index.html')

