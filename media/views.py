from django.shortcuts import render
from .services import search_tmdb_movies

def search_media(request):
    query = request.GET.get('q')
    results = []
    if query:
        # Aqui buscamos na API externa para teste
        results = search_tmdb_movies(query)
    
    return render(request, 'media/search.html', {'results': results, 'query': query})