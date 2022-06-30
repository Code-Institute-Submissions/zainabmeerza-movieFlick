from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from movie.models import Movie, Genre, Rating
from actor.models import Actor
from django.utils.text import slugify
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
            'page_number':1,
        }

        template = loader.get_template('search_results.html')

        return HttpResponse(template.render(context, request))
    
    return render(request, 'index.html')


def pagination(request, query, page_number):
    url = 'https://www.omdbapi.com/?apikey=9c393141&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }

    template = loader.get_template('search_results.html')

    return HttpResponse(template.render(context, request))


def movieDetails(request, imdb_id):

    if Movie.objects.filter(imdbID=imdb_id).exists():
        movie_data = Movie.objects.get(imdbID=imdb_id)
        our_db = True

    else:
        url = 'https://www.omdbapi.com/?apikey=9c393141&i=' + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        #Inject to our database:

        rating_objects = []
        genre_objects = []
        actor_objects = []

        #For the actors
        actor_list = [x.strip() for x in movie_data['Actors'].split(',')]

        for actor in actor_list:
            a, created = Actor.objects.get_or_create(name=actor)
            actor_objects.append(a)
        
        #For the genres
        genre_list = list(movie_data['Genre'].replace(" ", "").split(','))

        for genre in genre_list:
            genre_slug = slugify(genre)
            g, created = Genre.objects.get_or_create(title=genre, slug=genre_slug)
            genre_objects.append(g)

        #For the ratings
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            rating_objects.append(r)

        if movie_data['Type'] =='movie':
            m, created = Movie.objects.get_or_create(
                Title=movie_data['Title'],
                Year=movie_data['Year'],
                Rated=movie_data['Rated'],
                Released=movie_data['Released'],
                Runtime=movie_data['Runtime'],
                Director=movie_data['Director'],
                Writer=movie_data['Writer'],
                Plot=movie_data['Plot'],
                Awards=movie_data['Awards'],
                Poster_url=movie_data['Poster'],
                Metascore=movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                DVD=movie_data['DVD'],
                BoxOffice=movie_data['BoxOffice'],
                Production=movie_data['Production'],
                Website=movie_data['Website'],
                )
            m.Genre.set(genre_objects)
            m.Actors.set(actor_objects)
            m.Ratings.set(rating_objects)

        elif movie_data['Type'] =='game':
            m, created = Movie.objects.get_or_create(
                Title=movie_data['Title'],
                Year=movie_data['Year'],
                Rated=movie_data['Rated'],
                Released=movie_data['Released'],
                Runtime=movie_data['Runtime'],
                Director=movie_data['Director'],
                Writer=movie_data['Writer'],
                Plot=movie_data['Plot'],
                Awards=movie_data['Awards'],
                Poster_url=movie_data['Poster'],
                Metascore=movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                DVD=movie_data['DVD'],
                BoxOffice=movie_data['BoxOffice'],
                Production=movie_data['Production'],
                Website=movie_data['Website'],
                )
            m.Genre.set(genre_objects)
            m.Actors.set(actor_objects)
            m.Ratings.set(rating_objects)

        else:
            m, created = Movie.objects.get_or_create(
                    Title=movie_data['Title'],
                    Year=movie_data['Year'],
                    Rated=movie_data['Rated'],
                    Released=movie_data['Released'],
                    Runtime=movie_data['Runtime'],
                    Director=movie_data['Director'],
                    Writer=movie_data['Writer'],
                    Plot=movie_data['Plot'],
                    Awards=movie_data['Awards'],
                    Poster_url=movie_data['Poster'],
                    Metascore=movie_data['Metascore'],
                    imdbRating=movie_data['imdbRating'],
                    imdbVotes=movie_data['imdbVotes'],
                    imdbID=movie_data['imdbID'],
                    Type=movie_data['Type'],
                    totalSeasons=movie_data['totalSeasons'],
                    )
            m.Genre.set(genre_objects)
            m.Actors.set(actor_objects)
            m.Ratings.set(rating_objects)

        for actor in actor_objects:
            actor.movies.add(m)
            actor.save()

        m.save()
        our_db = False

        context = {
            'movie_data': movie_data,
            'our_db': our_db,
        }

    template = loader.get_template('movie_details.html')

    return HttpResponse(template.render(context, request))

