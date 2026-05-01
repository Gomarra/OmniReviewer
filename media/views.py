from django.shortcuts import render, get_object_or_404
from .models import Media
from .services import search_tmdb_movies, get_movie_details_tmdb # Vamos criar essa função

def search_media(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Aqui buscamos na API externa para teste
        results = search_tmdb_movies(query)
    
    return render(request, 'media/search.html', {'results': results, 'query': query})

def media_detail(request, category, external_id):
    # Tenta buscar no banco de dados local primeiro
    media = Media.objects.filter(category=category, external_id=external_id).first()

    # Se não existe localmente, busca na API e salva no banco
    if not media:
        if category == 'MOVIE':
            details = get_movie_details_tmdb(external_id)
            if details:
                media = Media.objects.create(
                    title=details['title'],
                    category='MOVIE',
                    synopsis=details['synopsis'],
                    release_date=details['release_date'],
                    image_url=details['image_url'],
                    external_id=external_id
                )

    return render(request, 'media/detail.html', {'media': media})