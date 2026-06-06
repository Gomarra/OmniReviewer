from django.shortcuts import render, redirect, get_object_or_404

from review.forms import ReviewForm
from .models import Media, UserList
from django.contrib.auth.decorators import login_required
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

    current_status = None
    if request.user.is_authenticated and media:
        user_list_item = UserList.objects.filter(user=request.user, media=media).first()
        if user_list_item:
            current_status = user_list_item.status

    return render(request, 'media/detail.html', {
    'media': media, 
    'form': ReviewForm(),
    'current_status': current_status # Passa o status atual para o HTML
})

@login_required
def update_list_status(request, media_id):
    if request.method == 'POST':
        media = get_object_or_404(Media, id=media_id)
        status = request.POST.get('status')
        
        if status:
            # Atualiza o registro se já existir ou cria um novo
            UserList.objects.update_or_create(
                user=request.user,
                media=media,
                defaults={'status': status}
            )
        else:
            # Se o usuário escolher uma opção em branco/remover, deleta o registro
            UserList.objects.filter(user=request.user, media=media).delete()
            
        return redirect('media_detail', category=media.category, external_id=media.external_id)
    return redirect('media_index')