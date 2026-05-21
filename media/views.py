from django.shortcuts import render

from review.forms import ReviewForm
from .models import Media
from .services import get_game_details_igdb, search_igdb_games, search_tmdb_movies, get_movie_details_tmdb

def search_media(request):
    query = request.GET.get('q')
    category_filter = request.GET.get('category') # Filtro opcional do usuário
    results = []

    if query:
        # Se o usuário não filtrou nada ou escolheu filmes
        if not category_filter or category_filter == 'MOVIE':
            results.extend(search_tmdb_movies(query))
        
        # Se o usuário não filtrou nada ou escolheu jogos
        if not category_filter or category_filter == 'GAME':
            results.extend(search_igdb_games(query))
            
    return render(request, 'media/search.html', {
        'results': results, 
        'query': query, 
        'category_filter': category_filter
    })

def media_detail(request, category, external_id):
    media = Media.objects.filter(category=category, external_id=external_id).first()

    if not media:
        if category == 'MOVIE':
            details = get_movie_details_tmdb(external_id)
        elif category == 'GAME':
            # Vamos criar essa função rápida ou adaptar o próprio retorno da busca
            details = get_game_details_igdb(external_id) # Crie uma lógica similar à busca por ID no services.py
            
        if details:
            media = Media.objects.create(
                title=details['title'],
                category=category,
                synopsis=details['synopsis'],
                release_date=details['release_date'],
                image_url=details['image_url'],
                external_id=external_id
            )

    # Lembre-se de passar o ReviewForm no contexto para o formulário de review aparecer!
    from review.forms import ReviewForm
    return render(request, 'media/detail.html', {'media': media, 'form': ReviewForm()})