import requests
from .models import Media

TMDB_API_KEY = '3a5be14811d55bd9906cc2ecc98a8987' # Coloque sua chave aqui
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def search_tmdb_movies(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'pt-BR'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        formatted_results = []
        for item in results:
            formatted_results.append({
                'external_id': item['id'],
                'title': item['title'],
                'synopsis': item['overview'],
                'release_date': item.get('release_date'),
                'image_url': f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item['poster_path'] else None,
                'category': 'MOVIE'
            })
        return formatted_results
    return []

def get_movie_details_tmdb(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {'api_key': TMDB_API_KEY, 'language': 'pt-BR'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'title': data['title'],
            'synopsis': data['overview'],
            'release_date': data.get('release_date'),
            'image_url': f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data['poster_path'] else None,
        }
    return None