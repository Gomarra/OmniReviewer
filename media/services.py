import requests
from .models import Media
import datetime

# TMDB - API de filmes

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

# IGDB - API de jogos
IGDB_CLIENT_ID = 'ssb1ykl34j7l55m35fagf7uhfwguyh'
IGDB_ACCESS_TOKEN = 'm17wpyfw3k1mm2p5bsk2iaprny8sk1'
IGDB_BASE_URL = 'https://api.igdb.com/v4'

def search_igdb_games(query):
    url = "https://api.igdb.com/v4/games"
    headers = {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {IGDB_ACCESS_TOKEN}',
    }
    
    # Linguagem de consulta do IGDB (pedindo id, nome, resumo, data e capa)
    body = f'search "{query}"; fields name, summary, first_release_date, cover.url; limit 10;'
    
    response = requests.post(url, headers=headers, data=body)
    
    if response.status_code == 200:
        results = response.json()
        formatted_results = []
        for item in results:
            # Tratamento para a imagem da capa do jogo
            image_url = None
            if 'cover' in item:
                # Substitui o padrão 'thumb' por 'cover_big' para ter uma imagem de melhor qualidade
                image_url = "https:" + item['cover']['url'].replace('t_thumb', 't_cover_big')
            
            # Conversão de timestamp Unix para o formato YYYY-MM-DD
            import datetime
            release_date = None
            if 'first_release_date' in item:
                release_date = datetime.date.fromtimestamp(item['first_release_date']).strftime('%Y-%m-%d')

            formatted_results.append({
                'external_id': item['id'],
                'title': item['name'],
                'synopsis': item.get('summary', ''),
                'release_date': release_date,
                'image_url': image_url,
                'category': 'GAME' # Define automaticamente como jogo!
            })
        return formatted_results
    return []

def get_game_details_igdb(game_id):
    url = f"{IGDB_BASE_URL}/games"
    headers = {
        'Client-ID': IGDB_CLIENT_ID,
        'Authorization': f'Bearer {IGDB_ACCESS_TOKEN}',
    }
    body = f"fields name, summary, first_release_date, cover.url; where id = {game_id};"
    response = requests.post(url, headers=headers, data=body)
    
    if response.status_code == 200:
        results = response.json()
        # Como filtramos por ID, a API retorna uma lista com um único elemento se encontrar o jogo
        if results:
            data = results[0]
            
            # Tratamento da imagem da capa (transformando o thumbnail padrão em imagem grande)
            image_url = None
            if 'cover' in data:
                image_url = "https:" + data['cover']['url'].replace('t_thumb', 't_cover_big')
            
            # Tratamento do formato da data (IGDB entrega um Timestamp Unix, precisamos converter para YYYY-MM-DD)
            release_date = None
            if 'first_release_date' in data:
                release_date = datetime.date.fromtimestamp(data['first_release_date']).strftime('%Y-%m-%d')
            
            # Retorna o dicionário com as chaves exatas que a sua View espera para salvar no banco
            return {
                'title': data['name'],
                'synopsis': data.get('summary', 'Sinopse não disponível.'),
                'release_date': release_date,
                'image_url': image_url,
            }
            
    return None