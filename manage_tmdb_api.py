import requests


TMDB_API_KEY = "03816ec4d984b48d2e41b4539e486bab"
TMDB_SEARCH = "https://api.themoviedb.org/3/search/movie"
TMDB_GET_DETAILS = "https://api.themoviedb.org/3/movie"
TMDB_GET_POPULAR = "https://api.themoviedb.org/3/movie/popular"


def get_movie(movie) -> dict: 
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie,
    }
    movie = requests.get(TMDB_SEARCH, params)
    return movie.json()['results']


def get_details(movie_id):
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
    }
    movie = requests.get(f"{TMDB_GET_DETAILS}/{movie_id}", params=params)
    return movie.json()


def get_popular_movies():
    params = {
        'api_key': TMDB_API_KEY,
    }
    movie = requests.get(TMDB_GET_POPULAR, params=params)
    return movie.json()['results']
    






